__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from bs4 import BeautifulSoup

class VERvideoSoupSite(BaseSite):
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

    def parse_index_file(self, fname, base_url=URL()):
        result = ParseResult()

        with open(fname,encoding='utf-8', errors='ignore') as fd:
            soup=BeautifulSoup(fd, "html.parser")

            video = soup.find('div',{'class':'video-container'})
            if video is not None:
                urls = UrlList()
                for source in video.find_all('source'):
                    urls.add(source.attrs['res'], self.get_url(source.attrs['src'],base_url))
                result.set_video(urls.get_media_data(-1))

                user=soup.find('div', {'class':'pull-left user-container'})
                if user is not None:
                    user_strings = [string for string in user.stripped_strings]
                    label='"{0} {1}"'.format(user_strings[0],user_strings[1])
                    href=user.find('a', href=lambda x: '#' not in x)
                    result.add_control(ControlInfo(label, self.get_url(href.attrs['href']+'/videos',base_url)))

                tags=soup.find_all('div', {'class':'m-t-10 overflow-hidden'})
                if tags is not None:
                    for item in tags:
                        hrefs=item.find_all('a')
                        for href in hrefs:
                            if href.string is not None:
                                result.add_control(ControlInfo(str(href.string), self.get_url(href.attrs['href'],base_url)))
                return result

            for thumbnail in soup.find_all('div',{'class':['well well-sm hover', 'channelContainer']}):
                href=self.get_url(thumbnail.a.attrs['href'],base_url)
                description=thumbnail.a.img.attrs['alt']
                thumb_url = self.get_url(thumbnail.img.attrs['src'], base_url)

                duration = thumbnail.find('div', {'class': "duration"})
                dur_time=''
                if duration is not None:
                    dur_time=duration.stripped_strings.__next__()

                result.add_thumb(ThumbInfo(thumb_url=thumb_url,href=href,description=description, duration=dur_time, show_description=True))

            tags=soup.find('ul', {'class': 'drop2 hidden-xs'})
            if tags is not None:
                for tag in tags.find_all('a'):
                    result.add_control(ControlInfo(str(tag.string).strip(), self.get_url(tag.attrs['href'],base_url)))

            pagination=soup.find('ul', {'class': 'pagination'})
            if pagination is not None:
                for page in pagination.find_all('a'):
                    if page.string.isdigit():
                        result.add_page(ControlInfo(page.string, self.get_url(page.attrs['href'],base_url)))

        result.set_caption_visible(True)
        return result

if __name__ == "__main__":
    pass
