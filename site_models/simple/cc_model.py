__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class CCSite(BaseSite):
    def start_button_name(self):
        return "CC"

    def startpage(self):
        return URL("http://www.coedcherry.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('coedcherry.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('ul', 'class', 'thumbs'),
                                                ('ul', 'class', 'thumbs break')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('p', 'class', 'pagination')])
        startpage_pages_rule.add_process_rule_level('a', {'class', 'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        picture_trigger_rule = ParserRule()
        picture_trigger_rule.add_activate_rule_level([('head', '', '')])
        picture_trigger_rule.add_process_rule_level('meta', {'name'})
        parser.add_rule(picture_trigger_rule)

        picture_href_rule = ParserRule()
        picture_href_rule.add_activate_rule_level([('ul', 'class', 'options')])
        picture_href_rule.add_process_rule_level('a', {'href'})

        parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        pictures = False
        for item in picture_trigger_rule.get_result(['name']):
            if item['name'] == 'gallery-id':
                pictures = True

        if pictures:
            result.set_type('pictures')
            i = 1
            for f in startpage_rule.get_result():
                result.add_full(FullPictureInfo(abs_href=URL(f['href']), rel_name='%03d.jpg' % i))
                i += 1

            for f in picture_href_rule.get_result():
                # print(f)
                if not f['href'].startswith('http://'):
                    result.add_control(ControlInfo(f['data'], URL(base_url.domain() + f['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            # print('Startpage rule')
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data', 'class']):
                if item['class'] == 'page':
                    result.add_page(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
