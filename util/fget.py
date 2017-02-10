__author__ = 'Nikitin'

from tkinter import *
from urllib.parse import urlparse

from lib.file_loader import BadFileLoader
from widgets.entry_block import EntryBlock
from widgets.object_list import ObjectList
from widgets.picture_frame import PreviewFrame
from widgets.status_bar import StatusBar

from view.tk_classes.widgets.button_line import ButtonLine


class FileData():
    def __init__(self, url, filename, name):
        self.data = (url, filename, name)

    def __str__(self):
        return self.data[2]

    def url(self):
        return self.data[0]

    def filename(self):
        return self.data[1]


class ViewString():
    def __init__(self, string, lenght):
        self.string = string
        self.lenght = lenght

    def __str__(self):
        left = 7
        if len(self.string) < self.lenght:
            return self.string
        return self.string[:left] + '..' + self.string[-(self.lenght - left - 2):]

    def get(self):
        return self.string


class FGetMain(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.url = StringVar(value='http://www.bravoerotica.com/hegre/luba/table-for-two/')
        self.name = StringVar(value='%02d.jpg')
        self.start = IntVar(value=1)
        self.end = IntVar(value=12)

        self.base_path = 'e:/out/'

        self.loader = BadFileLoader(self.on_file_loaded, self.on_all_files_loaded, self.on_loading_started,
                                    self.on_load_error)

        self.make_widgets()

    def make_widgets(self):
        self.status = StatusBar(self)
        self.status.right('IDLE')

        self.loaded_list = ObjectList(self, on_click=self.on_loaded_listbox_click)
        self.loaded_list.pack(side=RIGHT, fill=Y)

        frame = Frame(self)
        frame.pack(side=TOP, fill=X)

        self.file_list = ObjectList(frame, width=15, on_click=self.on_file_listbox_click)
        self.file_list.pack(side=RIGHT)

        self.block = EntryBlock(frame, callback=self.on_input_data_change, label_width=8)
        self.block.pack(side=TOP, fill=X, expand=NO)
        self.block.add_line('Url', self.url)
        self.block.add_line('Name', self.name)
        self.block.add_line('Start', self.start)
        self.block.add_line('End', self.end)

        self.buttons = ButtonLine(frame)
        self.buttons.pack(side=TOP)
        self.buttons.add_button('Get', self.on_get_button_click)
        self.buttons.add_button('Stop', self.loader.stop)

        self.preview = PreviewFrame(self, temp_dir='e:/out/')
        self.preview.pack(fill=BOTH, expand=YES)

        self.on_input_data_change()

    def on_input_data_change(self):
        self.file_list.clear()

        url = self.url.get()
        path = urlparse(url)
        if path[0] == '': url = 'http://' + url

        filepath = path[1] + '/' + path[2].strip(' /').replace('/', '..')
        fullpath = self.base_path + filepath + '/'

        for i in range(self.start.get(), self.end.get() + 1):
            fname = self.name.get() % i
            fullname = fullpath + fname
            self.file_list.add(FileData(url + fname, fullname, fname))

    def on_get_button_click(self):
        for item in self.file_list:
            self.loader.add(item.url(), item.filename())
        self.loader.start()

    def on_load_error(self, text):
        self.status.center(text)

    def on_file_loaded(self, address, fname):
        self.status.center('Loaded: ' + address)
        self.loaded_list.add(ViewString(fname, 30))

    def on_loading_started(self):
        self.status.left('Loading...')
        self.status.right('BUSY')

    def on_all_files_loaded(self, n):
        self.status.left('Loaded ' + str(n) + ' files')
        self.status.right('IDLE')

    def on_loaded_listbox_click(self, item):
        self.preview.set_picture_from_file(item.get())

    def on_file_listbox_click(self, item):
        print('Click', item.url())
        self.preview.set_picture_from_url(item.url(), str(item))


if __name__ == "__main__":
    tk = Tk()
    tk.geometry('700x500+100+100')
    fget = FGetMain(tk)
    fget.pack(fill=BOTH, expand=YES)
    fget.mainloop()
