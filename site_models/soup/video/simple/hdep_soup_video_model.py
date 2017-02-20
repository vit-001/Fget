__author__ = 'Vit'

from bs4 import BeautifulSoup

from base_classes import UrlList
from loader.base_loader import URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite, _iter
from site_models.util import quotes

class HDEPvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "HDEPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Newest=URL('http://www.hd-easyporn.com/?o=n*'),
                    Videos_Most_Viewed=URL('http://www.hd-easyporn.com/?o=v*'),
                    Videos_Top_Rated=URL('http://www.hd-easyporn.com/?o=r*'),
                    Videos_Longest=URL('http://www.hd-easyporn.com/?o=d*'),
                    Categories=URL('http://www.hd-easyporn.com/categories/')
                    )

    def startpage(self):
        return URL("http://www.hd-easyporn.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('hd-easyporn.com/')

    def parse_thumbs(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        thumbs_container=soup.find('div',{'class':'videos cf'})
        if thumbs_container is not None:
            for thumbnail in _iter(thumbs_container.find_all('div',{'class':['polaroid']})):
                href=URL(thumbnail.a.attrs['href'],base_url=base_url)
                description=thumbnail.a.img.attrs['alt']
                thumb_url = URL(thumbnail.img.attrs['data-src'], base_url=base_url)

                duration = thumbnail.find('div', {'class': "duration"})
                dur_time = '' if duration is None else str(duration.string)

                result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                           labels=[{'text':dur_time, 'align':'top right'},
                                                   {'text':description, 'align':'bottom center'}]))

    def parse_others(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # parce categories page
        categories=set()
        for category in _iter(soup.find_all('div',{'class':'catbox'})):
            href = URL(category.a.attrs['href'], base_url=base_url)
            thumb_url = URL(category.img.attrs['data-src'], base_url=base_url)
            title=str(category.find('div',{'class':'title'}).string)

            if title not in categories:
                result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=title,
                                       labels=[{'text': title, 'align': 'top right'}]))
                categories.add(title)

    def get_pagination_container(self,soup:BeautifulSoup):
        return  soup.find('div', {'class': 'pagination'})

    def parse_thumbs_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        tags = soup.find('ul', {'class': 'tags cf'})
        if tags is not None:
            for tag in tags.find_all('a'):
                result.add_control(ControlInfo(str(tag.string).strip(), URL(tag.attrs['href'], base_url=base_url)))

    def parse_video(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        video = soup.find('div',{'class':'video'})
        if video is not None:
            urls = UrlList()
            for source in _iter(video.find_all('source')):
                urls.add(source.attrs['res'], URL(source.attrs['src'],base_url=base_url))
            result.set_video(urls.get_media_data(-1))

    def parse_video_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        for tag_container in _iter(soup.find_all('div', {'class': 'video_header'})):
            for href in _iter(tag_container.find_all('a')):
                if href.string is not None:
                    result.add_control(ControlInfo(str(href.string), URL(href.attrs['href'], base_url=base_url)))

if __name__ == "__main__":
    pass
