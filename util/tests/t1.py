# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://www.veronicca.com/videos?o=mr")
bsObj = BeautifulSoup(html.read(),'lxml')
x=bsObj.find_all('div',{'class':'well well-sm hover'})

for item in x:

    print(item.a.attrs['href'])
    print(item.a.img.attrs['alt'])
    print(item.a.img.attrs['src'])
    print('=========================================================')

print(len(x))