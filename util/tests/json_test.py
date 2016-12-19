# -*- coding: utf-8 -*-
__author__ = 'Vit'

import json

with open('e:/out/tsp_video.json') as fd:
    script = ''
    for line in fd:
        script += line

# print(script.replace(' ',''))

txt = '[{' + script.replace(' ', '').partition("sources:[{")[2].partition('}]')[0] + '}]'

print(txt)

a = json.loads(txt)

for item in a:
    print(item)

if __name__ == "__main__":
    pass
