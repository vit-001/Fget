# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from base_classes import URL

def get_href( txt:str, base_url:URL):
    txt = txt.strip()
    if not txt.endswith('/'):
        txt = txt + "*"
    if txt.startswith('http://'):
        return txt
    if txt.startswith('//'):
        return 'http:' + txt
    if txt.startswith('https://'):
        return txt
    if txt.startswith('/'):
        return 'http://' + base_url.domain() + txt
    # print(base_url.get() + txt)
    return base_url.get().rpartition('/')[0] + '/' + txt

def get_url(txt:str, base_url:URL):
    return URL(get_href(txt,base_url))

def quotes(text:str, from_lex:str, to_lex:str):
    return text.partition(from_lex)[2].partition(to_lex)[0]


def sp():
    print('=========================================')

def psp(s:str):
    print(s)
    sp()

decode_table = dict()
decode_table['%3A'] = ':'
decode_table['%2F'] = '/'
decode_table['%3F'] = '?'
decode_table['%3D'] = '='
decode_table['%26'] = '&'


def decode_text(txt=''):
    for key in decode_table:
        txt = txt.replace(key, decode_table[key])
    return txt


if __name__ == "__main__":
    pass
