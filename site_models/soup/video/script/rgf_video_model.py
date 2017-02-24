__author__ = 'Vit'

from bs4 import BeautifulSoup

from base_classes import UrlList
from loader.base_loader import URL
from site_models.base_site_model import ParseResult, ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite, _iter
from site_models.util import quotes


class RGFvideoSite(BaseSoupSite):
    def start_button_name(self):
        return "RGFvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Most_Recent=URL('http://www.realgfporn.com/most-recent/'),
                    Categories=URL('http://www.realgfporn.com/channels/'),
                    Longest=URL('http://www.realgfporn.com/longest/'),
                    Most_Viewed=URL('http://www.realgfporn.com/most-viewed/'),
                    Top_Rated=URL('http://www.realgfporn.com/top-rated/')
                    )

    def startpage(self):
        return URL("http://www.realgfporn.com/most-recent/", test_string='Real GF Porn')

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('realgfporn.com/')

    def parse_thumbs(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'post'})):
            href = URL(thumbnail.a.attrs['href'], base_url=base_url)
            description = thumbnail.a.img.attrs['alt']
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=base_url)

            duration = thumbnail.find('b', {'class': 'post-duration'})
            dur_time = '' if duration is None else str(duration.string)

            result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                       labels=[{'text': dur_time, 'align': 'top right'},
                                               {'text': description, 'align': 'bottom center'}]))

    def parse_thumbs_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        tags_container = soup.find('div', {'class': 'site-cats'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a')):
                result.add_control(ControlInfo(str(tag.string), URL(tag.attrs['href'], base_url=base_url)))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        content = soup.find('div', {'id': 'mediaspace'})
        if content is not None:
            urls = UrlList()
            script = content.find('script', text=lambda x: 'jwplayer(' in x)
            if script is not None:
                data = str(script.string).replace(' ', '')
                file = quotes(data, 'file:"', '"')
                urls.add('DEFAULT', URL(file, base_url=base_url))

                result.set_video(urls.get_media_data())

    def parse_video_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        tags = list()
        for item in _iter(soup.find_all('div', {'class': 'more-content'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    if '/user/' in href.attrs['href']:
                        result.add_control(
                            ControlInfo(str(href.string), URL(href.attrs['href'], base_url=base_url),
                                        text_color='blue'))
                    else:
                        tags.append(ControlInfo(str(href.string), URL(href.attrs['href'], base_url=base_url)))

        for item in tags:
            result.add_control(item)


if __name__ == "__main__":
    pass
