__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


def get_href(txt):
    # print(txt)
    if '&' in txt or '?' in txt:
        txt = txt.replace('?', '&')
        s = txt.split('&')
        # print(s)
        for str in s:
            if str.startswith('url='):
                url = str[4:]
                return url
    else:
        return txt


class BBSite(BaseSite):
    def start_button_name(self):
        return "BB"

    def startpage(self):
        return URL("http://www.babesandbitches.net/galleries")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('babesandbitches.net/')

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt + '*'
        return base_url.get().partition('?')[0] + txt + '*'

    def parse_index_file(self, fname, base_url=URL()):
        print(base_url.domain())
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'refpost')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'nav')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'gallery')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src', 'class'})
        picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('/tn_', '/'))
        parser.add_rule(picture_rule)

        picture_href_rule = ParserRule()
        picture_href_rule.add_activate_rule_level([('div', 'class', 'tags')])
        picture_href_rule.add_process_rule_level('a', {'href'})
        picture_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if len(startpage_rule.get_result()) > 0:
            # print('Startpage rule')
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href'] + '*'),
                              popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result(['src', 'class']):
                # print(f)
                result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg' % i))
                i += 1

            for f in picture_href_rule.get_result():
                # print(f)
                result.add_control(ControlInfo(f['data'].replace(',', ''), URL(f['href'])))

        return result


if __name__ == "__main__":
    pass
