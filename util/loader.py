__author__ = 'Vit'
from urllib.request import urlretrieve
from urllib.error import HTTPError

if __name__ == "__main__":

    print('loading...')
    try:
        # urlretrieve("http://www.xvideos.com/video16684795/his_gift_is_two_girlfriends", 'e:/out/1.html')
        print('1')
        urlretrieve("http://videos4.cdn.xvideos.com/videos/mp4/5/c/8/xvideos.com_5c8bb759d09860dc2127e13ef6649760-1.mp4?e=1478776343&ri=1024&rs=85&h=3b90479e23feb08763070ae4d9bfe4dc", 'e:/out/1.mp4')
    except HTTPError as err:
        print(err)
        print(err.headers)
    else:
        print('loaded ok.')

