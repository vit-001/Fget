# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from multiprocessing import Process, Lock, Manager, freeze_support

def wait(i):
    x=0
    for k in range(i):
        x+=k
    return x

class DataServer:
    def __init__(self):
        self.manager=Manager()
        self.data = self.manager.dict()

        self.data['list']=[]
        self.data['count']=list([0 for i in range(10)])

    def get_data(self):
        return self.data

    def stop(self):
        self.manager.shutdown()

class AZ:
    def __init__(self, i):

        self.i=i

    def set_data(self, data):
        self.data=data

    def prnt(self, iter):

        lst=self.data['list']
        lst.append('a')
        self.data['list']=lst

        count=self.data['count']
        count[self.i]+=1
        self.data['count']=count

        print('process',self.i , 'iteration',iter, self.data['count'], self.data['list'])


class Server(Process):
    def __init__(self, i, data_server, lock):
        self.data=data_server.get_data()
        self.a=AZ(i)
        print('init process', i)
        self.lock=lock
        Process.__init__(self)

    def run(self):
        self.a.set_data(self.data)
        for iter in range(5):
            self.lock.acquire()
            self.a.prnt(iter)
            self.lock.release()
            wait(500000)


class Thread():
    def start(self, i,data_server, lock):
        self.server=Server(i, data_server, lock)
        self.server.daemon=True
        self.server.start()

if __name__ == '__main__':
    import time


    ds=DataServer()


    l=Lock()

    for num in range(10):
        wait(200000)
        Thread().start(num,ds,l)


    time.sleep(10)


    # print(ds.data)
    print(len(ds.data['list']))
    ds.stop()