__author__ = 'Nikitin'

from tkinter import *
from tkinter.ttk import *
from abc import ABCMeta, abstractmethod


def parse_geometry(geometry=''):
    (xy, x0, y0) = geometry.split('+')
    (x, y) = xy.split('x')
    return (int(x), int(y), int(x0), int(y0))


class AbstractButtonLine(metaclass=ABCMeta):
    def __init__(self): pass

    @abstractmethod
    def add_button(self, caption, action=lambda: 0): pass

    @abstractmethod
    def clear(self): pass


class ButtonLine(Frame, AbstractButtonLine):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.buttons = []

    def add_button(self, caption, action=lambda: 0):
        bn = Button(self, text=caption, command=action)
        bn.grid(row=0, column=len(self.buttons))
        self.buttons.append(bn)
        self.update()
        print(bn.winfo_geometry())
        # bn.configure(command=lambda:print(bn.winfo_geometry()))

    def clear(self):
        for bn in self.buttons:
            bn.destroy()
        self.buttons = []


class HScrolledButtonLine(Frame, AbstractButtonLine):
    def __init__(self, master=None, scrollable=True):
        Frame.__init__(self, master)
        self.scrollable = scrollable
        self.buttons = list()
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side=TOP, fill=X, expand=YES)
        self.canvas.config(height=0, scrollregion=(0, 0, 0, 0))

        self.xmax = 0
        self.ymax = 0

        if self.scrollable:
            self.canvas.bind('<MouseWheel>', (lambda event: self.canvas.xview_scroll(-event.delta // 120 * 1, 'units')))

    def add_button(self, caption, action=lambda: 0):
        self.canvas.config(height=25)
        bn = Button(self.canvas, text=caption, command=action)
        id = self.canvas.create_window(0, 0, window=bn, tag='button', anchor=NW)
        self.update()
        (x, y, x0, y0) = parse_geometry(bn.winfo_geometry())
        self.ymax = max(self.ymax, y)
        self.canvas.config(height=self.ymax, scrollregion=(0, 0, self.xmax + x, self.ymax))
        self.canvas.move(id, self.xmax, 0)
        self.xmax += x
        if self.scrollable:
            bn.bind('<MouseWheel>', (lambda event: self.canvas.xview_scroll(-event.delta // 120 * 1, 'units')))
        self.buttons.append(bn)

    def clear(self):
        self.canvas.delete('button')
        self.canvas.config(height=0, scrollregion=(0, 0, 0, 0))
        self.buttons = list()
        self.xmax = 0
        self.ymax = 0


if __name__ == "__main__":
    def add_bn():
        global i
        sbl.add_button('bn' + str(i) + '\nsss')
        i += 1

    def clr():
        sbl.clear()

    i = 0
    tk = Tk()
    tk.geometry('700x500+100+100')
    tk.configure(background='green')

    bl = ButtonLine(tk)
    bl.add_button('BN1\nsss', clr)
    bl.add_button('BN2', add_bn)
    bl.pack()

    sbl = HScrolledButtonLine(tk)
    sbl.pack(fill=X)

    tk.mainloop()
