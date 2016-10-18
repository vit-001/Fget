__author__ = 'Vit'

from tkinter import *


class ProgressLine(Frame):
    def __init__(self, master, height=4, color='red', color2='blue', background='gray', maximum=100):
        Frame.__init__(self, master, background=background, height=height, borderwidth=0)
        self.height = height
        self.background = background
        self.color = color
        self.color2 = color2
        self.max = maximum
        self.value = 0
        self.value2 = 0
        self.bind('<Configure>', (lambda event: self.on_size_change()))
        self.canvas = Canvas(self, background=self.background, height=self.height, width=1)
        self.canvas.pack(fill=X)
        self.rectangle = self.canvas.create_rectangle(0, 0, 0, self.height, fill=self.color)
        self.rectangle2 = self.canvas.create_rectangle(0, 0, 0, self.height, fill=self.color2)

    def set_height(self, height=4):
        self.height = height
        self.canvas.configure(height=height)

    def re_init(self, maximum=100):
        self.max = maximum
        self.value = 0
        self._redraw()

    def set(self, value):
        if value < 0: value = 0
        if value > self.max: value = self.max
        self.value = value
        self._redraw()

    def set2(self, value):
        if value < 0: value = 0
        if value > self.max: value = self.max
        self.value2 = value
        self._redraw()

    def on_size_change(self):
        # print(self.winfo_geometry())
        self.canvas.configure(height=self.height, width=self.winfo_width() - 4)
        self._redraw()

    def _redraw(self):
        if self.max!=0:
            x = self.canvas.winfo_width() * self.value // self.max
            x2 = self.canvas.winfo_width() * self.value2 // self.max
        else:
            x=x2=0
        self.canvas.coords(self.rectangle, 0, 0, x, self.height)
        self.canvas.coords(self.rectangle2, 0, 0, x2, self.height)


if __name__ == "__main__":
    def press():
        global i
        pl.set(i)
        i += 1


    tk = Tk()

    i = 0

    pl = ProgressLine(tk, maximum=20)
    pl.pack(side=BOTTOM, fill=X)

    bn = Button(tk, text='+1', command=press)
    bn.pack(fill=X)

    tk.mainloop()
