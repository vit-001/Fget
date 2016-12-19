# -*- coding: utf-8 -*-
__author__ = 'Vit'

import urllib.parse as up

url='http://www.extremetube.com/videos?format=json&number_pages=1&page=2'

p=up.urlsplit(url)
print(p)

qs=p[3]
print(qs)

qp=up.parse_qs(qs)
print(qp)
print(up.urlencode(qp))


print(up.urlunsplit(p))

print(up.unquote(up.urlencode({'page': ['2'], 'format': ['json'], 'number_pages': ['1']})))

#http://www.extremetube.com/videos?format=%5B%27json%27%5D&number_pages=%5B%271%27%5D&page=%5B%272%27%5D