# -*- coding: utf-8 -*-
from urllib import parse as up
from urllib.parse import urlparse

__author__ = 'Vit'

if __name__ == "__main__":
    pass

def get_href( txt:str, base_url):
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

class URL:
    SUFFIXES = ['.html', '.jpg', '.gif', '.JPG', '.mp4', '.flv', 'png']

    def __init__(self,
                 url='',
                 method='GET',
                 base_url=None,

                 coockies=None,
                 user_agent=None,
                 referer=None,
                 post_data=None,
                 any_data=None,

                 forced_proxy=False,
                 forced_unproxy=False
                 ):

        self.method = method
        self.coockies = coockies
        self.user_agent=user_agent
        self.referer=referer
        self.post_data = post_data
        self.xhr_data = any_data
        self.forced_proxy=forced_proxy
        self.forced_unproxy=forced_unproxy

        if base_url:
            url=get_href(url,base_url)

        if url == '':
            self.url = ''
            self.no_slash = True
            return

        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url

        self.no_slash = url.endswith('*')
        self.url = url.rstrip('*')

    def get(self):
        if self.url is '': return self.url
        for suffix in URL.SUFFIXES:
            if self.url.endswith(suffix): return self.url
        if self.no_slash:
            return self.url.rstrip('/')
        return self.url.rstrip('/') + '/'

    def get_short_path(self, base=''):
        p = urlparse(self.get())
        return base.rstrip('/') + '/' + p[1] + '/' + p[2].strip(' /').replace('/', '..')

    def get_path(self, base=''):
        p = urlparse(self.get())
        p2 = p[2]
        if p2.endswith('.html') or p2.endswith('.jpg'):
            p2 = p2.rpartition('/')[0] + '/'
        return base.rstrip('/') + '/' + p[1] + p2.rstrip('/') + '/'

    def domain(self):
        p = urlparse(self.get())
        return p[1]

    def contain(self, text=''):
        return text in self.url

    def add_query(self, pair_list):
        split = up.urlsplit(self.url)
        qs = up.parse_qs(split[3]).keys()
        qsl = up.parse_qsl(split[3])

        added = set()
        for (add_name, add_value) in pair_list:
            if add_name not in qs:
                added.add(add_name)

        new_qsl = list()
        for (name, value) in qsl:
            for (add_name, add_value) in pair_list:
                if add_name == name:
                    value = add_value
            new_qsl.append(tuple([name, value]))
        for (add_name, add_value) in pair_list:
            if add_name in added:
                new_qsl.append(tuple([add_name, add_value]))

        new_query = up.urlencode(new_qsl)
        self.url = up.urlunsplit(
            up.SplitResult(scheme=split[0], netloc=split[1], path=split[2], query=new_query, fragment=split[4]))

    def to_save(self):
        if self.no_slash:
            return self.get() + '*'
        else:
            return self.get()

    def __repr__(self, *args, **kwargs):
        return self.get()

    def __str__(self, *args, **kwargs):
        return self.__repr__()

    def __eq__(self, url2):
        # print('Compare', self,url2)
        if url2 is None:
            return False
        if self.method != url2.method:
            return False
        if self.method == 'GET':
            return url2.to_save() == self.to_save()
        elif self.method == 'POST':
            if url2.to_save() != self.to_save():
                return False
            if self.post_data is None:
                return url2.post_data is None
            if url2.post_data is None:
                return False
            for key in self.post_data:
                if self.post_data[key] != url2.post_data[key]:
                    return False
            for key in url2.post_data:
                if self.post_data[key] != url2.post_data[key]:
                    return False
            return True
        return False


