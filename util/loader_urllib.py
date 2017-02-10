__author__ = 'Vit'
from urllib.error import HTTPError
from urllib.request import urlretrieve

if __name__ == "__main__":

    print('loading...')
    try:
        urlretrieve("http://toseeporn.com/Movie/vika-lisichkina-hardcode-defloration-416/", 'e:/out/1.html')
        print('1')
        # urlretrieve("http://mh.daporn.com/videos/5/8/2/6/9/58269ebcb3673_2.mp4", 'e:/out/1.mp4')
    except HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')
