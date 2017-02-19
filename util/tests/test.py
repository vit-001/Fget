# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

if __name__ == "__main__":

    import datetime

    t=datetime.datetime.now()
    print(t)
    print(t.timestamp())

    ts=t.timestamp()

    t1=datetime.datetime.fromtimestamp(ts)

    print(t1)
