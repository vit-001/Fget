# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from setting import Setting
import os.path
import json
import requests
import re
import fnmatch
import datetime


from base_classes import URL

class LoaderError(RuntimeError):
    def __init__(self, txt):
        self.txt = txt

    def __str__(self):
        return self.txt

class AZLoader():
    def __init__(self):
        # restore configuration
        self.config_filename=Setting.base_dir+'az.json'
        self.read_config()

        # free proxy configuration
        self.pac_url = "http://antizapret.prostovpn.org/proxy.pac"
        self.proxy_domains=list()
        self.proxy_domains_cache=list()
        self.read_proxy_pac()

    def read_proxy_pac(self):
        try:
            pac=self.load(URL(self.pac_url+'*'))
            r = re.search('\"PROXY (.*); DIRECT', pac.text)
            if r:
                self.free_http_proxy = r.group(1)
                p = map(lambda x: x.replace("\Z(?ms)", "").replace("\\", ""), map(fnmatch.translate, re.findall("\"(.*?)\",", pac.text)))
                for item in p:
                    self.proxy_domains.append(item)
        except LoaderError:
            print('AZLoader error:',self.pac_url,'not loaded')

    def test_url_az(self, url:URL)->bool:
        domain=url.domain()
        for item in self.proxy_domains:
            if item in domain:
                return True
        return False


    def load(self, url:URL, fname: str = '', overwrite=True, cookie=None):
        # print('Loading',url.get(),'to',fname)
        filename = ''

        if overwrite or (not os.path.exists(fname)):
            try:
                if url.method == 'GET':
                    response = requests.get(url, cookies=cookie)
                elif url.method == 'POST':
                    response = requests.post(url, data=url.post_data)
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

            except requests.exceptions.HTTPError as err:  # todo Тестировать сообщения об ошибках
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

                return response

    def read_config(self):
        try:
            with open(self.config_filename) as config:
                data = json.load(config)
                print(data)
                # self.pac_url=data['pac_url']
                self.free_http_proxy=data.get('free_http_proxy',None)

        except EnvironmentError as err:
            print('Read '+self.config_filename+' error: ',err)

    def write_config(self):
        try:
            os.replace(self.config_filename, self.config_filename + '.old')
        except EnvironmentError as err:
            print('Writing ' + self.config_filename + ' error: ', err)

        try:
            with open(self.config_filename, 'w') as config:
                print('Writing AZLoader config to '+self.config_filename)

                data=dict()
                # data['pac_url']=self.pac_url
                data['free_http_proxy']=self.free_http_proxy

                json.dump(data,config)
                print(json.dumps(data))
        except EnvironmentError as err:
            print('Writing '+self.config_filename+' error: ',err)

if __name__ == "__main__":
    az=AZLoader()

    time = datetime.datetime.now()

    print('starting')

    print(az.test_url_az(URL('http://www.motherless.com/videos/recent?page=1*')))

    print(datetime.datetime.now() - time)
    print(az.test_url_az(URL('http://www.motherlesss.com/videos/recent?page=1*')))

    print(datetime.datetime.now() - time)

    az.write_config()