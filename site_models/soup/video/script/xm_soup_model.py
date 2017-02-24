__author__ = 'Vit'
from bs4 import BeautifulSoup

from base_classes import UrlList
from loader.base_loader import URL
from site_models.base_site_model import ParseResult, ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite, _iter
from site_models.util import psp, quotes

class XMvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "XMvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(HD_video=URL('https://ru.xhamster.com/channels/new-hd_videos-1.html*'),
                    Newest=URL('http://ru.xhamster.com/'),
                    Weekly_Top=URL('https://ru.xhamster.com/rankings/weekly-top-videos.html'),
                    Daily_Top=URL('https://ru.xhamster.com/rankings/daily-top-videos.html'),
                    Monthly_Top=URL('https://ru.xhamster.com/rankings/monthly-top-videos.html'),
                    Alltime_Top=URL('https://ru.xhamster.com/rankings/alltime-top-videos.html'),
                    )

    def startpage(self):
        return URL("http://ru.xhamster.com/", test_string='xHamster')

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('xhamster.com/')

    def parse_thumbs(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        for thumb_container in _iter(soup.find_all('div',{'class':['box boxTL','box boxTR'], 'id':lambda x: x!='vPromo'})):
            for thumb in _iter(thumb_container.find_all('div',{'class':'video'})):
                # psp(thumb)
                href = URL(thumb.a.attrs['href'], base_url=base_url)
                description = thumb.a.img.attrs['alt']
                thumb_url = URL(thumb.img.attrs['src'], base_url=base_url)

                duration = thumb.find('b')
                dur_time = '' if duration is None else str(duration.string)

                quality = thumb.find('div', {'class': "hSpriteHD"})
                qual = '' if quality is None else 'HD'

                result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                           labels=[{'text': dur_time, 'align': 'top right'},
                                                   {'text': description, 'align': 'bottom center'},
                                                   {'text': qual, 'align': 'top left', 'bold': True}]))

    def parse_thumbs_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        menu=soup.find('div', {'id':'menuLeft'})
        hrefs=menu.find_all('a',{'href':lambda x: '/channels/' in x})
        for item in _iter(hrefs):
            label=''
            for s in item.stripped_strings:
                label +=s
            href = item.attrs['href']
            result.add_control(ControlInfo(label.strip(), URL(href, base_url=base_url)))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pager'})

    def parse_video(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        video = soup.find('div', {'id': 'playerSwf'})
        if video is not None:
            urls = UrlList()
            script=video.find('script', text=lambda x: 'XPlayer' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\\/', '/')
                if 'sources:' in data:
                    sources=quotes(data,'sources:{','}').split('","')
                    for item in sources:
                        part=item.partition('":"')
                        file = part[2].strip('"')
                        label=part[0].strip('"')
                        urls.add(label, URL(file, base_url=base_url))
                    result.set_video(urls.get_media_data(-1))

    def parse_video_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        info_box = soup.find('div', {'id': 'videoInfoBox'})
        for item in _iter(info_box.find_all('a')):
            # psp(item)
            label=''
            for s in item.stripped_strings:
                label +=s
            color = None
            href = item.attrs['href']
            if '/pornstars/' in href:
                color = 'magenta'
                # href += '/videos'
            if '/user/' in href:
                color = 'blue'
                href = href.replace('/user/','/user/video/')+'/new-1.html'

            result.add_control(ControlInfo(label.strip(), URL(href, base_url=base_url), text_color=color))


if __name__ == "__main__":
    pass