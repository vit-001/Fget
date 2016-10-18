__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo


def get_href(txt, base):
    table = [('%3A', ':'),
             ('%2F', '/')]
    # print(txt)

    for i in table:
        txt = txt.replace(i[0], i[1])

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
        result = base + txt

    return result


def _del_thumb(txt=''):
    t = txt.rpartition('/')
    return t[0] + '/' + t[2].replace('t_', '')


class FPSite(BaseSite):
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        super().__init__(model, base_addr)
        self.accepted_sites = ['freeporn.hu/']

    def start_button_name(self):
        return "FP"

    def startpage(self):
        return URL("http://freeporn.hu/owngalleries")

    def can_accept_index_file(self, base_url=URL()):
        for site in self.accepted_sites:
            if base_url.contain(site):
                return True
        return False

    def parse_index_file(self, fname, base_url=URL()):
        print(base_url.get(), base_url.domain())
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'ogpost'),
                                                ('div', 'class', 'post300'),
                                                ('div', 'class', 'galelement')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: get_href(x, base_url.domain()))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('span', 'class', 'pager'),
                                                      ('div', 'class', 'pager')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        startpage_href_rule = ParserRule()
        startpage_href_rule.add_activate_rule_level([('div', 'id', 'right')])
        startpage_href_rule.add_activate_rule_level([('div', 'class', 'rightbox')])
        startpage_href_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(startpage_href_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'galcontentpics')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: _del_thumb(text))
        parser.add_rule(picture_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult(self)

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result(['href', 'src']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href'] + '*'),
                                           description=item.get('alt', '')))

            for item in startpage_href_rule.get_result(['href', 'data']):
                if item['href'].startswith('/'):
                    result.add_control(ControlInfo(item['data'], URL(base_url.domain() + item['href'] + '*')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'] + '*')))

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result(['src']):
                result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg' % i))
                i += 1

        return result




