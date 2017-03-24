# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

class A:
    def b(self, s, z=1):
        print(s, z)




def f(func, *args, **options):
    aa = A()
    aa.__getattribute__('b')(*args, **options)
    # aa.__dict__.get('b')(*args, **options)



a=A()
a.b(1,2)

# print(A.__dict__.get('b'))

f('b',5,3)
