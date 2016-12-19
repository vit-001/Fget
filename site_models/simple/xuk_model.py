__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class XUKSite(BaseSite):
    def start_button_name(self):
        return "XUK"

    def startpage(self):
        return URL("http://xuk.ru/erotic")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('xuk.ru/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'item photo-item')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'justified-pagination')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(startpage_pages_rule)

        startpage_tags_rule = ParserRule()
        startpage_tags_rule.add_activate_rule_level([('ul', 'class', 'tags')])
        startpage_tags_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(startpage_tags_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'photo-item')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('thumb', 'origin'))
        parser.add_rule(picture_rule)

        picture_model_rule = ParserRule()
        picture_model_rule.add_activate_rule_level([('div', 'class', 'block attached-model')])
        picture_model_rule.add_process_rule_level('a', {'href'})
        picture_model_rule.add_process_rule_level('img', {'alt'})
        parser.add_rule(picture_model_rule)

        picture_tags_rule = ParserRule()
        picture_tags_rule.add_activate_rule_level([('div', 'class', 'block gallery-tags')])
        picture_tags_rule.add_activate_rule_level([('ul', 'class', 'tags')])
        picture_tags_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(picture_tags_rule)

        for s in open(fname, encoding='utf-8'):
            parser.feed(s)

        result = ParseResult(self)

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_tags_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result():
                result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg' % i))
                i += 1

            for item in picture_model_rule.get_result(['href', 'alt']):
                result.add_control(ControlInfo(item['alt'], URL(item['href'] + '/galleries')))

            for item in picture_tags_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result
