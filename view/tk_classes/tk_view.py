__author__ = 'Vit'

from tkinter import *
from tkinter.messagebox import askokcancel
from tkinter.ttk import *

from base_classes import ControllerFromViewInterface, AbstractPictureView, AbstractThumbView, URL
from view.tk_classes.widgets.button_line import HScrolledButtonLine
from view.tk_classes.widgets.dir_viewer import DirViewer
from view.tk_classes.widgets.progress_line import ProgressLine
from view.tk_classes.widgets.tumb_view import ExtendedThumbView


class Popup():
    def build(self, coord, txt):
        self.pupwin = Toplevel()
        self.pupwin.overrideredirect(True)
        self.pupwin.geometry(coord)
        self.label = Label(self.pupwin, text=txt)
        self.label.pack(side=BOTTOM)

    def destroy(self):
        self.pupwin.destroy()


class HistoryCombobox(Combobox):
    def __init__(self, master=None, **kw):
        Combobox.__init__(self, master, **kw)
        self.history = []
        self.config(value=self.history)

    def add(self, href=URL()):
        if href.get() in self.history:
            self.history.remove(href.get())
        self.history.insert(0, href.get())
        self.config(value=self.history)
        self.current(0)


class ThumbViewer(Tk, AbstractThumbView):
    def __init__(self, controller=ControllerFromViewInterface()):
        Tk.__init__(self)
        self.geometry('440x895+41+92')
        self.title('SViewer')
        self.controller = controller
        self.full_view = None
        self.full_view_geometry = '1227x1072+599+42'
        self._make_widgets()
        self.url = None
        self.pos = None
        s = Style()
        s.theme_use('default')
        # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        self.bind_all('<Control-`>', self.panic)

    def _make_widgets(self):
        # if self.debug:
        #     self.debug_button = Button(self, text='DEBUG', command=self._debug)
        #     self.debug_button.pack()
        # self.controls = Labelframe(self, text='site to view')
        # self.controls.pack(side=TOP, fill=X)
        self.buttons = HScrolledButtonLine(self)
        self.buttons.pack(side=TOP, fill=X)

        bottomframe = Frame(self)
        bottomframe.pack(side=BOTTOM, fill=X)
        self.history = HistoryCombobox(bottomframe)
        self.history_go = Button(bottomframe, text='Go',
                                 command=lambda: self.controller.goto_url(URL(self.history_choice.get())))
        self.history_go.pack(side=RIGHT)
        self.back = Button(bottomframe, text='<<<', command=self.controller.back)
        self.back.pack(side=LEFT)

        self.history.pack(side=LEFT, fill=X, expand=YES)

        self.history_choice = StringVar()
        self.history.config(textvariable=self.history_choice)

        self.progress = ProgressLine(self, height=4)
        self.progress.pack(side=BOTTOM, fill=X)

        self.pages_bns = HScrolledButtonLine(self)
        self.pages_bns.pack(side=BOTTOM, fill=X)

        self.href_bns = HScrolledButtonLine(self)
        self.href_bns.pack(side=BOTTOM, fill=X)

        self.thumb = ExtendedThumbView(self)
        self.thumb.pack(side=TOP, fill=BOTH, expand=YES)

    def _debug(self):
        pass

    #     print('debug')
    #     gc.disable()
    #     gc.set_debug(gc.DEBUG_STATS)
    #     print(gc.collect())

    def panic(self, event):
        self.wm_state('icon')
        if self.full_view is not None:
            self.full_view.wm_state('icon')

    def history_add(self, href=URL()):
        self.history.add(href)

    def add_site_button(self, text='', action=lambda: 0):
        self.buttons.add_button(text, action)

    def add_control(self, text='', action=lambda: 0):
        self.href_bns.add_button(text, action)

    def add_page(self, text='', action=lambda: 0):
        self.pages_bns.add_button(text, action)

    def add_preview(self, picture_fname='', action=lambda: 0, popup_text=''):
        bn = self.thumb.add(picture_fname, picture_fname == self.pos)
        bn.configure(command=action)

        bn.bind('<Enter>', lambda event: self.show_popup('+%d+%d' % (event.x_root, event.y_root), popup_text))
        bn.bind('<Leave>', lambda event: self.hide_popup())
        self.update()
        self.title(self.url.get() + ' (' + str(len(self.thumb.thumbs)) + ' thumbs)')

    def show_popup(self, coord, text):
        self.popup = Popup()
        self.popup.build(coord, text)

    def hide_popup(self):
        self.popup.destroy()

    def set_thumbs_pos(self, pos):
        self.pos = pos

    def get_thumbs_pos(self):
        y = self.thumb.winfo_height()
        object = self.thumb.get_object_by_coord(0, y)
        if object is not None:
            return object.get_fname()
        else:
            return None

    def clear_thumbs(self):
        self.thumb.clear()
        self.pages_bns.clear()
        self.href_bns.clear()
        self.update()

    def set_thumbs_url(self, url=URL()):
        self.url = url
        self.title(url.get())

    def get_url(self):
        return self.url

    def progress_init(self, maximum=100):
        self.progress.re_init(maximum)
        self.progress.set_height(4)

    def progress_set(self, value):
        self.progress.set(value)

    def progress_stop(self):
        self.progress.set_height(0)

    def set_cycle_handler(self, handler=lambda: 0):
        self.cycle_handler = handler
        self.cycle()

    def cycle(self):
        self.cycle_handler()
        self.after(100, self.cycle)

    def get_picture_view(self, page_dir='', url=URL(), max_pics=12):
        if self.full_view is None:
            self.full_view = FullView(self, self.controller)
            self.full_view.geometry(self.full_view_geometry)
            self.full_view.protocol('WM_DELETE_WINDOW', self.on_destroy_full_view)
        self.full_view.set_dir(page_dir, max_pics)

        self.full_view.clear_control()
        self.full_view.wm_state('normal')
        return self.full_view

    def on_destroy_full_view(self):
        # self.full_view_geometry = self.full_view.winfo_geometry()
        self.full_view.wm_state('icon')


class FavoriteSelectorCombo(Frame):
    def __init__(self, master=None, controller=ControllerFromViewInterface):
        Frame.__init__(self, master)

        self.controller = controller
        self.fullscreen = False

        self.bn_add = Button(self, text="*")
        self.bn_add.grid(column=0, row=0)

        self.combo_category_list = Combobox(self)
        self.combo_category_list.grid(column=2, row=0)
        self.combo_category_list.configure(width=10)

        self.combo_url_list = Combobox(self)
        self.combo_url_list.grid(column=3, row=0, sticky=EW)

        self.bn_del = Button(self, text="-",
                             command=lambda: self.favorite_delete())
        self.bn_del.grid(column=1, row=0)
        self.bn_go = Button(self, text="Go",
                            command=lambda: self.controller.goto_url(URL(self.var_url_choice.get())))
        self.bn_go.grid(column=4, row=0)

        self.bn_show = Button(self, text='Show', command=self.toggle_fullscreen)
        self.bn_show.grid(column=5, row=0)

        self.columnconfigure(3, weight=4)

        self.var_url_choice = StringVar()
        self.combo_url_list.config(textvariable=self.var_url_choice)
        self.var_category_choice = StringVar()
        self.combo_category_list.config(textvariable=self.var_category_choice)

    def favorite_delete(self):
        answer = askokcancel('Confirm', 'Really delete ' + self.var_url_choice.get())
        if answer:
            self.controller.favorite_delete(URL(self.var_url_choice.get()), self.var_category_choice.get())

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.winfo_toplevel().wm_state('normal')
            self.winfo_toplevel().overrideredirect(False)
            self.winfo_toplevel().wm_geometry(self.save_geometry)
            self.combo_url_list.bind("<<ComboboxSelected>>", lambda x: None)
            self.fullscreen = False
        else:
            self.save_geometry = self.winfo_toplevel().winfo_geometry()
            self.winfo_toplevel().wm_state('zoomed')
            self.winfo_toplevel().overrideredirect(True)
            self.combo_url_list.bind("<<ComboboxSelected>>",
                                     lambda x: self.controller.goto_url(URL(self.var_url_choice.get())))
            self.fullscreen = True

    def set_favorite_list(self, favorite_list=list()):
        self.combo_url_list.configure(value=favorite_list)
        if self.combo_url_list.current() == -1:
            if len(favorite_list) > 0:
                self.combo_url_list.current(0)
        if self.fullscreen:
            self.controller.goto_url(self.var_url_choice.get())

    def set_favorite_category_list(self, category_list=list()):
        self.combo_category_list.configure(value=category_list)
        if self.combo_category_list.current() == -1:
            if len(category_list) > 0:
                self.combo_category_list.current(0)
                self.category_change_handler(self.var_category_choice.get())

    def set_favorite_add_handler(self, handler=lambda cat: None):
        self.bn_add.configure(command=lambda: handler(self.var_category_choice.get()))

    def set_favorite_category_change_handler(self, handler=lambda cat: None):
        self.category_change_handler = handler
        self.combo_category_list.bind("<<ComboboxSelected>>", lambda x: handler(self.var_category_choice.get()))


class FullView(Toplevel, AbstractPictureView):
    def __init__(self, master=None, controller=ControllerFromViewInterface()):
        Toplevel.__init__(self, master)
        self.controller = controller
        self.make_widgets()

    def make_widgets(self):
        top_frame = Frame(self)
        top_frame.pack(side=BOTTOM, fill=X)

        self.buttons = HScrolledButtonLine(top_frame, scrollable=True)
        self.buttons.grid(column=0, row=0, sticky=EW)

        self.fav_combo = FavoriteSelectorCombo(top_frame, self.controller)
        self.fav_combo.grid(column=1, row=0, sticky=EW)

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=3)

        self.picture = DirViewer(self, on_picture_change=self.on_picture_change)
        self.picture.pack(fill=BOTH, expand=YES)

    def set_favorite_handlers(self, add_handler=lambda cat: None, category_change_handler=lambda i: None):
        self.fav_combo.set_favorite_add_handler(add_handler)
        self.fav_combo.set_favorite_category_change_handler(category_change_handler)

    def set_favorite_list(self, favorite_list=list()):
        self.fav_combo.set_favorite_list(favorite_list)

    def set_favorite_category_list(self, category_list=list()):
        self.fav_combo.set_favorite_category_list(category_list)

    def add_control(self, text='', action=lambda: 0):
        self.buttons.add_button(text, action)

    def clear_control(self):
        self.buttons.clear()

    def set_dir(self, page_dir='', max_pics=0):
        self.page_dir = page_dir
        self.picture.set_dir(page_dir, max_pics)

    def set_max_pics(self, max_pix=12): raise Exception()

    def refresh(self):
        self.update()
        self.picture.load_dir()

    def on_picture_change(self, fname, cur_pic, max_pic, loaded):
        self.title(
            self.page_dir + fname + '  (' + str(cur_pic + 1) + ' of ' + str(max_pic) + ', ' + str(loaded) + ' loaded)')


if __name__ == "__main__":
    tk = ThumbViewer()
    tk.geometry('820x600+100+100')

    tk.mainloop()
