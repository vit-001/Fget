__author__ = 'Vit'
from urllib.request import urlretrieve
from urllib.error import HTTPError

if __name__ == "__main__":

    print('loading...')
    try:
        urlretrieve("http://gobdsm.com/videos/two-beautiful-sex-slaves-experiences-lusty-and-wild-public/?pqr=13:2c8d63ec93028cf593fa06c9ab7db742:0:11420:1", 'e:/out/1.html')
        print('1')
        #urlretrieve("http://cdn3.bdsmstreak.com/26397.mp4", 'e:/out/1.mp4')
    except HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')

