__author__ = 'Vit'

from bs4 import BeautifulSoup

from loader.base_loader import URL
from loader.az_loader import AZLoader
from site_models.base_site_model import BaseSite, ParseResult, ControlInfo
from site_models.util import psp

def _iter(source):
    if source is None:
        return []
    else:
        return source

class BaseSoupSite(BaseSite):
    def text_color(self):
        print(self.startpage())
        if AZLoader.test_url_az(self.startpage()):
            return 'mediumvioletred'
        else:
            return 'green'

    def parse_index_file(self, fname, base_url=URL())->ParseResult:
        result = ParseResult()
        with open(fname, encoding='utf-8', errors='ignore') as fd:
            soup = BeautifulSoup(fd, "html.parser")
            self.parse_soup(soup, result, base_url)
        return result

    def parse_soup(self, soup:BeautifulSoup, result:ParseResult, base_url:URL):
        self.parse_video(soup,result,base_url)
        if result.is_video():
            self.parse_video_tags(soup,result,base_url)
            return

        self.parse_pictures(soup,result,base_url)
        if result.is_pictures():
            self.parse_pictures_tags(soup,result,base_url)
            return

        self.parse_thumbs(soup,result,base_url)
        if result.is_no_result():
            self.parse_others(soup,result,base_url)
        if result.is_hrefs():
            self.parse_thumbs_tags(soup,result,base_url)
            self.parse_pagination(soup,result,base_url)

    def parse_thumbs(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return

    def parse_others(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return

    def parse_video(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return

    def parse_pictures(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return

    def parse_pagination(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        container=self.get_pagination_container(soup)
        if container is not None:
            for page in container.find_all('a',{'href':True}):
                # psp(page.prettify())
                if page.string is not None and page.string.isdigit():
                    result.add_page(ControlInfo(page.string, URL(page.attrs['href'],base_url=base_url)))

    def get_pagination_container(self,soup:BeautifulSoup)->BeautifulSoup:
        return None

    def parse_thumbs_tags(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return

    def parse_video_tags(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return

    def parse_pictures_tags(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return


if __name__ == "__main__":
    pass
