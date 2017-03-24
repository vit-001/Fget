__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


def get_href(txt):
    s = txt.split('&')
    for str in s:
        if str.startswith('url='):
            url = str[4:]
            return url


class BEPSite(BaseSite):
    def start_button_name(self):
        return "BN"

    def startpage(self):
        return URL("http://www.bravonude.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('bravonude.com/')

    def get_start_button_menu_text_url_dict(self):
        return dict(Pictures=URL('http://www.bravonude.com/'),
                    Movies=URL('http://www.bravonude.com/erotica-videos/'))

    def process_picture_address(self, text):
        # print(text, '->','http://www.bravonude.com'+text.replace('t.jpg','.jpg'))
        return 'http://www.bravonude.com' + text.replace('t.jpg', '.jpg')

    def get_href(self, txt):
        # print(txt)
        if '&' in txt or '?' in txt:
            txt = txt.replace('?', '&')
            s = txt.split('&')
            # print(s)
            for str in s:
                if str.startswith('http://'):
                    return str
                if str.startswith('url='):
                    url = str[4:]
                    return url
        else:
            return txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumbs200'),
                                                ('div', 'class', 'thumbs300')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', self.get_href)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'menu')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        startpage_pages_rule.set_attribute_filter_function('href', lambda txt: '/st/' in txt)
        parser.add_rule(startpage_pages_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'gallery-thumbs')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', self.process_picture_address)
        parser.add_rule(picture_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            for f in picture_rule.get_result():
                result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name=f['src'].rpartition('/')[2]))
            return result

        if len(startpage_rule.get_result()) > 0:
            # print('Startpage rule')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))
                #
                # for item in startpage_hrefs_rule.get_result(['href', 'data']):
                #     result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result
