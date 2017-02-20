__author__ = 'Vit'

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


class TOPSite(BaseSite):
    def start_button_name(self):
        return "TOP"

    def startpage(self):
        return URL("http://www.tomorrowporn.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('tomorrowporn.com/')

    def get_start_button_menu_text_url_dict(self):
        return dict(Movies=URL('http://www.tomorrowporn.com/porn-movies/'),
                    Stars=URL('http://www.tomorrowporn.com/porn-stars/'),
                    Pics=URL('http://www.tomorrowporn.com/'),
                    LatestUpdates=URL('http://www.tomorrowporn.com/latest_updates.html'),
                    )

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumbs'),
                                                ('div', 'class', 'movie_thumbs')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', get_href)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'head')])
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pages')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: 'http://www.tomorrowporn.com' + x)
        parser.add_rule(startpage_pages_rule)

        href_rule = ParserRule()
        href_rule.add_activate_rule_level([('ul', 'class', 'sub_thumb_list')])
        href_rule.add_process_rule_level('a', {'href'})
        href_rule.add_process_rule_level('img', {'src', 'alt'})
        href_rule.set_attribute_modifier_function('href', get_href)
        parser.add_rule(href_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'thumb_box'),
                                              ('div', 'class', 'thumb_box bottom_corners'),
                                              ('div', 'class', 'thumb_box top_corners')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('t', ''))
        parser.add_rule(picture_rule)

        picture_href_rule = ParserRule()
        picture_href_rule.add_activate_rule_level([('div', 'class', 'menus')])
        picture_href_rule.add_process_rule_level('h2', set())
        picture_href_rule.add_process_rule_level('a', {'href', 'title'})
        parser.add_rule(picture_href_rule)

        for s in open(fname, encoding='utf-8'):
            parser.feed(s)

        result = ParseResult()

        if len(startpage_rule.get_result()) > 0:
            # result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        if len(href_rule.get_result()) > 0:
            # result.set_type('hrefs')
            for item in href_rule.get_result():
                # print (item)
                if 'src' in item:
                    result.add_thumb(
                        ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

        if len(picture_rule.get_result()) > 0:
            # result.set_type('pictures')
            for f in picture_rule.get_result():
                result.add_full(FullPictureInfo(rel_name=f['src']))

            for f in picture_href_rule.get_result():
                # print(f)
                result.add_control(ControlInfo(f['title'], URL(f['href'])))

        return result
