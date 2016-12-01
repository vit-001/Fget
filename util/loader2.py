# -*- coding: utf-8 -*-
__author__ = 'Vit'
import requests
import requests.exceptions


def load(url, fname):
    print('Loading',url,'to',fname)
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(fname, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)



    except requests.exceptions.HTTPError as err: #todo Тестировать сообщения об ошибках
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

        url1='http://toseeporn.com/Movie/jessica-mazury-hardcore-2-defloration-1596'

        url3='http://toseeporn.com/Media/GetMediaSource?movieId=2&Eposide=0'
        url2='http://statics.toseeporn.com/toseeporn.com-Vika-Lisichkina-Hardcode-Defloration-416_tb.jpg'

        fname1 = 'e:/out/1.html'
        fname2 = 'e:/out/1.jpg'
        fname3 = 'e:/out/3.json'

        r=load(url3,fname3)

        for item in r.json()['mediaSources']:
            print(item)



