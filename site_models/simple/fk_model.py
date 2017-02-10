__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class FKSite(BaseSite):
    def start_button_name(self):
        return "FK"

    def startpage(self):
        return URL("http://fuskator.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('fuskator.com/')

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://') or txt.startswith('https://'):
            return txt
        if txt.startswith('/'):
            return 'http://' + base_url.domain() + txt
        return ''

    def parse_index_file(self, fname, base_url=URL()):
        # print(base_url)
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumblinks')])
        # startpage_rule.add_process_rule_level('div', {})
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url) + '*')
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url) + '*')
        parser.add_rule(startpage_rule)

        tags_rule = ParserRule()
        tags_rule.add_activate_rule_level([('div', 'id', 'divTags')])
        tags_rule.add_process_rule_level('a', {'href'})
        tags_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(tags_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('td', 'class', 'pages')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        picture_base_addr_rule = ParserRule()
        picture_base_addr_rule.add_activate_rule_level([('div', 'class', 'imagelinks')])
        picture_base_addr_rule.add_process_rule_level('script', {})
        picture_base_addr_rule.set_attribute_filter_function('data', lambda x: 'unescape' in x)
        parser.add_rule(picture_base_addr_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'imagelinks')])
        picture_rule.add_process_rule_level('script', {})
        picture_rule.set_attribute_filter_function('data', lambda x: "'src'" in x)
        parser.add_rule(picture_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if len(picture_base_addr_rule.get_result()) > 0:
            result.set_type('pictures')
            base = \
            picture_base_addr_rule.get_result()[0]['data'].replace('%2f', '/').partition("unescape('//")[2].partition(
                "'")[0]
            # print(base)
            i = 1
            for f in picture_rule.get_result():
                picname = f['data'].partition("+'")[2].partition("'")[0]
                # print(picname)
                result.add_full(FullPictureInfo(abs_href=URL(base + picname + '*'), rel_name='%03d.jpg' % i))
                i += 1

            for item in tags_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                # print(item)
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),
                              popup=item.get('alt', '')))

            for item in tags_rule.get_result(['href', 'data']):
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
