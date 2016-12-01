# -*- coding: utf-8 -*-
__author__ = 'Vit'

if __name__ == "__main__":
    import requests
    import urllib.error
    from requests.exceptions import ConnectionError,ConnectTimeout

    try:
        # headers = {'user-agent': 'my-app/0.0.1'}
        url='http://toseeporn.com/Movie/vika-lisichkina-hardcode-defloration-416/'
        url1='http://statics.toseeporn.com/toseeporn.com-Vika-Lisichkina-Hardcode-Defloration-416_tb.jpg'

        fname = 'e:/out/1r.html'
        fname1 = 'e:/out/1.jpg'

        response = requests.get(url)

        # i=0
        #
        # for line in response.iter_lines():
        #     print(i,line)
        #     i+=1


        with open(fname, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

        print(response.raw)
        print(response.url)
    except urllib.error.HTTPError as err:
        print(err)
        print(err.headers)
    except (ConnectionError, ConnectTimeout) as err:
        print(err)
    else:
        print('loaded ok.')