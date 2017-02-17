# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

if __name__ == "__main__":
    from turtle import *

    color('red', 'yellow')
    begin_fill()
    while True:
        forward(200)
        left(125)
        if abs(pos()) < 1:
            break
    end_fill()
    done()