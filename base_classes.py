__author__ = 'Vit'
from loader.base_loader import URL,FLData


# from favorites import FavoritesNEW


class MediaData:
    # txt='text'
    # url='url'
    def __init__(self, url):
        self.url = url
        self.alternate = list()
        self.add_alternate(dict(text='DEFAULT', url=self.url))

    def add_alternate(self, text_url_dict):
        self.alternate.append(text_url_dict)

class ControlInfo:
    def __init__(self, text:str, url: URL, menu_text_url_dict=None, bold=False, underline=False, autoraise=False, text_color=None):
        self.text = text
        self.url = url
        self.menu_text_url_dict = menu_text_url_dict
        self.bold = bold
        self.underline = underline
        self.autorise = autoraise
        self.text_color=text_color


class UrlList:
    def __init__(self):
        self.urls = list()

    def add(self, label:str, url:URL):
        self.urls.append(dict(text=label, url=url))

    def sort(self):
        self.urls.sort(key=lambda x:int(x['text']))


    def get_media_data(self, default=0):
        video = None
        if len(self.urls) == 1:
            video = MediaData(self.urls[0]['url'])
        elif len(self.urls) > 1:
            video = MediaData(self.urls[default]['url'])
            for item in self.urls:
                video.add_alternate(item)
        return video


class AbstractModelFromControllerInterface():
    def can_accept_url(self, url: URL): pass

    def accept_index(self, filedata:FLData): pass


class AbstractModelFromSiteInterface():
    def register_site_model(self, control:ControlInfo):
        pass

    def request_file(self,filedata:FLData, on_load=lambda filedata:None):
        pass

    def on_file_parsed(self, filedata:FLData, result):
        pass


class AbstractModel(AbstractModelFromControllerInterface, AbstractModelFromSiteInterface):
    pass


class AbstractThumbView():
    def add_site_button(self, text:str, action=lambda: 0, menu_items:dict=None, tooltip='', bold=False, underline=False,
                        autoraise=False, text_color=None): pass

    def add_site_nested(self, text='', action=lambda: 0, menu_items=None, tooltip='', bold=False, underline=False,
                    autoraise=False, text_color=None): pass

    def add_control(self, text='', action=lambda: 0, menu_items=None, tooltip='', bold=False, underline=False,
                    autoraise=False, text_color=None): pass

    def add_page(self, text='', action=lambda: 0, menu_items=None, tooltip='', bold=False, underline=False,
                    autoraise=False, text_color=None): pass

    def prepare(self, url: URL, show_caption=False): pass

    def panic(self): pass

    def add_preview(self, picture_fname:str, action=lambda: 0, popup_text=''): pass

    def progress_init(self, maximum=100): pass

    def progress_set(self, value:int): pass

    def progress_stop(self): pass

    def get_url(self): pass

    def set_cycle_handler(self, handler=lambda: 0): pass

    def show_status(self, txt:str): pass


class AbstractFullView():
    def add_control(self, text='', action=lambda: 0, menu_items=None, tooltip='', bold=False, underline=False,
                    autoraise=False, text_color=None): pass

    def set_favorite_handlers(self, add_handler=lambda cat: None, category_change_handler=lambda i: None): pass

    def set_favorite_list(self, favorite_list:list): pass

    def set_favorite_category_list(self, category_list:list): pass

    def panic(self): pass

    def get_url(self): return URL()

    def test_favorite_item(self, item): return False

    def get_page_type(self): pass


class AbstractPictureView(AbstractFullView):
    def set_dir(self, filedir:str, url: URL, max_pics:int): pass

    def refresh(self): pass


class AbstractVideoView(AbstractFullView):
    def playback(self, media:MediaData, page_url: URL, autoplay=False): pass

    def playlist_connect(self, goto_prev=lambda: None, goto_next=lambda: None): pass

    def playlist_disconnect(self): pass


class AbstractPlaylistView():
    pass

class PresenterFromViewInterface():
    def back(self): pass

    def goto_url(self, url: URL): pass

    def uget_file(self, filename:str, url: URL): pass

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

    def show_thumb_view(self, url: URL, controls:list, pages:list, thumbs:list, sites:list,
                        caption_visible=False): pass

    def show_picture_view(self, url: URL, page_dir:str, controls:list, full_list:list, picture_collector=None): pass

    def show_video_view(self, page_url: URL, video:MediaData, controls:list): pass

    # def refresh_picture_view(self): pass
    def request_file(self, filedata: FLData, on_load=lambda filedata: None):pass

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

