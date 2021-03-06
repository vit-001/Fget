__author__ = 'Vit'

import urllib.parse as up
from urllib.parse import urlparse


# from favorites import FavoritesNEW


class URL():
    SUFFIXES = ['.html', '.jpg', '.gif', '.JPG', '.mp4', '.flv', 'png']

    def __init__(self, url='', method='GET', coockies=None, post_data=None, xhr_data=None):
        self.method = method
        self.coockies = coockies
        self.post_data = post_data
        self.xhr_data = xhr_data

        if url == '':
            self.url = ''
            self.no_slash = True
            return

        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url

        self.no_slash = url.endswith('*')
        self.url = url.rstrip('*')

    def get(self):
        if self.url is '': return self.url
        for suffix in URL.SUFFIXES:
            if self.url.endswith(suffix): return self.url
        if self.no_slash:
            return self.url.rstrip('/')
        return self.url.rstrip('/') + '/'

    def get_short_path(self, base=''):
        p = urlparse(self.get())
        return base.rstrip('/') + '/' + p[1] + '/' + p[2].strip(' /').replace('/', '..')

    def get_path(self, base=''):
        p = urlparse(self.get())
        p2 = p[2]
        if p2.endswith('.html') or p2.endswith('.jpg'):
            p2 = p2.rpartition('/')[0] + '/'
        return base.rstrip('/') + '/' + p[1] + p2.rstrip('/') + '/'

    def domain(self):
        p = urlparse(self.get())
        return p[1]

    def contain(self, text=''):
        return text in self.url

    def add_query(self, pair_list):
        split = up.urlsplit(self.url)
        qs = up.parse_qs(split[3]).keys()
        qsl = up.parse_qsl(split[3])

        added = set()
        for (add_name, add_value) in pair_list:
            if add_name not in qs:
                added.add(add_name)

        new_qsl = list()
        for (name, value) in qsl:
            for (add_name, add_value) in pair_list:
                if add_name == name:
                    value = add_value
            new_qsl.append(tuple([name, value]))
        for (add_name, add_value) in pair_list:
            if add_name in added:
                new_qsl.append(tuple([add_name, add_value]))

        new_query = up.urlencode(new_qsl)
        self.url = up.urlunsplit(
            up.SplitResult(scheme=split[0], netloc=split[1], path=split[2], query=new_query, fragment=split[4]))

    def to_save(self):
        if self.no_slash:
            return self.get() + '*'
        else:
            return self.get()

    def __repr__(self, *args, **kwargs):
        return self.get()

    def __str__(self, *args, **kwargs):
        return self.__repr__()

    def __eq__(self, url2):
        # print('Compare', self,url2)
        if url2 is None:
            return False
        if self.method != url2.method:
            return False
        if self.method == 'GET':
            return url2.to_save() == self.to_save()
        elif self.method == 'POST':
            if url2.to_save() != self.to_save():
                return False
            if self.post_data is None:
                return url2.post_data is None
            if url2.post_data is None:
                return False
            for key in self.post_data:
                if self.post_data[key] != url2.post_data[key]:
                    return False
            for key in url2.post_data:
                if self.post_data[key] != url2.post_data[key]:
                    return False
            return True
        return False


class UrlList:
    def __init__(self):
        self.urls = list()

    def add(self, label:str, url:URL):
        self.urls.append(dict(text=label, url=url))

    def get_media_data(self, default=0):
        video = None
        if len(self.urls) == 1:
            video = MediaData(self.urls[0]['url'])
        elif len(self.urls) > 1:
            video = MediaData(self.urls[default]['url'])
            for item in self.urls:
                video.add_alternate(item)
        return video


class MediaData:
    # txt='text'
    # url='url'
    def __init__(self, url:URL):
        self.url = url
        self.alternate = list()
        self.add_alternate(dict(text='DEFAULT', url=self.url))

    def add_alternate(self, text_url_dict):
        self.alternate.append(text_url_dict)

class ControlInfo:
    def __init__(self, text:str, url:URL, menu_text_url_dict=None, bold=False, underline=False, autoraise=False, text_color=None):
        self.text = text
        self.url = url
        self.menu_text_url_dict = menu_text_url_dict
        self.bold = bold
        self.underline = underline
        self.autorise = autoraise
        self.text_color=text_color

class AbstractModelFromControllerInterface():
    def can_accept_url(self, url:URL): pass

    def accept_index(self, url:URL, index_fname:str): pass


class AbstractModelFromSiteInterface():
    def register_site_model(self, control:ControlInfo): pass

    # def load_file(self,url=URL,filename='',on_load=lambda success:None):pass


class AbstractModel(AbstractModelFromControllerInterface, AbstractModelFromSiteInterface):
    pass


class AbstractThumbView():
    def add_site_button(self, text:str, action=lambda: 0, menu_items:dict=None, tooltip=''): pass

    def add_site_nested(self, text:str, action=lambda: 0, menu_items=None, tooltip=''): pass

    def add_control(self, text:str, action=lambda: 0, menu_items=None, tooltip=''): pass

    def add_page(self, text:str, action=lambda: 0, menu_items=None, tooltip=''): pass

    def prepare(self, url:URL, show_caption=False): pass

    def panic(self): pass

    def add_preview(self, picture_fname:str, action=lambda: 0, popup_text=''): pass

    def progress_init(self, maximum=100): pass

    def progress_set(self, value:int): pass

    def progress_stop(self): pass

    def get_url(self): pass

    def set_cycle_handler(self, handler=lambda: 0): pass

    def show_status(self, txt:str): pass


class AbstractFullView():
    def add_control(self, text:str, action=lambda: 0): pass

    def set_favorite_handlers(self, add_handler=lambda cat: None, category_change_handler=lambda i: None): pass

    def set_favorite_list(self, favorite_list:list): pass

    def set_favorite_category_list(self, category_list:list): pass

    def panic(self): pass

    def get_url(self): return URL()

    def test_favorite_item(self, item): return False

    def get_page_type(self): pass


class AbstractPictureView(AbstractFullView):
    def set_dir(self, filedir:str, url:URL, max_pics:int): pass

    def refresh(self): pass


class AbstractVideoView(AbstractFullView):
    def playback(self, media:MediaData, page_url:URL, autoplay=False): pass

    def playlist_connect(self, goto_prev=lambda: None, goto_next=lambda: None): pass

    def playlist_disconnect(self): pass


class AbstractPlaylistView():
    pass

class PresenterFromViewInterface():
    def back(self): pass

    def goto_url(self, url:URL): pass

    def uget_file(self, filename:str, url:URL): pass

    def download_now(self): pass

    def get_favorites(self): pass

    def get_playlist(self): pass

    def panic(self): pass

    def add_thumb_page_to_fav(self, category:str): pass

    def add_full_page_to_fav(self, category:str): pass

    def on_exit(self): pass


class PresenterFromModelInterface():
    def add_cycle_handler(self, handler=lambda: None): pass

    def add_startpage(self, control_info): pass

    def show_thumb_view(self, url:URL, controls:list, pages:list, thumbs:list, sites:list,
                        caption_visible=False): pass

    def show_picture_view(self, url:URL, page_dir:str, controls:list, full_list:list, picture_collector=None): pass

    def show_video_view(self, page_url:URL, video:MediaData, controls:list): pass

    # def refresh_picture_view(self): pass
    # def load_file(self,url=URL,filename='',on_load=lambda success:None):pass
    def show_status(self, txt:str): pass


class AbstractPresenter(PresenterFromViewInterface, PresenterFromModelInterface):
    pass

class AbstractViewManager():
    def get_thumb_view(self): pass

    def get_picture_view(self)-> AbstractPictureView:pass

    def get_video_view(self)-> AbstractVideoView:pass

    def get_controller(self)-> PresenterFromViewInterface:pass

    def toggle_tool_view(self): pass

    def toggle_playlist_view(self): pass

    def show_full_view(self, view:AbstractFullView): pass

    def show_config_dialog(self): pass

    def panic(self): pass

    def on_close_event(self): pass

    def recompile_interfaces(self): pass

    def add_keyboard_shortcut(self, window, shortcut:str, action=lambda: None): pass

    def show_status(self, txt:str): pass





if __name__ == "__main__":
    url = URL('http://www.extremetube.com/videos?format=json&number_pages=1&page=2*')
    print(url.get())
    url.add_query([('qqq', '1'), ('page', '5')])
    print(url.get())
