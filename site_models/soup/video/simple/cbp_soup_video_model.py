__author__ = 'Vit'
from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite,_iter
from site_models.util import get_href,get_url,quotes

class CBPvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "CBPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(HD=URL('http://collectionofbestporn.com/tag/hd-porn*'),
                    Latest=URL('http://collectionofbestporn.com/most-recent*'),
                    TopRated=URL('http://collectionofbestporn.com/top-rated*'),
                    MostViewed=URL('http://collectionofbestporn.com/most-viewed*'),
                    Categories=URL('http://collectionofbestporn.com/channels/'),
                    Longest=URL('http://collectionofbestporn.com/longest*'))

    def startpage(self):
        return URL("http://collectionofbestporn.com/most-recent*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('collectionofbestporn.com/')

    def parse_soup(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # parce video page
        video = soup.find('video')
        if video is not None:
            urls = UrlList()
            for source in _iter(video.find_all('source')):
                urls.add(source.attrs['res'], get_url(source.attrs['src'],base_url))
            result.set_video(urls.get_media_data(-1))

            for tag_container in _iter(soup.find_all('div', {'class':'tags-container'})):
                for href in _iter(tag_container.find_all('a')):
                    if href.string is not None:
                        result.add_control(ControlInfo(str(href.string), get_url(href.attrs['href'],base_url)))
            return result

        # parce thumbnail page
        for thumbnail in soup.find_all('div',{'class':'video-thumb'}):
            href=get_url(thumbnail.a.attrs['href'],base_url)
            description=thumbnail.a.img.attrs['alt']
            thumb_url = get_url(thumbnail.img.attrs['src'], base_url)

            duration = thumbnail.find('span', {'class': "time"})
            dur_time= '' if duration is None else str(duration.string)

            quality = thumbnail.find('span', {'class': "quality"})
            qual = '' if quality is None else str(quality.string)

            result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                       labels=[{'text':dur_time, 'align':'top right'},
                                               {'text':description, 'align':'bottom center'},
                                               {'text':qual,'align':'top left'}]))

        tags=soup.find('ul', {'class': 'drop2 hidden-xs'})
        if tags is not None:
            for tag in tags.find_all('a'):
                result.add_control(ControlInfo(str(tag.string).strip(), get_url(tag.attrs['href'],base_url)))

        pagination=soup.find('ul', {'class': 'pagination'})
        if pagination is not None:
            for page in pagination.find_all('a'):
                if page.string.isdigit():
                    result.add_page(ControlInfo(page.string, get_url(page.attrs['href'],base_url)))

        return result

if __name__ == "__main__":
    pass
