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

    def parse_index_file(self, fname, base_url=URL()):
        result = ParseResult()
        with open(fname, encoding='utf-8', errors='ignore') as fd:
            soup = BeautifulSoup(fd, "html.parser")
            result=self.parse_soup(soup, result, base_url)
        return result

    def parse_soup(self, soup:BeautifulSoup, result:ParseResult, base_url:URL):
        return result


if __name__ == "__main__":
    pass
