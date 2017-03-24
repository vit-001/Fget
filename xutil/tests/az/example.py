# -*- coding: utf-8 -*-

from urllib.request import build_opener,install_opener,Request,urlopen

from bs4 import BeautifulSoup

from xutil.tests.az.antizapret import AntizapretProxyHandler

install_opener(build_opener(AntizapretProxyHandler()))

req = Request("http://motherless.com/videos/recent?page=1")
response = urlopen(req)
data = response.read()

bs=BeautifulSoup(data)

print(bs.prettify())