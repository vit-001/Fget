__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


def get_href(txt):
    if '&' in txt or '?' in txt:
        txt = txt.replace('?', '&')
        s = txt.split('&')
        for str in s:
            if str.startswith('url='):
                url = str[4:]
                return url
    else:
        return txt


class LISite(BaseSite):
    def start_button_name(self):
        return "LI"

    def startpage(self):
        return URL("http://lustimages.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('lustimages.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'galleries')])
        startpage_rule.add_process_rule_level('div', {})
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', get_href)
        parser.add_rule(startpage_rule)

        menu_rule = ParserRule()
        menu_rule.add_activate_rule_level([('div', 'class', 'menu-list')])
        menu_rule.add_process_rule_level('a', {'href'})
        menu_rule.set_attribute_modifier_function('href', lambda x: "http://lustimages.com" + x)
        parser.add_rule(menu_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagi')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: "http://lustimages.com" + x)
        parser.add_rule(startpage_pages_rule)

        picture_trigger_rule = ParserRule()
        picture_trigger_rule.add_activate_rule_level([('div', 'class', 'left-main')])
        picture_trigger_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(picture_trigger_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'gall')])
        picture_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(picture_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if len(picture_trigger_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result():
                result.add_full(FullPictureInfo(abs_href=URL(f['href']), rel_name='%03d.jpg' % i))
                i += 1

            for item in menu_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL("http://lustimages.com" + item['href']),
                              popup=item.get('alt', '')))

            for item in menu_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    from lib.file_loader import load

    model = LISite()

    print('http://lustimages.com/')
    load("http://lustimages.com/", 'e:/out/index.html')
    model.parse_index_file('e:/out/index.html', 'http://lustimages.com').print_result()

    # print('http://lustimages.com/photo/hot-summer-love/')
    # load("http://lustimages.com/photo/hot-summer-love/", 'e:/out/index.html')
    # model.parse_index_file('e:/out/index.html').print_result()
    #
    # print('http://torrid-art.bravoerotica.com/')
    # load("http://torrid-art.bravoerotica.com/", 'e:/out/index.html')
    # model.parse_index_file('e:/out/index.html')
    #
    # print('http://www.bravoerotica.com/go/torrid-art/')
    # load("http://www.bravoerotica.com/go/torrid-art/", 'e:/out/index.html')
    # model.parse_index_file('e:/out/index.html')
    #
