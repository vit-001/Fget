__author__ = 'Vit'
from urllib.request import urlretrieve
from urllib.error import HTTPError

if __name__ == "__main__":

    print('loading...')
    try:
        urlretrieve("https://static-eu-cdn.eporner.com/vjs/vjs.js?cache=20160926", 'e:/out/1.js')
        print('1')
        # urlretrieve("http://cds.t4m5e9q7.hwcdn.net/contents/videos_screenshots/129000/129150/300x225/2.jpg", 'e:/out/1.jpg')
    except HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')

