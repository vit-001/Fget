# -*- coding: utf-8 -*-
__author__ = 'Vit'
import requests
import requests.exceptions
import socket
from urllib.parse import urlparse,urlsplit


def load(url, fname, cookies=None, headers=None):
    print('Loading', url, 'to', fname)
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        with open(fname, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)



    except requests.exceptions.HTTPError as err:  # todo Тестировать сообщения об ошибках
        print('HTTP error: {0}'.format(err.response.status_code))
        return response

    except requests.exceptions.ConnectTimeout:
        print('Connection timeout')

    except requests.exceptions.ReadTimeout:
        print('Read timeout')

    except requests.exceptions.ConnectionError:
        print('Connection error')

    except:
        print('Unknown error in loader')
    else:
        print('loaded ok!')
        return response

def _dpi_send(host, port, data, fragment_size=0, fragment_count=0):
    sock = socket.create_connection((host, port), 10)
    if fragment_count:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
    try:
        for fragment in range(fragment_count):
            sock.sendall(data[:fragment_size].encode())
            data = data[fragment_size:]
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
    return recv#.decode(errors='replace')

def _dpi_build_tests(host, urn, ip):
    dpi_built_list = {
            # 'дополнительный пробел после GET':
            #     {'data': "GET  {} HTTP/1.0\r\n".format(urn) + \
            #             "Host: {}\r\nConnection: close\r\n\r\n".format(host),
            #     'lookfor': lookfor, 'ip': ip,
            #     'fragment_size': 0, 'fragment_count': 0},
            'перенос строки перед GET':
                {'data': "\nGET {} HTTP/1.0\r\n".format(urn) + \
                        "Host: {}\r\nConnection: close\r\n\r\n".format(host),
                 'ip': ip,
                'fragment_size': 0, 'fragment_count': 0},
            # 'табуляция в конце домена':
            #     {'data': "GET {} HTTP/1.0\r\n".format(urn) + \
            #             "Host: {}\t\r\nConnection: close\r\n\r\n".format(host),
            #     'lookfor': lookfor, 'ip': ip,
            #     'fragment_size': 0, 'fragment_count': 0},
            # 'фрагментирование заголовка':
            #     {'data': "GET {} HTTP/1.0\r\n".format(urn) + \
            #             "Host: {}\r\nConnection: close\r\n\r\n".format(host),
            #     'lookfor': lookfor, 'ip': ip,
            #     'fragment_size': 2, 'fragment_count': 6},
            # 'точка в конце домена':
            #     {'data': "GET {} HTTP/1.0\r\n".format(urn) + \
            #             "Host: {}.\r\nConnection: close\r\n\r\n".format(host),
            #     'lookfor': lookfor, 'ip': ip,
            #     'fragment_size': 0, 'fragment_count': 0},
            # 'заголовок host вместо Host':
            #     {'data': "GET {} HTTP/1.0\r\n".format(urn) + \
            #             "host: {}\r\nConnection: close\r\n\r\n".format(host),
            #     'lookfor': lookfor, 'ip': ip,
            #     'fragment_size': 0, 'fragment_count': 0},
            # 'перенос строки в заголовках в UNIX-стиле':
            #     {'data': "GET {} HTTP/1.0\n".format(urn) + \
            #             "Host: {}\nConnection: close\n\n".format(host),
            #     'lookfor': lookfor, 'ip': ip,
            #     'fragment_size': 0, 'fragment_count': 0},
            # 'необычный порядок заголовков':
            #     {'data': "GET {} HTTP/1.0\r\n".format(urn) + \
            #             "Connection: close\r\nHost: {}\r\n\r\n".format(host),
            #     'lookfor': lookfor, 'ip': ip,
            #     'fragment_size': 0, 'fragment_count': 0},
        }
    return dpi_built_list


def load2(url, fname):

    us=urlsplit(url)

    # print(us)



    hostname = us[1]
    addr = socket.gethostbyname(hostname)


    if us[2] is not '':
        urn=us[2]
    else:
        urn='/'

    if us[3] is not '':
        urn+='?'+us[3]
    print('The address of ', hostname, 'is', addr)


    site = {'host': us[1], 'urn': urn,
                    'ip': addr}
    # print(site)

    dpi_built_tests = _dpi_build_tests(site['host'], site['urn'], site['ip'])
    # print(dpi_built_tests)
    for testname in dpi_built_tests:
        test = dpi_built_tests[testname]
        # print("\tПробуем способ «{}» на {}".format(testname, us[1]))
        try:
            result = _dpi_send(test.get('ip'), 80, test.get('data'), test.get('fragment_size'), test.get('fragment_count'))
        except Exception as e:
            print("[☠] Ошибка:", repr(e))
        else:
            print('AZ loaded ok')
            with open(fname, 'w+b') as fd:
                fd.write(result)
    return


if __name__ == "__main__":

    from bs4 import BeautifulSoup

    url1 = 'http://motherless.com/videos/recent?page=1?xxx=1'
    url1a = 'http://www.pornhub.com/'
    url2= 'http://google.com'
    url3='http://scs.spb.ru'

    fname1 = 'out/plain.html'
    fname2 = 'out/az.html'

    url=url1a

    r=load(url,fname1)

    load2(url,fname2)

    print(r.history)

    for item in r.headers:
        print(item, ':', r.headers[item])

    print('========request========')
    for item in r.request.headers:
        print(item, ':', r.request.headers[item])


    with open(fname1,encoding='UTF-8',errors='ignore') as fs:
        bs=BeautifulSoup(fs,'html.parser')
        print('=======plain=========')
        print(bs.head.title.string)
        print('================')

    with open(fname2,encoding='UTF-8',errors='ignore') as fs:
        bs=BeautifulSoup(fs,'html.parser')
        print('========az========')
        print(bs.head.title.string)
        print('================')

