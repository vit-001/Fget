__author__ = 'Vit'
from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite,_iter
from site_models.util import get_href,get_url,quotes,psp

class V24videoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "V24vid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Most_Recsent=URL('http://www.24videos.tv/latest-updates/'),
                    Videos_Most_Viewed=URL('http://www.24videos.tv/most-popular/'),
                    Videos_Top_Rated=URL('http://www.24videos.tv/top-rated/')
                    )

    def startpage(self):
        return URL("http://www.24videos.tv/latest-updates/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('24videos.tv/')

    def parse_thumbs(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        container=soup.find('div',{'class':'list-videos'})
        if container is not None:
            for thumbnail in _iter(container.find_all('div',{'class':'item'})):
                psp(thumbnail.prettify())

                href = get_url(thumbnail.a.attrs['href'], base_url)
                thumb_url = get_url(thumbnail.img.attrs['data-original'], base_url)
                label=thumbnail.img.attrs.get('alt','')

                duration = thumbnail.find('div', {'class': 'duration'})
                dur_time = '' if duration is None else str(duration.contents[-1])

                result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=label,
                                           labels=[{'text':dur_time, 'align':'top right'},
                                                   {'text':label, 'align':'bottom center'}]))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        content = soup.find('div', {'class': 'player'})
        if content is not None:
            urls = UrlList()
            script =content.find('script', text=lambda x: 'flashvars' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\n', '').replace('\t', '')
                flashvars = self.quotes(data,'flashvars={', '};').split(',')
                fv = dict()
                for flashvar in flashvars:
                    print(flashvar)
                    split = flashvar.partition(':')
                    fv[split[0]] = split[2].strip("'\"")
                files = dict()
                for f in fv:
                    if fv[f].startswith('http://') and fv[f].endswith('.mp4/'):
                        file = fv[f]
                        label = fv.get(f + '_text', f)
                        files[label] = file

                for key in sorted(files.keys(), reverse=True):
                    urls.add(key, URL(files[key]))

                result.set_video(urls.get_media_data())

if __name__ == "__main__":
    pass
