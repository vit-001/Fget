__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


def get_href(txt, base):
    table = [('%3A', ':'),
             ('%2F', '/'),
             ('%3F', '?'),
             ('%26', '&'),
             ('%3D', '=')]
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
        result = base + txt

    for i in table:
        result = result.replace(i[0], i[1])

    # print(result)

    return result


def _del_thumb(txt=''):
    t = txt.rpartition('/')
    return t[0] + '/' + t[2].replace('_girl_', '_big_')


class DSUSite(BaseSite):
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        super().__init__(model, base_addr)
        self.accepted_sites = ['deffki.su/']

    def start_button_name(self):
        return "DSU"

    def startpage(self):
        return URL("http://www.deffki.su/")

    def can_accept_index_file(self, base_url=URL()):
        for site in self.accepted_sites:
            if base_url.contain(site):
                return True
        return False

    def parse_index_file(self, fname, base_url=URL()):
        print(base_url.get(), base_url.domain())
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'lady')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + '/' + x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'nav_link')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + '/' + x)
        parser.add_rule(startpage_pages_rule)

        startpage_nav_rule = ParserRule()
        startpage_nav_rule.add_activate_rule_level([('td', 'class', 'nav')])
        startpage_nav_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(startpage_nav_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('td', 'align', 'center')])
        picture_rule.add_process_rule_level('a', {'href'})
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: _del_thumb(text))
        parser.add_rule(picture_rule)

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

            for item in startpage_nav_rule.get_result(['href', 'data']):
                if item['href'].startswith("http://www.deffki.su/"):
                    result.add_control(ControlInfo(item['data'], URL(item['href'] + '*')))

        if base_url.contain('?go=gal&id='):
            result.set_type('pictures')
            dirname = self.base_addr + base_url.get_path() + '/' + base_url.get().rpartition('=')[2] + '/'
            result.set_gallery_path(dirname)
            i = 1
            for f in picture_rule.get_result(['src', 'href']):
                if not f['href'].startswith('prv.php?id='): continue
                if not f['src'].startswith('http://'): continue
                # print(f['src'])
                result.add_full(FullPictureInfo(abs_href=URL(f['src']), abs_name=dirname + '%03d.jpg' % i))
                i += 1

        return result
