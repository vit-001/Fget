__author__ = 'Vit'
from urllib.request import urlretrieve
from urllib.error import HTTPError

if __name__ == "__main__":

    print('loading...')
    try:
        urlretrieve("http://www.deviantclip.com/watch/mega-tits-bbw-dildoing-in-the-car-jjjaa", 'e:/out/2.html')
        print('1')
        #urlretrieve("http://cdn3.bdsmstreak.com/26397.mp4", 'e:/out/1.mp4')
    except HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')

