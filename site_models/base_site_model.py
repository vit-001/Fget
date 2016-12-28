__author__ = 'Vit'

from base_classes import AbstractModelFromSiteInterface, URL, ControlInfo, MediaData
from requests_loader import FLData, PictureCollector


class ThumbInfo(FLData):
    def __init__(self, thumb_url:URL, filename:str='', href:URL=URL(), description=''):
        FLData.__init__(self, url=thumb_url, filename=filename)
        self.href = href
        self.description = description

    def set_base_dir(self, base_dir:str):
        self.base_dir = base_dir

    def get_href(self):
        return self.href

    def get_description(self):
        return self.description

    def get_filename(self):
        if self.filename == '':
            return self.get_url().get_short_path(base=self.base_dir)
            # return self.base_dir+self.get_address().rpartition('/')[2]
        else:
            return self.filename

    def __str__(self):
        return 'thumb: HREF ' + self.get_href().get() + '  SRC ' + self.get_url().get()


class FullPictureInfo(FLData):
    # noinspection PyMissingConstructor
    def __init__(self, rel_name='', abs_name='', abs_href=URL()):
        self.rel_name = rel_name
        self.abs_name = abs_name
        self.abs_href = abs_href
        self.set_base()

    def set_base(self, base_dir='', base_url=URL()):
        self.base_dir = base_dir
        self.base_url = base_url

    def get_url(self)->URL:
        if self.abs_href.get() != '': return self.abs_href
        return URL(self.base_url.get() + self.rel_name)

    def get_filename(self)->str:
        if self.abs_name != '': return self.abs_name
        return self.base_dir + self.rel_name

    def __str__(self):
        return 'full: HREF ' + self.get_url().get() + '  FNAME ' + self.get_filename()


class BaseSite():
    def __init__(self, model:AbstractModelFromSiteInterface, base_addr='e:/out/'):
        self.model = model
        self.base_addr = base_addr
        self.model.register_site_model(ControlInfo(text=self.start_button_name(),
                                                   url=self.startpage(),
                                                   menu_text_url_dict=self.get_start_button_menu_text_url_dict(),
                                                   bold=self.bold(), underline=self.underline(),
                                                   autoraise=self.autoraise()))

    def bold(self):
        return False

    def underline(self):
        return False

    def autoraise(self):
        return False

    def get_href(self, txt:str, base_url:URL):
        txt = txt.strip()
        if not txt.endswith('/'):
            txt = txt + "*"
        if txt.startswith('http://'):
            return txt
        if txt.startswith('//'):
            return 'http:' + txt
        if txt.startswith('https://'):
            return txt
        if txt.startswith('/'):
            return 'http://' + base_url.domain() + txt
        # print(base_url.get() + txt)
        return base_url.get().rpartition('/')[0] + '/' + txt

    def proceed_parcing(self, parser, fname):
        # for s in open(fname, encoding='utf-8', errors='ignore'):
        #     parser.feed(s)  # .replace('</b>','</a>'))

        with open(fname,encoding='utf-8', errors='ignore') as fd:
            for s in fd:
                parser.feed(s)

    def quotes(self, text:str, from_lex:str, to_lex:str):
        return text.partition(from_lex)[2].partition(to_lex)[0]

    def start_button_name(self):
        return ''

    def get_start_button_menu_text_url_dict(self):
        return None

    def startpage(self):
        return URL()

    def parse_index_file(self, fname:str, base_url:URL):
        pass

    def can_accept_index_file(self, base_url:URL):
        return False


class BaseNest(BaseSite, AbstractModelFromSiteInterface):
    def __init__(self, model:AbstractModelFromSiteInterface, base_addr='e:/out/'):
        BaseSite.__init__(self, model, base_addr)
        self.sites = list()
        self.controls = list()

    def add_site(self, site:BaseSite):
        self.sites.append(site)

    def register_site_model(self, control:ControlInfo):
        self.controls.append(control)

    def can_accept_index_file(self, url:URL):
        for s in self.sites:
            if s.can_accept_index_file(url):
                return True
        return False

    def parse_index_file(self, fname:str, url:URL):
        site = None
        for s in self.sites:
            if s.can_accept_index_file(url):
                site = s
                break
        if site is None:
            print(url.to_save(), ' rejected')
            return

        result = site.parse_index_file(fname, url)

        for i in self.controls:
            result.add_site(i)

        return result


class BaseNestedSite(BaseSite):
    pass


class ParseResult():
    def __init__(self):
        self._type = 'none'
        self.redirect = URL()
        self.video = None
        self.thumbs = []
        self.caption_visible = False
        self.full = []
        self.controls = []
        self.pages = []
        self.sites = []
        self.gallery_path = None
        self.picture_collector = None

    def is_no_result(self):
        return self._type == 'none'

    def is_hrefs(self):
        return self._type == 'hrefs'

    def is_pictures(self):
        return self._type == 'pictures'

    def is_video(self):
        return self._type == 'video'

    def set_base(self, base_dir='', base_url=URL()):
        for item in self.thumbs:
            item.set_base_dir(base_dir)
        for item in self.full:
            item.set_base(base_dir, base_url)

    def set_gallery_path(self, path=''):
        self.gallery_path = path

    def get_gallery_path(self):
        return self.gallery_path

    def set_video(self, media:MediaData):
        self.video = media
        if media is not None:
            self._type = 'video'

    def get_video(self):
        return self.video

    def set_type(self, type):  # todo  убрать совсем
        pass
    #     # self._type = type

    def set_picture_collector(self, collector:PictureCollector):
        self.picture_collector = collector

    def set_redirect(self, url:URL):
        self.redirect = url

    def add_thumb(self, thumb:ThumbInfo):
        self.thumbs.append(thumb)
        self._type = 'hrefs'

    def add_full(self, full:FullPictureInfo):
        self.full.append(full)
        self._type = 'pictures'

    def add_control(self, control:ControlInfo):
        for c in self.controls:
            if control.url == c.url:
                return
        self.controls.append(control)

    def add_page(self, control:ControlInfo):
        for c in self.pages:
            if control.url == c.url:
                return
        self.pages.append(control)

    def add_site(self, control:ControlInfo):
        for c in self.sites:
            if control.url == c.url:
                return
        self.sites.append(control)

    def set_caption_visible(self, visible=False):
        self.caption_visible = visible

    def print_result(self):
        print('==============PARSER RESULT=============')
        print('Type', self._type)
        if type == 'none': return

        if self._type == 'hrefs':
            for i in self.thumbs:
                print(i)

        if self._type == 'pictures':
            for i in self.full:
                print(i)

        print('Controls')
        for i in self.controls:
            print(i)

        print('Pages')
        for i in self.pages:
            print(i)

        print('~~~~~~~~~~~~~~PARSER RESULT~~~~~~~~~~~~~~')


if __name__ == "__main__":
    pass
