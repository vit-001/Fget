__author__ = 'Nikitin'

from tkinter import *
from tkinter.ttk import *


class EntryBlock(Frame):
    def __init__(self, master=None, callback=(lambda event: 0), label_width=10, entry_width=60):
        Frame.__init__(self, master)
        self.label_width = label_width
        self.entry_width = entry_width
        self.rows = 0

        self.callback = callback

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=(label_width + entry_width) * 2 // label_width)

    def add_line(self, caption, var):
        label = Label(self, text=caption, width=self.label_width)
        entry = Entry(self, textvariable=var, width=self.entry_width)  # ,relief=GROOVE)
        label.grid(row=self.rows, column=0, sticky=EW)
        entry.grid(row=self.rows, column=1, sticky=EW)
        entry.bind('<FocusOut>', self.on_focus_lost)

        self.rows += 1

    def on_focus_lost(self, event):
        self.callback()
