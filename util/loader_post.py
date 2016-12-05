# -*- coding: utf-8 -*-
__author__ = 'Vit'
import requests
import requests.exceptions


def load(url, fname, data=None):
    print('Loading', url, 'to', fname)
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        with open(fname, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                print(chunk)
                fd.write(chunk)

    except requests.exceptions.HTTPError as err:  # todo Тестировать сообщения об ошибках
        print('HTTP error: {0}'.format(err.response.status_code))

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


if __name__ == "__main__":

    url1 = 'http://yourporn.sexy/php/get_vlink.php'

    url3 = 'http://toseeporn.com/Media/GetMediaSource?movieId=2&Eposide=0'
    url2 = 'http://statics.toseeporn.com/toseeporn.com-Vika-Lisichkina-Hardcode-Defloration-416_tb.jpg'

    fname1 = 'e:/out/1.html'
    fname1a = 'e:/out/1a.html'
    fname2 = 'e:/out/1.jpg'
    fname3 = 'e:/out/3.json'

    data = {'uid':"5a8bac8670e6a662b959bb3a1979aa40", 'source':'blog', 'hash':'57bcce3d85ef5', 'x':'s9', 'oid':'5669adbda0e41', 'pid':'57bcce3d85ef5'}

    r = load(url1, fname1a, data=data)

    for item in r.headers:
        print(item, ':', r.headers[item])

    def json_chipper(txt=''):
        t1=txt.replace('\\"',"\0")
        t2=t1.partition('"content":"')[2].partition('"')[0]
        return t2.replace('\\/','/').replace('\0','"').replace('>','>\n')

    print(r.text)

    with open(fname1a, 'w') as fd:
        fd.write(json_chipper(r.text))

