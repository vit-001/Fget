# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from multiprocessing import Process, Lock

def wait(i):
    x=0
    for k in range(i):
        x+=k
    return x

class A:

    n=0
    lock=Lock()

    def __init__(self, i):
        A.n+=1
        self.i=i
        print('init',i, A.n)

    def prnt(self, i):
        # A.lock.acquire()
        print('hello world ',self.n)
        wait(10000)
        print('               ', self.i)
        wait(10000)
        print('                          ', i)
        # A.lock.release()

class Server(Process):

    def __init__(self, i, lock):
        self.a=A(i)
        self.lock=lock
        print('init', i)
        Process.__init__(self)

    def run(self):
        for i in range(5):
            self.lock.acquire()
            self.a.prnt(i)
            self.lock.release()

class Thread():
    def start(self, i, lock):
        self.server=Server(i, lock)
        self.server.start()

if __name__ == '__main__':

    l=Lock()

    for num in range(5):
        wait(1500)
        Thread().start(num,l)

