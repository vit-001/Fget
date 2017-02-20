# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

if __name__ == "__main__":

    import io

    myString="""1
2
3
"""

    s = io.StringIO(myString)
    for line in s:
        print(line, end='')
