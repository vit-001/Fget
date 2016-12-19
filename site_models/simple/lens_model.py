__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class LENSSite(BaseSite):
    def start_button_name(self):
        return "LENS"

    def startpage(self):
        return URL("http://xxxlens.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('xxxlens.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'post')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'paginator')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(startpage_pages_rule)

        href_rule = ParserRule()
        href_rule.add_activate_rule_level([('div', 'class', 'sidebar')])
        href_rule.add_process_rule_level('li', {'class'})
        href_rule.add_process_rule_level('a', {'href', 'title'})
        href_rule.set_attribute_modifier_function('title', lambda text: text.replace('View all posts filed under ', ''))
        parser.add_rule(href_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('dl', 'class', 'gallery-item')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('-180x240', ''))
        parser.add_rule(picture_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult(self)

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result(['src']):
                result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg' % i))
                i += 1
            return result

        if len(startpage_rule.get_result()) > 0:
            # print('Startpage rule')
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in href_rule.get_result(['class', 'href', 'title']):
                # print(item['title'])
                result.add_control(ControlInfo(item['title'], URL(item['href'])))

        return result
