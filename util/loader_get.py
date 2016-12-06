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

        url1='http://www.pornhd4k.com/channels/virgin-russian-girl-with-a-slender-body-loves-buttfucked.html'
        url1a = 'http://porndoe.com/video/543033/jacquelyn-gets-fucked-from-behind-with-her-socks-on'
        url2='https://storage.googleapis.com/mypocket-99.appspot.com/kink/20_04_2016_All_Natural_19_Year_Old_Girl_Next_Door_is_Machine_Fucked_Like_a_Whore.mp4'
        url3='http://www.drtuber.com/player_config/?h=503093cfbeaa558180554133b2315358%26check_speed=1%26t=1480701894%26vkey=676d54293b2629388734&project_name=drtuber&id=player&javascriptid=player&enablejs=true'

        fname1 = 'e:/out/1.html'
        fname1a = 'e:/out/1a.html'
        fname2 = 'e:/out/1.mp4'
        fname3 = 'e:/out/3.json'
        fname4 = 'e:/out/1.js'

        # coockies={'_gat':'1',
        # '_ga' :'GA1.2.1045758528.1480589656'}

        # headers={'Referer':'http://www.daporn.com/'}


        r=load(url1,fname1)
        # r = load(url1a, fname1a)
        # r = load(url2, fname2)

        for item in r.headers:
            print(item,':',r.headers[item])

        print('========request========')
        for item in r.request.headers:
            print(item,':',r.request.headers[item])



