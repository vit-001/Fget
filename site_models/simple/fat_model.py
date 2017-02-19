__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


def get_href(txt):
    table = [('%3A', ':'),
             ('%2F', '/')]
    # print(txt)
    result = ''
    if '&' in txt or '?' in txt:
        txt = txt.replace('?', '&')
        s = txt.split('&')
        # print(s)
        for str in s:
            if str.startswith('url='):
                url = str[4:]
                result = url
    else:
        result = txt

    for i in table:
        result = result.replace(i[0], i[1])

    return result


def _del_thumb(txt=''):
    t = txt.rpartition('/')
    return t[0] + '/' + t[2].replace('t_', '')


class FATSite(BaseSite):
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        super().__init__(model, base_addr)
        self.accepted_sites = ['fineartteens.com/']

    def start_button_name(self):
        return "FAT"

    def startpage(self):
        return URL("http://fineartteens.com/")

    def can_accept_index_file(self, base_url=URL()):
        for site in self.accepted_sites:
            if base_url.contain(site):
                return True
        return False

    def parse_index_file(self, fname, base_url=URL()):
        print(base_url.get(), base_url.domain())
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'post'),
                                                ('div', 'class', 'post300')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: get_href(x))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'id', 'pager')])
        startpage_pages_rule.add_activate_rule_level([('div', 'id', 'pc')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'id', 'cc')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src', 'title'})
        picture_rule.set_attribute_modifier_function('src', lambda text: _del_thumb(text))
        parser.add_rule(picture_rule)

        picture_href_rule = ParserRule()
        picture_href_rule.add_activate_rule_level([('div', 'id', 'cc')])
        picture_href_rule.add_activate_rule_level([('div', 'class', 'shorttext')])
        picture_href_rule.add_process_rule_level('a', {'href', 'alt'})
        parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result(['href', 'src']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href'] + '*'),
                                           popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'] + '*')))

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result(['src', 'title']):
                result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg' % i))
                i += 1

            for f in picture_href_rule.get_result():
                if f['href'].startswith('/'):
                    result.add_control(ControlInfo(text=f['alt'], url=URL(base_url.domain() + f['href'])))

        return result
