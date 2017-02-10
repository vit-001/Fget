__author__ = 'Vit'

from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite, _iter
from site_models.util import get_href,get_url,quotes

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

    def parse_soup(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # parce video page
        video = soup.find('div',{'class':'video'})
        if video is not None:
            urls = UrlList()
            for source in _iter(video.find_all('source')):
                urls.add(source.attrs['res'], get_url(source.attrs['src'],base_url))
            result.set_video(urls.get_media_data(-1))

            for tag_container in _iter(soup.find_all('div', {'class':'video_header'})):
                for href in _iter(tag_container.find_all('a')):
                    if href.string is not None:
                        result.add_control(ControlInfo(str(href.string), get_url(href.attrs['href'],base_url)))
            return result

        # parce thumbnail page
        thumbs_container=soup.find('div',{'class':'videos cf'})
        if thumbs_container is not None:
            for thumbnail in _iter(thumbs_container.find_all('div',{'class':['polaroid']})):
                href=get_url(thumbnail.a.attrs['href'],base_url)
                description=thumbnail.a.img.attrs['alt']
                thumb_url = get_url(thumbnail.img.attrs['data-src'], base_url)
                dur_time = str(thumbnail.find('div', {'class': "duration"}).string)
                result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                           labels=[{'text':dur_time, 'align':'top right'},{'text':description, 'align':'bottom center'}]))

            tags=soup.find('ul', {'class': 'tags cf'})
            if tags is not None:
                for tag in tags.find_all('a'):
                    result.add_control(ControlInfo(str(tag.string).strip(), get_url(tag.attrs['href'],base_url)))

            pagination=soup.find('div', {'class': 'pagination'})
            if pagination is not None:
                for page in pagination.find_all('a'):
                    if page.string.isdigit():
                        result.add_page(ControlInfo(page.string, get_url(page.attrs['href'],base_url)))
            return result

        # parce categories page
        categories=set()
        for category in _iter(soup.find_all('div',{'class':'catbox'})):
            href = get_url(category.a.attrs['href'], base_url)
            thumb_url = get_url(category.img.attrs['data-src'], base_url)
            title=str(category.find('div',{'class':'title'}).string)

            if title not in categories:
                result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=title,
                                       labels=[{'text': title, 'align': 'top right'}]))
                categories.add(title)
        return result

if __name__ == "__main__":
    pass
