__author__ = 'Vit'

from tkinter import *
import os

from PIL import Image, ImageTk


class FramedButton(Frame):
    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master)
        self.size = kw.pop('size', 200)
        self.picture = kw.pop('picture', '')
        self.loaded = False
        super().configure(width=self.size, height=self.size, background='black')
        self.bn = Button(self, cnf, **kw)
        self.bn.place(x=self.size // 2, y=self.size // 2, anchor=CENTER)

    def re_init(self, picture=''):
        self.picture = picture
        self.loaded = False

    def configure(self, cnf=None, **kw):
        return self.bn.configure(cnf, **kw)

    def bind(self, sequence=None, func=None, add=None):
        self.bn.bind(sequence, func, add)
        return super().bind(sequence, func, add)

    def set_number(self, n):
        self.number = n

    def get_number(self):
        return self.number

    def get_fname(self):
        return self.picture

    def show_image(self):
        if self.loaded:
            return
        try:
            pic = Image.open(self.picture)
            pic.thumbnail((self.size, self.size), Image.BICUBIC)
            self.photo = ImageTk.PhotoImage(pic)
            self.bn.configure(image=self.photo)
        except os.error as error:
            print('OS error', error.args)
            pass
        self.loaded = True


class ExtendedCanvas(Canvas):
    def set_yscroll_bind(self, proc=lambda: None):
        self.proc = proc

    def yview_scroll(self, number, what):
        super().yview_scroll(number, what)
        self.proc()

    def yview_moveto(self, fraction):
        super().yview_moveto(fraction)
        self.proc()

    def yview(self, *args):
        x = super().yview(*args)
        self.proc()
        return x


class ExtendedThumbView(Frame):
    def __init__(self, master=None, tumbsize=210, spacing=2, framesize=(600, 600)):
        Frame.__init__(self, master, height=framesize[1], width=framesize[0])
        self.canvas = ExtendedCanvas(self, borderwidth=0)
        self.vbar = Scrollbar(self)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES)

        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)

        self.thumbsize = tumbsize
        self.spacing = tumbsize + spacing
        self.thumbs = []
        self.free_thumbs = []

        self.bind('<Configure>', (lambda event: self.on_size_change()))
        self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(-event.delta // 120 * 2, 'units'))
        self.canvas.set_yscroll_bind(self.on_canvas_yscroll)

        self.refresh()

    def clear(self):
        for item in self.thumbs:
            self.free_thumbs.append(item)
        self.thumbs = []
        self.refresh()

    def add(self, fname, scroll=False):
        if len(self.free_thumbs) > 0:
            bn = self.free_thumbs.pop()
            bn.re_init(picture=fname)
        else:
            bn = FramedButton(self.canvas, size=self.thumbsize, picture=fname, text='loading...', borderwidth=0)
        # bn.show_image()
        bn.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(-event.delta // 120 * 2, 'units'))

        self.thumbs.append(bn)
        self._set_canvas_size()

        i = len(self.thumbs) - 1
        self._set_tumb_on_pos(bn, i, scroll)

        return bn.bn

    def on_canvas_yscroll(self):
        self.after_idle(self.show)

    def show(self):
        x = self.canvas.winfo_width()
        y = self.canvas.winfo_height()
        bns = self.canvas.find_overlapping(self.canvas.canvasx(0), self.canvas.canvasy(-self.thumbsize),
                                           self.canvas.canvasx(x), self.canvas.canvasy(y))
        for i in bns:
            for bn in self.thumbs:
                if bn.get_number() == i:
                    bn.show_image()

    def _set_tumb_on_pos(self, thumb, pos, scroll=False):
        y = pos // self.coloumns
        x = pos - y * self.coloumns
        y *= self.spacing
        x *= self.spacing

        thumb.set_number(self.canvas.create_window(x, y, window=thumb, tag='tumbs', anchor=NW))

        if scroll:
            self.canvas.yview_moveto(0)
            self.canvas.yview_scroll(y + self.canvas.winfo_height(), 'unit')
            self.show()
        else:
            y_curr = self.canvas.winfo_height()
            y_min = self.canvas.canvasy(-self.thumbsize)
            y_max = self.canvas.canvasy(y_curr)
            if y_min < y < y_max:
                self.show()

    def _set_canvas_size(self):
        self.coloumns = self.canvas.winfo_width() // self.thumbsize
        if self.coloumns == 0:
            self.coloumns = 1

        rows = len(self.thumbs) // self.coloumns
        if rows * self.coloumns < len(self.thumbs):
            rows += 1

        self.canvas.config(scrollregion=(0, 0, self.coloumns * self.spacing, rows * self.spacing))

    def on_size_change(self):
        col = self.canvas.winfo_width() // self.spacing
        if col == 0:
            col = 1
        if self.coloumns != col:
            self.refresh()

    def refresh(self):
        self.canvas.delete('tumbs')
        self._set_canvas_size()

        i = 0
        for bn in self.thumbs:
            self._set_tumb_on_pos(bn, i)
            i += 1

    def get_object_by_coord(self, x, y):
        x = self.canvas.canvasx(x)
        y = self.canvas.canvasy(y)
        ids = self.canvas.find_closest(x, y, halo=5)
        for thumb in self.thumbs:
            if thumb.get_number() == ids[0]:
                return thumb
        return None
