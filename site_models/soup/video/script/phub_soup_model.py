__author__ = 'Vit'
from bs4 import BeautifulSoup
import re

from base_classes import UrlList
from loader.base_loader import URL
from site_models.base_site_model import ParseResult, ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite, _iter
from site_models.util import psp, quotes

class PHUBvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "PHUBvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(HD_video=URL('https://ru.xhamster.com/channels/new-hd_videos-1.html*'),
                    Newest=URL('http://ru.xhamster.com/'),
                    Weekly_Top=URL('https://ru.xhamster.com/rankings/weekly-top-videos.html'),
                    Daily_Top=URL('https://ru.xhamster.com/rankings/daily-top-videos.html'),
                    Monthly_Top=URL('https://ru.xhamster.com/rankings/monthly-top-videos.html'),
                    Alltime_Top=URL('https://ru.xhamster.com/rankings/alltime-top-videos.html'),
                    )

    def startpage(self):
        return URL("http://www.pornhub.com/video?o=cm*", test_string='xxx')

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('pornhub.com/')

    def parse_thumbs(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        for thumb_container in _iter(soup.find_all('div',{'class':'sectionWrapper'})):
            for thumb in _iter(thumb_container.find_all('li',{'class':'videoblock'})):
                # psp(thumb)
                href = URL(thumb.a.attrs['href'], base_url=base_url)
                description = thumb.img.attrs['alt']
                thumb_url = URL(thumb.img.attrs['data-mediumthumb'], base_url=base_url)

                duration = thumb.find('var', {'class':'duration'})
                dur_time = '' if duration is None else str(duration.string)

                quality = thumb.find('span', {'class': "hd-thumbnail"})
                qual = '' if quality is None else 'HD'

                result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                           labels=[{'text': dur_time, 'align': 'top right'},
                                                   {'text': description, 'align': 'bottom center'},
                                                   {'text': qual, 'align': 'top left', 'bold': True}]))

    def parse_thumbs_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        for sidebar in _iter(soup.find_all('div',{'class':'sidebar_wrapper'})):
            for category in _iter(sidebar.find_all('a',{'href':lambda x: '/video?c' in x})):
                label = ''
                for s in category.stripped_strings:
                    label += s
                result.add_control(ControlInfo(label, URL(category.attrs['href'], base_url=base_url)))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination3'})

    def parse_video(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        video = soup.find('div', {'id': 'player'})
        if video is not None:
            urls = UrlList()
            script=video.find('script', text=lambda x: 'flashvars' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\\/', '/')
                # psp(data)
                p = re.findall('varplayer_quality_\w*="[\w/:._?=\-&]*"', data)
                for item in p:
                    part=item.partition('="')
                    file = part[2].strip('"')
                    label=quotes(part[0],'quality_','p')
                    psp(label,file)

                    if 'pornhub.com/' in file:
                        forced_proxy=True
                        print('=============== Need proxy ===============')
                    else:
                        forced_proxy=False
                    urls.add(label, URL(file, base_url=base_url, forced_proxy=True))
                urls.sort()
                result.set_video(urls.get_media_data(-1))

    def parse_video_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        info_box = soup.find('div', {'class': 'video-detailed-info'})
        # psp(info_box)
        for item in _iter(info_box.find_all('div',{'class':'usernameWrap'})):
            user=item.find('a')
            if user:
                # psp(user)
                result.add_control(ControlInfo(user.string, URL(user.attrs['href'], base_url=base_url), text_color='blue'))

        for item in _iter(info_box.find_all('div', {'class': 'pornstarsWrapper'})):
            for star in _iter(item.find_all('a',{'class':'pstar-list-btn'})):
                # psp(star)
                label=''
                for s in star.stripped_strings:
                    label +=s
                result.add_control(
                    ControlInfo(label, URL(star.attrs['href'], base_url=base_url), text_color='magenta'))

        for item in _iter(info_box.find_all('div', {'class': 'categoriesWrapper'})):
            for category in _iter(item.find_all('a',{'href':True})):
                # psp(category)
                result.add_control(ControlInfo(category.string, URL(category.attrs['href'], base_url=base_url)))

        for item in _iter(info_box.find_all('div', {'class': 'tagsWrapper'})):
            for tag in _iter(item.find_all('a',{'href':True})):
                # psp(tag)
                result.add_control(ControlInfo(tag.string, URL(tag.attrs['href'], base_url=base_url)))

if __name__ == "__main__":
    pass