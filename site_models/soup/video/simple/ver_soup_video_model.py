__author__ = 'Vit'
from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite,_iter
from site_models.util import get_href,get_url,quotes

class VERvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "VERvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Most_Recsent=URL('https://www.veronicca.com/videos?o=mr*'),
                    Videos_Most_Viewed=URL('https://www.veronicca.com/videos?o=mv*'),
                    Videos_Most_Commented=URL('https://www.veronicca.com/videos?o=md*'),
                    Videos_Top_Rated=URL('https://www.veronicca.com/videos?o=tr*'),
                    Videos_Top_Favorited=URL('https://www.veronicca.com/videos?o=tf*'),
                    Videos_Longest=URL('https://www.veronicca.com/videos?o=lg*'),
                    Channels=URL('https://www.veronicca.com/channels*')
                    )

    def startpage(self):
        return URL("https://www.veronicca.com/videos?o=mr*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('veronicca.com/')

    def parse_soup(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # parce video page
        video = soup.find('div',{'class':'video-container'})
        if video is not None:
            urls = UrlList()
            for source in _iter(video.find_all('source')):
                urls.add(source.attrs['res'], get_url(source.attrs['src'],base_url))
            result.set_video(urls.get_media_data(-1))

            user=soup.find('div', {'class':'pull-left user-container'})
            if user is not None:
                user_strings = [string for string in user.stripped_strings]
                label='{0} {1}'.format(user_strings[0],user_strings[1])
                href=user.find('a', href=lambda x: '#' not in x)
                result.add_control(ControlInfo(label, get_url(href.attrs['href']+'/videos',base_url),text_color='blue'))

            for tag_container in _iter(soup.find_all('div', {'class':'m-t-10 overflow-hidden'})):
                for href in _iter(tag_container.find_all('a')):
                    if href.string is not None:
                        result.add_control(ControlInfo(str(href.string), get_url(href.attrs['href'],base_url)))
            return result

        # parce thumbnail page
        for thumbnail in soup.find_all('div',{'class':['well well-sm hover', 'channelContainer']}):
            href=get_url(thumbnail.a.attrs['href'],base_url)
            description=thumbnail.a.img.attrs['alt']
            thumb_url = get_url(thumbnail.img.attrs['src'], base_url)

            duration = thumbnail.find('div', {'class': "duration"})
            dur_time= '' if duration is None else duration.stripped_strings.__next__()

            result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                       labels=[{'text':dur_time, 'align':'top right'},{'text':description, 'align':'bottom center'}]))

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
