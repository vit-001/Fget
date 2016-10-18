__author__ = 'Vit'

from tkinter import *
import glob
import os.path

from PIL import Image, ImageTk

from view.tk_classes.widgets.progress_line import ProgressLine


class DirViewer(Frame):
    def __init__(self, master=None, mode='thumb',on_picture_change=(lambda fname, cur_pic, max_pic, loaded: 0)):
        Frame.__init__(self, master, background='black', borderwidth=0)
        self.dir = ''
        self.handler = on_picture_change
        self.mode=mode
        self.current_image = 0
        self.use_progress = False
        self.max_pics = 0

        self.make_widgets()
        self.load_dir()
        self.binding()

    def binding(self):
        self.bind('<Configure>', (lambda event: self.on_change_size()))
        self.bind_all('<KeyPress-Down>', lambda event: self.change_pic(1))
        self.bind_all('<KeyPress-Up>', lambda event: self.change_pic(-1))
        self.bind_all('<KeyPress-End>', lambda event: self.change_pic(len(self.files)))
        self.bind_all('<KeyPress-Home>', lambda event: self.change_pic(-len(self.files)))
        self.bind_all('<KeyPress-Prior>', lambda event: self.change_pic(-10))
        self.bind_all('<KeyPress-Next>', lambda event: self.change_pic(10))
        self.bind_all('/', lambda event: self.set_mode('window'))
        self.bind_all('*', lambda event: self.set_mode('thumb'))

        self.canvas.bind('<MouseWheel>', (lambda event: self.change_pic(-event.delta // 120)))

    def set_dir(self, dir='', max_pics=0):
        self.dir = dir
        self.max_pics = max_pics
        self.current_image = 0
        if max_pics == 0:
            self.use_progress = False
        else:
            self.use_progress = True
            self.progress.re_init(max_pics)
        self.load_dir()

    def set_mode(self,mode='thumb'):
        print('mode',mode)
        self.mode=mode
        self.redraw_pic()

    def on_change_size(self):
        self.after_idle(self.redraw_pic)

    def change_pic(self, delta):
        self.current_image += delta
        if self.current_image < 0: self.current_image = 0
        if self.current_image > len(self.files) - 1: self.current_image = len(self.files) - 1

        self.after_idle(self.load_pic)

    def make_widgets(self):
        self.canvas = Canvas(self, borderwidth=0, bg='black')
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES)

        self.progress = ProgressLine(self.canvas)
        self.progress_pos = self.canvas.create_window(0, 0, window=self.progress, tag='progress', anchor=W)

    def redraw_pic(self):
        if self.no_pic: return
        self.canvas.delete('pic')
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        try:
            img = self.fit_to_window(Image.open(self.files[self.current_image].replace('\\', '/')),w,h)

            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(w // 2, h // 2, image=self.photo, anchor=CENTER, tag='pic')
        except OSError:
            print('OS error:')

        self.progress.configure(width=w)
        self.canvas.coords(self.progress_pos, 0, h * 96 / 100)

        if self.use_progress:
            self.progress.configure(width=w)
        else:
            self.progress.configure(width=0)

    def fit_to_window(self,img,w,h):

        if self.mode=='thumb':
            img.thumbnail((w, h), Image.BICUBIC)
        elif self.mode=='window':
            (iw,ih)=img.size
            if iw>w or ih>h:
                img.thumbnail((w, h), Image.BICUBIC)
            else:
                aspect=iw/ih
                window_aspect=w/h
                if window_aspect<aspect:
                    iw_new=w
                    ih_new=w/aspect
                else:
                    iw_new=h*aspect
                    ih_new=h
                img=img.resize((int(iw_new),int(ih_new)),Image.BICUBIC)
        else:
            print('DirViewer.fit_to_window ERROR: wrong mode, must be "thumb" or "window"')

        return img


    def load_pic(self):
        if self.no_pic: return
        self.progress.set2(self.current_image + 1)
        # self.picture = Image.open(self.files[self.current_image].replace('\\', '/'))
        picname = os.path.split(self.files[self.current_image])[1]
        self.handler(picname, self.current_image, self.max_pics, len(self.files))
        self.redraw_pic()

    def load_dir(self):
        self.files = glob.glob(self.dir + '*.jpg')
        self.progress.set(len(self.files))
        if len(self.files) >= self.max_pics:
            self.use_progress = False

        if len(self.files) == 0:
            self.no_pic = True
        else:
            self.no_pic = False
            self.load_pic()


if __name__ == "__main__":
    def handler(picname):
        tk.title(picname)

    tk = Tk()
    tk.geometry('820x600+100+100')
    viewer = DirViewer(tk, 'E:/out/www.bravoerotica.com/', handler=handler)
    viewer.pack(fill=BOTH, expand=YES)

    tk.mainloop()
