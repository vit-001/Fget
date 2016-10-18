__author__ = 'Nikitin'

from tkinter import *
from tkinter.ttk import *


class StatusBar(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(side=BOTTOM, fill=X)

        self._left = Label(self, width=10, relief=RIDGE)
        self._right = Label(self, width=10, relief=RIDGE)
        self._center = Label(self, width=40, relief=RIDGE, anchor=W)

        self._left.grid(row=0, column=0, sticky=EW)
        self._right.grid(row=0, column=2, sticky=EW)
        self._center.grid(row=0, column=1, sticky=EW)

        self.columnconfigure(1, weight=8)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

    def left(self, txt=''):
        self._left.config(text=txt)

    def right(self, txt=''):
        self._right.config(text=txt)

    def center(self, txt=''):
        self._center.config(text=txt)