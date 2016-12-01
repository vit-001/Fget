# -*- coding: utf-8 -*-
__author__ = 'Vit'

if __name__ == "__main__":
    import requests
    import urllib.error

    try:
        headers = {'user-agent': 'my-app/0.0.1'}
        url='http://toseeporn.com/Movie/vika-lisichkina-hardcode-defloration-416/'

        response = requests.get('http://toseeporn.com/Movie/vika-lisichkina-hardcode-defloration-416/')
        print(response.text)
        print(response.url)
    except urllib.error.HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')