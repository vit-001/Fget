__author__ = 'Vit'
from urllib.request import urlretrieve
from urllib.error import HTTPError

if __name__ == "__main__":

    print('loading...')
    try:
        urlretrieve("https://www.vporn.com/mature/horny-mom-enjoys-a-big-black-cock/1515126/?t=1/", 'e:/out/1.html')
        print('1')
        #urlretrieve("http://cdn3.bdsmstreak.com/26397.mp4", 'e:/out/1.mp4')
    except HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')

