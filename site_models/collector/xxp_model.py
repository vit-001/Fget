__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class XXPSite(BaseSite):
    def start_button_name(self):
        return "XXP"

    def startpage(self):
        return URL("http://xxx-porno.net/?cat=5*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('xxx-porno.net/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('td', 'class', 'blokth')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + '/' + x + '*')
        startpage_rule.set_attribute_modifier_function('src', lambda x: base_url.domain() + '/' + x + '*')
        parser.add_rule(startpage_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('td', 'class', 'text2')])
        startpage_hrefs_rule.add_activate_rule_level([('div', 'id', 'div3')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + '/' + x + '*')
        parser.add_rule(startpage_hrefs_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('td', 'class', 'archives')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + '/' + x + '*')
        # picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('thumb', 'origin'))
        parser.add_rule(startpage_pages_rule)

        picture_base_rule = ParserRule()
        picture_base_rule.add_activate_rule_level([('td', 'height', '500')])
        picture_base_rule.add_process_rule_level('a', set())
        picture_base_rule.add_process_rule_level('img', {'src'})
        picture_base_rule.set_attribute_modifier_function('src', lambda x: base_url.domain() + '/' + x)
        parser.add_rule(picture_base_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('td', 'class', 'archives')])
        picture_rule.add_process_rule_level('a', {'href'})
        picture_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('thumb', 'origin'))
        parser.add_rule(picture_rule)
        #
        picture_tags_rule = ParserRule()
        picture_tags_rule.add_activate_rule_level([('span', 'class', 'text2')])
        picture_tags_rule.add_process_rule_level('a', {'href'})
        picture_tags_rule.set_attribute_modifier_function('href', lambda x: x + '*')
        parser.add_rule(picture_tags_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult(self)

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                if item['href'].rfind('?cat=') != -1:
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))

            return result

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')

            result.set_picture_collector(XXPSitePictureCollector())

            dirname = self.base_addr.rstrip('/') + URL(picture_base_rule.get_result()[0]['src']).get_path()
            result.set_gallery_path(dirname)

            i = 1
            result.add_full(FullPictureInfo(abs_href=base_url, abs_name=dirname + '%03d.jpg' % i))

            for f in picture_rule.get_result():
                i += 1
                result.add_full(FullPictureInfo(abs_href=URL(f['href']), abs_name=dirname + '%03d.jpg' % i))

            for item in picture_tags_rule.get_result(['href', 'data']):
                if item['href'].rfind('?cat=') != -1:
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


class XXPSitePictureCollector(PictureCollector):
    def parse_index(self, request, url=URL()):
        parser = SiteParser()

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('td', 'height', '500')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda x: url.domain() + '/' + x)
        parser.add_rule(picture_rule)

        for data in request:
            parser.feed(data.decode(encoding="utf-8", errors="ignore"))

        return picture_rule.get_result()[0]['src']
