__author__ = 'Nikitin'

from tkinter import *

from PIL import Image, ImageTk
from lib.file_loader import BadFileLoader


class PictureFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.img = Label(self)
        self.img.pack(fill=BOTH, expand=YES)

    def refresh(self):
        size = (self.img.winfo_width(), self.img.winfo_height())
        img = self.picture.copy()
        img.thumbnail(size, Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(img)
        self.img.config(image=self.photo)

    def set_picture_from_file(self, fname):
        if fname == '': return
        self.picture = Image.open(fname)
        print(self.picture.format, self.picture.size, self.picture.mode)
        self.refresh()

    def clear(self):
        self.img.config(image='')


class PreviewFrame(PictureFrame):
    def __init__(self, master=None, temp_dir=''):
        PictureFrame.__init__(self, master)
        self.temp_dir = temp_dir
        self.loader = BadFileLoader(on_load=self.on_loaded, on_all_load=self.on_all_load, on_error=self.on_error)
        self.fname = ''
        self.error = False

    def set_picture_from_url(self, url, fname):
        self.error = False
        self.loader.stop()
        self.loader.add(url, self.temp_dir + fname)
        self.loader.start()

    def on_loaded(self, adress, fname):
        self.fname = fname

    def on_all_load(self, n):
        if not self.error:
            self.set_picture_from_file(self.fname)

    def on_error(self, error):
        self.error = True
        self.clear()
        self.img.config(text=error)
