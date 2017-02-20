# -*- coding: utf-8 -*-
__author__ = 'Vit'

class A:

    a=1

    @staticmethod
    def sm1(x):
        A.a=x


    def m1(self,x):
        A.a=x

    def m2(self,x):
        A.sm1(x)


    def __str__(self):
        return str(A.a)


if __name__ == "__main__":
    a=A()
    print(a)
    a.sm1(2)
    print(a)
    a.m1(3)
    print(a)
    a.m2(4)
    print(a)
