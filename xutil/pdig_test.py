# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

import json

import xutil.loader_get as lg
import xutil.loader_post as lp

dir = 'e:/out/pdig/'

lg.load('https://www.porndig.com/video/', dir + 'index.html')

# 'main_category_id':'1',
# 'type':'post',
# 'name':'all_videos',
# 'filters[filter_type]':'ctr',
# 'filters[filter_period]':'month',
# 'offset':'100'

data = {'main_category_id': '1',
        'type': 'post',
        'name': 'all_videos',
        # 'filters[filter_type]': 'ctr',
        # 'filters[filter_period]': 'month',
        'offset': '100'}

r = lp.load('https://www.porndig.com/posts/load_more_posts', dir + 'post100.bin.html', data=data)
with open(dir + 'post100.bin.html') as inp:
    with open(dir + 'post100.json', 'w') as fd:
        for line in inp:
            # print(line)

            # l = line.replace('\\/', '/').replace('\\"','"')
            fd.write(line)

with open(dir + 'post100.json') as fd:
    j = json.load(fd)

for item in j:
    print(item)
print('========')
for item in j['data']:
    print(item)
print('========')

print(j['message'])

success = j.get('success', False)
if success:
    data = j['data']

    content = data['content']
    # print(content)
    if len(content) > 0:
        has_more = data['has_more']

        print(len(content))
        print(has_more)

        with open(dir + 'post100.html', 'w') as fd:
            fd.write(content)
