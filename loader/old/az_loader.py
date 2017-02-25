# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from setting import Setting
import os.path
import json
import requests
import re
import datetime
import socket
from urllib.parse import urlparse,urlsplit
from io import BytesIO
from multiprocessing import Lock

from loader.base_loader import URL

class LoaderError(RuntimeError):
    def __init__(self, txt):
        self.txt = txt

    def __str__(self):
        return self.txt

class AZLoader():
    config_filename = Setting.base_dir + 'az.json'
    initialized = False
    pac_url = "http://antizapret.prostovpn.org/proxy.pac"
    last_loaded=None

    proxy_domains = list()
    free_http_proxy=None
    proxies=None

    trick_headers={
    'sp_method': "GET  {0} HTTP/1.0\r\nHost: {1}\r\nConnection: close\r\n\r\n",
    'cr_method': "\nGET {0} HTTP/1.0\r\nHost: {1}\r\nConnection: close\r\n\r\n",
    'tab_method': "GET {0} HTTP/1.0\r\nHost: {1}\t\r\nConnection: close\r\n\r\n",
    'point_method': "GET {0} HTTP/1.0\r\nHost: {1}.\r\nConnection: close\r\n\r\n",
    'host_method': "GET {0} HTTP/1.0\r\nhost: {1}\r\nConnection: close\r\n\r\n",
    'unix_method': "GET {0} HTTP/1.0\nHost: {1}\nConnection: close\n\n",
    'order_method': "GET {0} HTTP/1.0\r\nConnection: close\r\nHost: {1}\r\n\r\n",
    }

    def __init__(self):
        if AZLoader.initialized:
            print('AZ loader init\'ed')
            return
        print('Requests version: ' + requests.__version__)
        self.read_config()
        self.read_proxy_pac()
        # self.proxies = {'http': self.free_http_proxy}
        AZLoader.initialized=True
        print('AZ loader read', len(AZLoader.proxy_domains), 'domains')

    @staticmethod
    def test_url_az(url:URL)->bool:
        if url.forced_unproxy:
            return False
        if url.forced_proxy:
            return True
        domain=url.domain()
        for item in AZLoader.proxy_domains:
            if '.' + item in domain or item == domain:
                # print(item,domain)
                return True
        return False

    def _inspect_availability(self,url:URL)->str:
        if url.test_string is None:
            return 'plain'

        url.forced_unproxy=True
        string=self.requests_load(url)
        # print(string)
        if url.test_string in string:
            return 'plain'

        url.forced_unproxy=False
        url.forced_proxy=True
        string=self.requests_load(url)
        # print(string)
        if url.test_string in string:
            return 'proxy'

        for method_name in AZLoader.trick_headers:
            # print(method_name)
            string = self.trick_load(url,trick_name=method_name)
            # print(string)
            if url.test_string in string:
                return method_name

        return 'none'

    def safe_load(self, url, fname: str, overwrite=True)->str:
        try:
            return self.load(url, fname, overwrite)
        except (ValueError, LoaderError) as Error:
            print(url.get() + ' not loaded: ', Error)
            return ''

    def load(self, url:URL, fname: str = '', overwrite=True)->str:
        return self.requests_load(url,fname,overwrite)

    def requests_load(self, url:URL, fname: str = '', overwrite=True)->str:
        # print('Loading',url.get(),'to',fname)
        filename = ''

        if overwrite or (not os.path.exists(fname)):
            # print(self.test_url_az(url))
            if self.test_url_az(url):
                # print('Proxy ON')
                proxies=AZLoader.proxies
            else:
                proxies=None

            # print(proxies)
            try:
                if url.method == 'GET':
                    response = requests.get(url, cookies=url.coockies,proxies=proxies)
                elif url.method == 'POST':
                    response = requests.post(url, data=url.post_data,proxies=proxies)
                else:
                    raise LoaderError('Unknown method:' + url.method)

                response.raise_for_status()

                if fname is not '':
                    path = os.path.dirname(fname)
                    filename = os.path.split(fname)[1]

                    if not os.path.exists(path):
                        os.makedirs(path)

                    with open(fname, 'wb') as fd:
                        for chunk in response.iter_content(chunk_size=128):
                            fd.write(chunk)

                            # print(fname,'loaded')

            except requests.exceptions.HTTPError as err:
                raise LoaderError('HTTP error: {0}'.format(err.response.status_code))

            except requests.exceptions.ConnectTimeout:
                raise LoaderError('Connection timeout')

            except requests.exceptions.ReadTimeout:
                raise LoaderError('Read timeout')

            except requests.exceptions.ConnectionError:
                raise LoaderError('Connection error')

            except:
                raise LoaderError('Unknown error in loader')

            else:
                if filename == 'index.html':
                    c = response.cookies.get_dict()
                    if len(c) > 0:
                        with open(Setting.base_dir + 'index.cookie', 'w') as fd:
                            for item in c:
                                # print(item,c[item])
                                fd.write(item + ':' + c[item] + '\n')

                response.encoding='UTF-8'
                return response.text

    def _send(self, host, port, data)->bytes:
        recv=''
        sock = socket.create_connection((host, port), 10)
        try:
            sock.sendall(data.encode())
            recvdata = sock.recv(8192)
            recv = recvdata
            while recvdata:
                recvdata = sock.recv(8192)
                recv += recvdata
        finally:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            sock.close()
        return recv


    def trick_load(self, url:URL, fname: str = '', overwrite=True, trick_name=None)->str:
        if trick_name is None:
            return ''

        if overwrite or (not os.path.exists(fname)):
            us = urlsplit(url.get())
            hostname = us[1]
            addr = socket.gethostbyname(hostname)

            if us[2] is not '':
                uri = us[2]
            else:
                uri = '/'

            if us[3] is not '':
                uri += '?' + us[3]

            try:
                result = self._send(addr, 80, AZLoader.trick_headers[trick_name].format( uri, hostname))

            except Exception as e:
                raise LoaderError(e.__repr__())
            else:
                (head,sp,body)=result.partition(b'\r\n\r\n')

                # print(head)
                # print(len(body))

                if fname is not '':
                    path = os.path.dirname(fname)

                    if not os.path.exists(path):
                        os.makedirs(path)

                    buf=BytesIO(body)
                    with open(fname, 'wb') as fd:
                        chunk=buf.read(256)
                        while len(chunk)>0:
                            fd.write(chunk)
                            chunk=buf.read(256)
                return body.decode(encoding='UTF-8',errors='ignore')

    def read_proxy_pac(self):
        if AZLoader.last_loaded:
            if datetime.datetime.now()-AZLoader.last_loaded<datetime.timedelta(hours=2):
                return
        try:
            pac=self.requests_load(URL(AZLoader.pac_url + '*'))
            r = re.search('\"PROXY (.*); DIRECT', pac)
            if r:
                AZLoader.free_http_proxy = r.group(1)
                p = re.findall("\"(.*?)\",", pac)

                AZLoader.proxy_domains = list()
                for item in p:
                    AZLoader.proxy_domains.append(item)

                AZLoader.proxies={'http': AZLoader.free_http_proxy}
                AZLoader.last_loaded=datetime.datetime.now()

        except LoaderError:
            print('AZLoader error:',AZLoader.pac_url,'not loaded')

    def read_config(self):
        try:
            with open(AZLoader.config_filename) as config:
                data = json.load(config)
                # print(data)
                # self.pac_url=data['pac_url']
                AZLoader.free_http_proxy=data.get('free_http_proxy',None)
                AZLoader.last_loaded=datetime.datetime.fromtimestamp(data.get('last_loaded'),None)
                AZLoader.proxy_domains=data.get('proxy_domains',list())
                if AZLoader.free_http_proxy:
                    AZLoader.proxies = {'http': AZLoader.free_http_proxy}

        except EnvironmentError as err:
            print('Read '+AZLoader.config_filename+' error: ',err)
        except (TypeError, ValueError):
            print('AZLoader config error, using default')
            AZLoader.pac_url = "http://antizapret.prostovpn.org/proxy.pac"
            AZLoader.last_loaded=None

    def write_config(self):
        try:
            os.replace(AZLoader.config_filename, AZLoader.config_filename + '.old')
        except EnvironmentError as err:
            print('Writing ' + AZLoader.config_filename + ' error: ', err)

        try:
            with open(self.config_filename, 'w') as config:
                print('Writing AZLoader config to '+AZLoader.config_filename)

                data=dict()
                # data['pac_url']=self.pac_url
                data['free_http_proxy']=AZLoader.free_http_proxy
                data['last_loaded']=AZLoader.last_loaded.timestamp()
                data['proxy_domains']=AZLoader.proxy_domains

                json.dump(data,config)
                # print(json.dumps(data))
        except EnvironmentError as err:
            print('Writing '+AZLoader.config_filename+' error: ',err)

if __name__ == "__main__":

    az=AZLoader()
    time = datetime.datetime.now()
    print('starting')
    print('result:', az._inspect_availability(URL('http://motherless.com/videos/recent?page=1*',test_string='MOTHERLESS.COM')))
    # print(az.inspect_availability(URL('http://motherless.com/videos/recent?page=1')))


    # print(az.trick_load(URL('http://cdn4.images.motherlessmedia.com/images/55FCE1C.jpg*'),fname='xutil/out/az.jpg',overwrite=False, trick_name='cr_method'))
    print(datetime.datetime.now()-time)
    exit()


    print('starting')


    print(az.test_url_az(URL('http://amotherless.com/videos/recent?page=1')))
    print(az.test_url_az(URL('http://motherless.com/videos/recent?page=1')))
    print(az.test_url_az(URL('http://a.motherless.com/videos/recent?page=1')))






    from bs4 import BeautifulSoup

    url1 = 'http://motherless.com/videos/recent?page=1'
    url1a = 'http://www.pornhub.com/'
    url1b = 'http://yourporn.sexy/'
    url2= 'http://google.com'
    url3='http://scs.spb.ru'

    url_jpeg='http://c2.trafficdeposit.com/bvideo/dOGa0-piG0qiYhDQhdjreQ/1487417906/58164a71a4195/58a7ec2224f03.mp4'

    fname1 = 'xutil/out/plain.html'
    fname2 = 'xutil/out/az.html'

    fname1_jpeg='xutil/out/plain.mp4'
    fname2_jpeg='xutil/out/az.jpg'

    url=url_jpeg
    f1=fname1_jpeg
    f2=fname2

    # metod=sp_method
    # metod=cr_method
    # metod=tab_method
    # metod=point_method
    # metod=host_method
    # metod=unix_method
    # metod=order_method



    # r=az.requests_load(URL(url,forced_proxy=True),f1)

    # print(r.history)
    #
    # for item in r.headers:
    #     print(item, ':', r.headers[item])
    #
    # print('========request========')
    # for item in r.request.headers:
    #     print(item, ':', r.request.headers[item])
    #
    #
    # with open(fname1,encoding='UTF-8',errors='ignore') as fs:
    #     bs=BeautifulSoup(fs,'html.parser')
    #     print('=======plain=========')
    #     if bs.head is not None:
    #         if bs.head.title is not None:
    #             print(bs.head.title.string)
    #     print('======================================================')

    # # load2(url,f2)
    # load3(url,f2, az_method=metod)
    #
    # with open(fname2,encoding='UTF-8',errors='ignore') as fs:
    #     bs=BeautifulSoup(fs,'html.parser')
    #     print('========az========')
    #     if bs.head is not None:
    #         if bs.head.title is not None:
    #             print(bs.head.title.string)
    #
    #     print('================')








    #
    # print(datetime.datetime.now() - time)
    #
    # az.write_config()