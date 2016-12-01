__author__ = 'Vit'

import os

from setting import Setting
from base_classes import *
# from qt_view import QTThumbViewer
from history import HistoryRecord, History, HistoryException
from favorites import Favorites,FavoriteRecord
from playlist import PlaylistEntry,Playlist
from requests_loader import Loader


class Controller(AbstractController):
    def __init__(self,view_manager_class,model_class):
        self.fav=Favorites(open(Setting.fav_filename))
        self.playlist=Playlist(open(Setting.playlist_filename))

        self.view = view_manager_class(controller=self)
        self.thumb_view=self.view.get_thumb_view()
        self.picture_view=self.view.get_picture_view()
        self.video_view=self.view.get_video_view()

        self.model = model_class(self)
        self.history = History()
        self.loader = Loader()

        self.thumb_loader = self.loader.get_new_thread(self.on_thumb_load, self.thumb_view.progress_stop)
        self.picture_loader = self.loader.get_new_thread(lambda x: self.picture_view.refresh())

        self.thumb_view.set_cycle_handler(self.cycle_handler)

    def cycle_handler(self):
        self.loader.update()

    def add_startpage(self, control=ControlInfo()):
        self.add_button_on_view(self.thumb_view.add_site_button,control)

    def goto_url(self, url=URL()):
        print('goto:', url.to_save())
        self.thumb_view.show_status('Goto url: '+url.get())

        if not self.model.can_accept_url(url):
            print('Rejected url', url.get())
            return

        index = Setting.base_dir + 'index.html'

        self.thumb_view.progress_init(1)
        self.loader.load_file(url, index, self.on_index_load)

    def uget_file(self, filename='', url=URL()):
        if Setting.controller_debug: print('Controller: uGet file ',url.get(), 'to',filename)
        if Setting.download_method=='uget':
            fname=' --filename="'+filename+'" '
            folder='--folder="'+Setting.download_dir+'"'
            os.spawnl(os.P_DETACH,Setting.uget(),'-gtk','--quiet',folder,fname,'"'+url.get()+'"')
        elif Setting.download_method=='server':
            self.load_server_integration(filename,url.get())

    def load_server_integration(self,filename='',url=''):
        i=1
        while True:
            fname=Setting.exchange_path+'fget%d.lsf'%i
            if os.path.exists(fname):
                i+=1
                print(i)
                continue
            else:
                break
        print('Writing',fname)
        file=open(fname,'w')
        file.write(filename+' '+url+'\n')


    def on_index_load(self, url=URL(), fname=''):
        self.thumb_view.progress_stop()
        self.model.accept_index(url, fname)

    def show_thumb_view(self, url=URL(), controls=list(), pages=list(), thumbs=list(), sites=list()):
        self.thumb_loader.abort()
        self.thumb_view.prepare(url)

        for item in sites:
            self.add_button_on_view(self.thumb_view.add_site_nested,item)
        for item in controls:
            self.add_button_on_view(self.thumb_view.add_control,item)
        for item in pages:
            self.add_button_on_view(self.thumb_view.add_page,item)

        self.thumb_view.progress_init(len(thumbs))
        self.curr_loading_thumb = 0

        self.thumb_loader.load_list(thumbs)

    def on_thumb_load(self, data):
        popup_text = data.get_href().get()
        alt = data.get_description()
        if alt != '':
            popup_text += '\n' + alt
        self.thumb_view.add_preview(data.get_filename(), lambda: self.goto_url(data.get_href()), popup_text)
        self.curr_loading_thumb += 1
        self.thumb_view.progress_set(self.curr_loading_thumb)

    def show_picture_view(self, url=URL(), page_dir='', controls=list(), full_list=list(), picture_collector=None):
        self.picture_loader.abort()
        self.picture_loader.load_list(full_list, picture_collector)

        self.picture_view.set_dir(page_dir, url, len(full_list))
        self.view.show_full_view(self.picture_view)

        for item in controls:
            self.picture_view.add_control(item.text, self.get_goto_url_handler(item.url))
        self.current_full_view=self.picture_view

    def show_video_view(self, page_url=URL(), video=MediaData(), controls=list()):
        self.video_view.playback(video, page_url, autoplay=True)
        self.view.show_full_view(self.video_view)
        for item in controls:
            self.video_view.add_control(item.text, self.get_goto_url_handler(item.url))
        self.current_full_view=self.video_view

    def add_button_on_view(self,view_add_function,button_data=ControlInfo()):
        if button_data.menu_text_url_dict is not None:
            menu_items=dict()
            for key in button_data.menu_text_url_dict:
                menu_items[key]=self.get_goto_url_handler(button_data.menu_text_url_dict[key])
        else:
            menu_items=None

        view_add_function(button_data.text, self.get_goto_url_handler(button_data.url),menu_items,button_data.url.get())

    def get_goto_url_handler(self, url):
        def handler(url):
            self.video_view.playlist_disconnect()
            self.goto_url(url)
        return lambda:handler(url)

    def panic(self):
        print('panic')
        self.view.panic()

    def get_favorites(self):
        return self.fav

    def get_playlist(self):
        return self.playlist

    def add_thumb_page_to_fav(self, category=''):
        url=self.thumb_view.get_url()
        if Setting.fav_debug: print('Adding thumb',url.get(),'to',category)
        self.fav.add(FavoriteRecord(url,category,FavoriteRecord.thumb,url.get()))

    def add_full_page_to_fav(self, category=''):
        url=self.current_full_view.get_url()
        if Setting.fav_debug: print('Adding full',url.get(),'to',category,', type ',self.current_full_view.get_page_type())
        self.fav.add(FavoriteRecord(url,category,self.current_full_view.get_page_type(),url.get()))

    def back(self):
        try:
            self.curr_history = None
            h = self.history.pop()
            self.goto_url(h.get_url())
            self.thumb_view.set_thumbs_pos(h.get_context())
        except HistoryException:
            pass

    def plus_action(self, url=URL):
        self.playlist.add(PlaylistEntry(url))

    def minus_action(self, url=URL):
        pass

    def on_exit(self):
        def saving(filename,proc):
            try:
                os.replace(filename, filename+'.old')
            except OSError as err:
                print('Saving',filename,err)
            try:
                file = open(filename, 'w')
                proc(file)
                file.close()
            except OSError as err:
                print('Saving',filename,err)

        saving(Setting.fav_filename,self.fav.save)
        saving(Setting.playlist_filename,self.playlist.save)
        saving(Setting.setting_file,Setting.save_setting)

        self.loader.terminate_all()

if __name__ == "__main__":
    pass
