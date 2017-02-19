# -*- coding: utf-8 -*-
__author__ = 'Vit'

class SingleTone(object):
    __instance = None
    def __new__(cls):
        if SingleTone.__instance is None:
            SingleTone.__instance = object.__new__(cls)
        return SingleTone.__instance


class Test(SingleTone):
    def __init__(self):
        self.x=1


    def set_x(self,x):
        self.x=x






if __name__ == "__main__":
    a=Test()
    b=Test()

    b.set_x(2)

    print(a.x)
    print(b.x)
