# -*- coding: utf-8 -*-
__author__ = 'Vit'

from pathlib import Path

def line_count(fd):
    n=0
    for line in fd:
        n+=1

    return n


if __name__ == "__main__":
    n=0
    p=Path('.')
    list_files=list(p.glob('**/*.py'))
    for item in list_files:
        try:
            print(item, end=' ')
            with open(str(item.absolute())) as fd:
                i=line_count(fd)
                print(i)
                n+=i
        except UnicodeDecodeError:
            pass
    print(n)



