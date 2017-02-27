# -*- coding: utf-8 -*-
__author__ = 'Vit'
import requests
import requests.exceptions


def load(url, fname, cookies=None, headers=None, proxies=None):
    print('Loading', url, 'to', fname)
    try:
        response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies)
        response.raise_for_status()
        with open(fname, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)



    except requests.exceptions.HTTPError as err:
        print('HTTP error: {0}'.format(err.response.status_code))
        # return response

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

    proxies={'http': 'proxy.antizapret.prostovpn.org:3128'}

    url1 = 'http://ru.xhamster.com/'
    url1a = 'http://www.pornhub.com/view_video.php?viewkey=ph58b2cd0bcd448'
    url2 = 'http://cdn2b.video.pornhub.phncdn.com/videos/201702/27/107746912/480P_600K_107746912.mp4?ip=163.172.173.40/8&rs=106&ri=1000&s=1488179361&e=1488186561&h=405881cd40941cf7d64938db638a204c'
    url3 = 'http://www.drtuber.com/player_config/?h=503093cfbeaa558180554133b2315358%26check_speed=1%26t=1480701894%26vkey=676d54293b2629388734&project_name=drtuber&id=player&javascriptid=player&enablejs=true'

    fname1 = 'out/1.html'
    fname1a = 'out/1a.html'
    fname1b = 'out/1b.html'
    fname1c = 'out/1.html'
    fname2 = 'out/1.mp4'
    fname2a = 'out/2.html'
    fname3 = 'out/3.json'
    fname4 = 'out/1.js'


    # coockies={'_gat':'1', 'protect':'BPJvGkuwOdy0D4amF44YTA', '_ga':'GA1.2.638382635.1487974825'}

    # headers = {'Referer': 'http://her69.net/massagerooms-daphne-angel-daisy-lee/'}

    # r=load(url2,fname2)#, proxies=proxies)
    # r = load(url2, fname2a)
    # r = load(url1a, fname1a, proxies=proxies)
    # r = load(url1a, fname1a,headers=headers)
    r = load(url2, fname2, proxies=proxies)

    # r=load('https://assets.porndig.com/assets/porndig/js/bundle.js?ver=1481122807','e:/out/bundle.js')

    for item in r.headers:
        print(item, ':', r.headers[item])

    print('========request========')
    for item in r.request.headers:
        print(item, ':', r.request.headers[item])
