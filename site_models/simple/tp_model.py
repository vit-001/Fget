__author__ = 'Vit'

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


class TPSite(BaseSite):
    def start_button_name(self):
        return "TP"

    def startpage(self):
        return URL("http://www.teenport.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('teenport.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumbs_main'),
                                                ('div', 'class', 'content_box model_sub'),
                                                ('div', 'class', 'teen_girls_list'),
                                                ('div', 'class', 'gallery_box')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', get_href)
        parser.add_rule(startpage_rule)

        startpage_menu_rule = ParserRule()
        startpage_menu_rule.add_activate_rule_level([('div', 'class', 'head')])
        startpage_menu_rule.add_activate_rule_level([('ul', 'class', 'menu')])
        startpage_menu_rule.add_process_rule_level('a', {'href'})
        startpage_menu_rule.set_attribute_modifier_function('href', lambda x: x)
        parser.add_rule(startpage_menu_rule)

        archive_pages_rule = ParserRule()
        archive_pages_rule.add_activate_rule_level([('div', 'class', 'head')])
        archive_pages_rule.add_activate_rule_level([('span', '', '')])
        archive_pages_rule.add_process_rule_level('a', {'href'})
        archive_pages_rule.set_attribute_modifier_function('href', lambda x: 'http://www.teenport.com' + x)
        parser.add_rule(archive_pages_rule)

        model_href_rule = ParserRule()
        model_href_rule.add_activate_rule_level([('div', 'class', 'model_desc model_niche_desc')])
        model_href_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(model_href_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'thumb_box top_corners'),
                                              ('div', 'class', 'thumb_box bottom_corners')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('t', ''))
        parser.add_rule(picture_rule)

        picture_href_rule = ParserRule()
        picture_href_rule.add_activate_rule_level([('div', 'class', 'title')])
        picture_href_rule.add_process_rule_level('a', {'href', 'title'})
        parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_menu_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

            for item in model_href_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in archive_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            for f in picture_rule.get_result():
                result.add_full(FullPictureInfo(rel_name=f['src']))

            for f in picture_href_rule.get_result():
                result.add_control(ControlInfo(f['title'], URL(f['href'])))

        return result
