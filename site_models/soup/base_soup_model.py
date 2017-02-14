__author__ = 'Vit'

from bs4 import BeautifulSoup

from base_classes import URL
from site_models.base_site_model import BaseSite, ParseResult

def _iter(source):
    if source is None:
        return []
    else:
        return source

class BaseSoupSite(BaseSite):
    def text_color(self):
        return 'mediumvioletred'

    def parse_index_file(self, fname, base_url=URL())->ParseResult:
        result = ParseResult()
        with open(fname, encoding='utf-8', errors='ignore') as fd:
            soup = BeautifulSoup(fd, "html.parser")
            self.parse_soup(soup, result, base_url)
        return result

    def parse_soup(self, soup:BeautifulSoup, result:ParseResult, base_url:URL):
        if self.parse_video(soup,result,base_url):
            self.parse_video_tags(soup,result,base_url)
            return

        if self.parse_pictures(soup,result,base_url):
            self.parse_pictures_tags(soup,result,base_url)
            return

        if self.parse_thumbs(soup,result,base_url):
            self.parse_thumbs_tags(soup,result,base_url)
            self.parse_pagination(soup,result,base_url)


    def parse_thumbs(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return False

    def parse_video(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return False

    def parse_pictures(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return False

    def parse_pagination(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return False

    def parse_thumbs_tags(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return False

    def parse_video_tags(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return False

    def parse_pictures_tags(self,soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return False


if __name__ == "__main__":
    pass
