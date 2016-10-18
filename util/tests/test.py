# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

if __name__ == "__main__":
    import sys
    print(sys.path)
    from model.data import Data
    d=Data
    print(d.__dict__)