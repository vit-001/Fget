# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from base_classes import URL

def get_href(txt='', base_url=URL()):
    txt = txt.strip()
    if not txt.endswith('/'):
        txt = txt + "*"
    if txt.startswith('http://'):
        return txt
    if txt.startswith('/'):
        return base_url.domain() + txt
    # print(base_url.get() + txt)
    return base_url.get().rpartition('/')[0] + '/' + txt

decode_table=dict()
decode_table['%3A']=':'
decode_table['%2F']='/'
decode_table['%3F']='?'
decode_table['%3D']='='
decode_table['%26']='&'

def decode_text(txt=''):
    for key in decode_table:
        txt=txt.replace(key,decode_table[key])
    return txt

if __name__ == "__main__":
    pass