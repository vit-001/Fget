# -*- coding: utf-8 -*-
__author__ = 'Vit'
import requests
import requests.exceptions


def load(url, fname, cookies=None, headers=None):
    print('Loading',url,'to',fname)
    try:
        response = requests.get(url,cookies=cookies, headers=headers)
        response.raise_for_status()
        with open(fname, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)



    except requests.exceptions.HTTPError as err: #todo Тестировать сообщения об ошибках
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

        url1='https://www.veronicca.com/video/22/sexy-teen-dance'
        url1a = 'https://openload.co/embed/J8_8UK3Ge6A/Show_Me_How_You_Jerk_Off_-_Brazzers_-_Abbey_Brooks.mp4'
        url2='http://donfreeporn.com/ziej6ai.bid/88/47/27/8847279f86ec9c47f2baab3f51fa7b0a.js'
        url3='http://www.drtuber.com/player_config/?h=503093cfbeaa558180554133b2315358%26check_speed=1%26t=1480701894%26vkey=676d54293b2629388734&project_name=drtuber&id=player&javascriptid=player&enablejs=true'

        fname1 = 'e:/out/1.html'
        fname1a = 'e:/out/1a.html'
        fname1b = 'e:/out/1b.html'
        fname2 = 'e:/out/1.mp4'
        fname3 = 'e:/out/3.json'
        fname4 = 'e:/out/1.js'

        # coockies={'_gat':'1',
        # '_ga' :'GA1.2.1045758528.1480589656'}

        # headers={'Referer':'http://www.daporn.com/'}


        r=load(url1,fname1)
        # r = load(url1a, fname1a)
        # r = load(url2, fname1b)
        # r = load(url2, fname2)

        for item in r.headers:
            print(item,':',r.headers[item])

        print('========request========')
        for item in r.request.headers:
            print(item,':',r.request.headers[item])



