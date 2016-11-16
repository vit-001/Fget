__author__ = 'Vit'
from urllib.request import urlretrieve
from urllib.error import HTTPError

if __name__ == "__main__":

    print('loading...')
    try:
        urlretrieve("http://static1.eu.cdn.eporner.com/ajax.js?cache=20161115", 'e:/out/3.html')
        print('1')
        # urlretrieve("http://cds.t4m5e9q7.hwcdn.net/contents/videos_screenshots/129000/129150/300x225/2.jpg", 'e:/out/1.jpg')
    except HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')

