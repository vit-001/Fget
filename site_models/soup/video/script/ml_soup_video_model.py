__author__ = 'Vit'

from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite,_iter
from site_models.util import get_href,get_url,quotes

class MLvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "MLvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Galleries_Recently_Updated=URL('http://motherless.com/galleries/updated*'),
                    Galleries_Most_Viewed=URL('http://motherless.com/galleries/viewed*'),
                    Galleries_Most_Favorited=URL('http://motherless.com/galleries/favorited*'),
                    Videos_Recent=URL('http://motherless.com/videos/recent*'),
                    Videos_Most_Viewed=URL('http://motherless.com/videos/viewed*'),
                    Videos_Most_Favoritede=URL('http://motherless.com/videos/favorited*'),
                    Videos_Popular=URL('http://motherless.com/videos/popular*'),
                    Videos_Live=URL('http://motherless.com/live/videos*'),
                    Videos_All_Time_Most_Viewed=URL('http://motherless.com/videos/all/viewed*'),
                    Videos_All_Time_Most_Favorited=URL('http://motherless.com/videos/all/favorited*'),
                    Videos_Archived=URL('http://motherless.com/videos/archives*'))

    def startpage(self):
        return URL("http://motherless.com/videos/recent?page=1*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('motherless.com/')

    def parse_thumbs(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        for item in _iter(soup.find_all('div', {'class': ['content-inner']})):
            for thumbnail in _iter(item.find_all('div', {'class': 'thumb'})):
                href = get_url(thumbnail.a.attrs['href'], base_url)
                thumb_url = get_url(thumbnail.img.attrs['src'], base_url)

                duration = thumbnail.find('div', {'class': 'caption left'})
                dur_time = '' if duration is None else str(duration.string)

                caption = thumbnail.find('h2', {'class': 'caption title'})
                label = '' if caption is None else str(caption.string)

                user = thumbnail.find('a', {'class': 'caption left'})
                username = '' if user is None else str(user.string)

                if not 'x' in dur_time:
                    result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=label,
                                               labels=[{'text':dur_time, 'align':'top right'},
                                                       {'text':label, 'align':'bottom center'},
                                                       {'text': username, 'align': 'top left'}]))

    def parse_thumbs_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        tags = soup.find('div', {'class': 'dark-menu'})
        if tags is not None:
            for tag in _iter(tags.find_all('a')):
                result.add_control(ControlInfo(str(tag.string).strip(), get_url(tag.attrs['href'], base_url)))

    def get_pagination_container(self,soup:BeautifulSoup):
        return  soup.find('div', {'class': 'pagination_link'})

    def parse_video(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        content = soup.find('div', {'id': 'content'})
        if content is not None:
            urls = UrlList()
            script =content.find('script', text=lambda x: 'jwplayer(' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '')
                file = quotes(data, '"file":"', '"')
                urls.add('DEFAULT', get_url(file, base_url))
                result.set_video(urls.get_media_data())

    def parse_video_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # adding "user" to video
        user = soup.find('div', {'class': 'thumb-member-username'})
        if user is not None:
            href = user.find('a').attrs['href']
            username = href.rpartition('/')[2]

            result.add_control(
                ControlInfo(username + ' uploads', URL('http://motherless.com/u/' + username + '*'), text_color='blue'))
            result.add_control(
                ControlInfo(username + ' gals', URL('http://motherless.com/galleries/member/' + username + '*'),
                            text_color='blue'))

        # adding tags to video
        for item in _iter(soup.find_all('div', {'id': 'media-tags-container'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    result.add_control(
                        ControlInfo(str(href.string), get_url(href.attrs['href'], base_url)))

if __name__ == "__main__":
    pass
