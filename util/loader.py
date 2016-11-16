__author__ = 'Vit'
from urllib.request import urlretrieve
from urllib.error import HTTPError

if __name__ == "__main__":

    print('loading...')
    try:
        urlretrieve("http://www.porndreamer.com/videos/172519/jobless-woman-licks-on-dudes-ass-while-doing-a-handjob/", 'e:/out/1.html')
        print('1')
        # urlretrieve("http://cds.t4m5e9q7.hwcdn.net/contents/videos_screenshots/129000/129150/300x225/2.jpg", 'e:/out/1.jpg')
    except HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')

