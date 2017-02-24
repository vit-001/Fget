# -*- coding: utf-8 -*-
__author__ = 'Vit'

import os

import requests

from loader.old.az_loader import LoaderError
from setting import Setting

def safe_load(url, fname:str, overwrite=True):
    try:
        load(url, fname, overwrite)
        return fname
    except (ValueError, LoaderError) as Error:
        print(url.get() + ' not loaded: ', Error)
        return None

def load(url, fname:str='', overwrite=True, cookie=None):
    # print('Loading',url.get(),'to',fname)
    filename = ''

    if overwrite or (not os.path.exists(fname)):
        try:
            if url.method == 'GET':
                response = requests.get(url, cookies=cookie)
            elif url.method == 'POST':
                response = requests.post(url, data=url.post_data)
            else:
                raise LoaderError('Unknown method:' + url.method)

            response.raise_for_status()

            if fname is not '':
                path = os.path.dirname(fname)
                filename = os.path.split(fname)[1]

                if not os.path.exists(path):
                    os.makedirs(path)

                with open(fname, 'wb') as fd:
                    for chunk in response.iter_content(chunk_size=128):
                        fd.write(chunk)

                        # print(fname,'loaded')

        except requests.exceptions.HTTPError as err:  # todo Тестировать сообщения об ошибках
            raise LoaderError('HTTP error: {0}'.format(err.response.status_code))

        except requests.exceptions.ConnectTimeout:
            raise LoaderError('Connection timeout')

        except requests.exceptions.ReadTimeout:
            raise LoaderError('Read timeout')

        except requests.exceptions.ConnectionError:
            raise LoaderError('Connection error')

        except:
            raise LoaderError('Unknown error in loader')

        else:
            if filename == 'index.html':
                c = response.cookies.get_dict()
                if len(c) > 0:
                    with open(Setting.base_dir + 'index.cookie', 'w') as fd:
                        for item in c:
                            # print(item,c[item])
                            fd.write(item + ':' + c[item] + '\n')

            return response

def get_last_index_cookie():
    cookie = dict()
    print('Getting cookie')
    with open(Setting.base_dir + 'index.cookie', 'r') as fd:
        for line in fd:
            split = line.strip().partition(':')
            cookie[split[0]] = split[2]
    return cookie


if __name__ == "__main__":
    pass
