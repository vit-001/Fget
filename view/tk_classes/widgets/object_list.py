__author__ = 'Vit'

from tkinter import *
from tkinter.ttk import *


class ObjectList(Frame):
    def __init__(self, master=None, width=30, on_click=(lambda item: 0)):
        Frame.__init__(self, master)
        self.data = []
        self.on_click = on_click
        self.sbar = Scrollbar(self)
        self.list = Listbox(self, relief=GROOVE, width=width)
        self.sbar.config(command=self.list.yview)
        self.list.config(yscrollcommand=self.sbar.set)
        self.sbar.pack(side=RIGHT, fill=Y)
        self.list.pack(side=LEFT, expand=YES, fill=BOTH)
        self.list.bind('<<ListboxSelect>>', self.on_item_click)

    def clear(self):
        self.data = []
        self.list.delete(0, END)

    def insert(self, pos, item):
        self.data.insert(pos, item)
        self.list.insert(pos, str(item))

    def add(self, item):
        self.data.append(item)
        self.list.insert(END, str(item))

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        return self.data.__iter__()

    def on_item_click(self, event):
        if len(self.list.curselection()) == 0: return
        self.on_click(self.data[self.list.curselection()[0]])
