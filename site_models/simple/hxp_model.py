__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


def get_href(txt):
    if '&' in txt or '?' in txt:
        txt = txt.replace('?', '&')
        s = txt.split('&')
        return s[0]
    else:
        return txt


class HXPSite(BaseSite):
    def start_button_name(self):
        return "HXP"

    def startpage(self):
        return URL("http://hotxpix.net/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('hotxpix.net/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'grid_1')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: 'http://hotxpix.net' + get_href(x))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
        startpage_pages_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: 'http://hotxpix.net' + x)
        parser.add_rule(startpage_pages_rule)

        picture_trigger_rule = ParserRule()
        picture_trigger_rule.add_activate_rule_level([('div', 'class', 'grid_4 gal dbg')])
        picture_trigger_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(picture_trigger_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'grid_4 gal dbg')])
        picture_rule.add_process_rule_level('a', {'href'})
        picture_rule.add_process_rule_level('img', {'src'})
        parser.add_rule(picture_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult(self)

        if len(picture_trigger_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result(['href', 'src']):
                if f['href'].endswith('.jpg'):
                    result.add_full(FullPictureInfo(abs_href=URL(f['href']), rel_name='%03d.jpg' % i))
                    i += 1

            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data', 'title']):
                result.add_page(ControlInfo(item['title'], URL(item['href'])))

        return result


if __name__ == "__main__":
    from lib.file_loader import load

    model = HXPSite()

    print('http://hotxpix.net/gallery/teenslovehugecocks-trade-presents-willow-hayes-in-pussy-willow/index.html')
    load("http://hotxpix.net/gallery/teenslovehugecocks-trade-presents-willow-hayes-in-pussy-willow/index.html",
         'e:/out/index.html')
    model.parse_index_file('e:/out/index.html', 'http://hotxpix.net').print_result()

    # print('http://lustimages.com/photo/hot-summer-love/')
    # load("http://lustimages.com/photo/hot-summer-love/", 'e:/out/index.html')
    # model.parse_index_file('e:/out/index.html').print_result()
