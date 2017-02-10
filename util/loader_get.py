# -*- coding: utf-8 -*-
__author__ = 'Vit'
import requests
import requests.exceptions


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


if __name__ == "__main__":

    url1 = 'http://www.realgfporn.com/most-recent/'
    url1a = 'https://videos.porndig.com/player/index/174087/1035/13798'
    url2 = 'http://www.realgfporn.com/videos/stepsister-riding-cock-and-getting-creampied-125995.html'
    url3 = 'http://www.drtuber.com/player_config/?h=503093cfbeaa558180554133b2315358%26check_speed=1%26t=1480701894%26vkey=676d54293b2629388734&project_name=drtuber&id=player&javascriptid=player&enablejs=true'

    fname1 = 'out/1.html'
    fname1a = 'out/1a.html'
    fname1b = 'out/1b.html'
    fname1c = 'out/1.html'
    fname2 = 'out/1.mp4'
    fname2a = 'out/2.html'
    fname3 = 'out/3.json'
    fname4 = 'out/1.js'

    # coockies={'_gat':'1',
    # '_ga' :'GA1.2.1045758528.1480589656'}

    headers = {'Referer': 'http://her69.net/massagerooms-daphne-angel-daisy-lee/'}

    # r=load(url1,fname1)
    r = load(url2, fname2a)
    # r = load(url1a, fname1a)
    # r = load(url1a, fname1a,headers=headers)
    # r = load(url2, fname2)

    # r=load('https://assets.porndig.com/assets/porndig/js/bundle.js?ver=1481122807','e:/out/bundle.js')

    for item in r.headers:
        print(item, ':', r.headers[item])

    print('========request========')
    for item in r.request.headers:
        print(item, ':', r.request.headers[item])
