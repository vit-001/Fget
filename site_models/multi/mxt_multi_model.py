__author__ = 'Vit'

from urllib.parse import urlparse

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo


def get_href(txt):
    if '&' in txt or '?' in txt:
        txt = txt.replace('?', '&')
        s = txt.split('&')
        return s[0]
    else:
        return txt


class MXTmultiSite(BaseSite):
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        super().__init__(model, base_addr)
        self.accepted_sites = ['matrixteens.com/', 'xmodelpics.com/', 'metartgirlz.com/',
                               'femjoygirlz.com/', 'xteengirlz.com/', 'xhotgirlz.com/',
                               'xftvgirlz.com/', 'amourgirlz.com/', 'xwetgirlz.com/',
                               'xwowgirls.com/']

    def start_button_name(self):
        return "MXTmulti"

    def startpage(self):
        return URL("http://matrixteens.com/")

    def can_accept_index_file(self, base_url=URL()):
        for site in self.accepted_sites:
            if base_url.contain(site):
                return True
        return False

    def parse_index_file(self, fname, base_url=URL()):
        site_url = 'http://' + urlparse(base_url.get())[1].strip('/')
        print('site url=', site_url)

        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'bodycontainer')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt', 'class'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: site_url + get_href(x))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        # startpage_pages_rule.add_activate_rule_level([('div', 'class', 'bodycontainer')])
        startpage_pages_rule.add_activate_rule_level([('td', 'align', 'right')])
        startpage_pages_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: site_url + x)
        parser.add_rule(startpage_pages_rule)

        site_rule = ParserRule()
        site_rule.add_activate_rule_level([('div', 'class', 'headerlinetext')])
        site_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(site_rule)

        picture_trigger_rule = ParserRule()
        picture_trigger_rule.add_activate_rule_level([('a', 'class', 'fancybox')])
        picture_trigger_rule.add_process_rule_level('img', {'src'})
        parser.add_rule(picture_trigger_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'bodycontainer')])
        picture_rule.add_process_rule_level('a', {'href', 'class'})
        picture_rule.add_process_rule_level('img', {'alt'})
        parser.add_rule(picture_rule)

        picture_href_rule = ParserRule()
        picture_href_rule.add_activate_rule_level([('div', 'class', 'bodycontainer')])
        picture_href_rule.add_activate_rule_level([('h2', 'style', 'font-size:18px')])
        picture_href_rule.add_process_rule_level('a', {'href'})
        picture_href_rule.set_attribute_modifier_function('href', lambda x: site_url + x)
        parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult(self)

        if len(picture_trigger_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result(['href', 'alt', 'class']):
                if f['class'] == 'fancybox':
                    result.add_full(FullPictureInfo(abs_href=URL(f['href']), rel_name='%03d.jpg' % i))
                    i += 1

            for item in picture_href_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(text=item['data'], url=URL(item['href'])))

            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result(['href', 'src', 'class']):
                if item['class'] == 'thumb':
                    result.add_thumb(
                        ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in site_rule.get_result(['href', 'data']):
                result.add_site(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_pages_rule.get_result(['href', 'data', 'title']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
    # model = BESite()
    #
    # print('http://www.bravoerotica.com/')
    # load("http://www.bravoerotica.com/", 'e:/out/index.html')
    # model.parse_index_file('e:/out/index.html')
    #
    # print('http://www.bravoerotica.com/torrid-art/elisa/the-promise-1/')
    # load("http://www.bravoerotica.com/torrid-art/elisa/the-promise-1/", 'e:/out/index.html')
    # model.parse_index_file('e:/out/index.html')
    #
    # print('http://torrid-art.bravoerotica.com/')
    # load("http://torrid-art.bravoerotica.com/", 'e:/out/index.html')
    # model.parse_index_file('e:/out/index.html')
    #
    # print('http://www.bravoerotica.com/go/torrid-art/')
    # load("http://www.bravoerotica.com/go/torrid-art/", 'e:/out/index.html')
    # model.parse_index_file('e:/out/index.html')




