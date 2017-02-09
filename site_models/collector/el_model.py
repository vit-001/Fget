__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class ELSite(BaseSite):
    def start_button_name(self):
        return "EL"

    def startpage(self):
        return URL("http://www.ero-lust.com/photos/latest/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('ero-lust.com/')

    def get_start_button_menu_text_url_dict(self):
        return dict(Latest_Video=URL('http://www.ero-lust.com/videos/latest/'),
                    Latest_Photos=URL('http://www.ero-lust.com/photos/latest/'),
                    Channels=URL('http://www.ero-lust.com/videos/channels/'),
                    Top_rated=URL('http://www.ero-lust.com/videos/top-rated/'),
                    Most_viewed=URL('http://www.ero-lust.com/videos/most-popular/')
                    )

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'image-delete'),
                                                ('div', 'class', 'thumbs'),
                                                ('div', 'class', 'image')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pager')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'main')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'function getEmbed()' in text)
        parser.add_rule(video_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'thumbs2')])
        picture_rule.add_process_rule_level('a', {'href'})
        picture_rule.add_process_rule_level('img', {'src'})
        # picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('thumb', 'origin'))
        parser.add_rule(picture_rule)

        picture_tags_rule = ParserRule()
        picture_tags_rule.add_activate_rule_level([('div', 'class', 'main')])
        picture_tags_rule.add_process_rule_level('a', {'href'})
        picture_tags_rule.set_attribute_filter_function('href', lambda txt: '/categories/' in txt or '/model/' in txt)
        parser.add_rule(picture_tags_rule)

        for s in open(fname, encoding='utf-8'):
            parser.feed(s)

        result = ParseResult()

        if len(video_rule.get_result()) > 0:
            result.set_video(MediaData(URL(self.get_attr_from_script(video_rule.get_result()[0]['data']))))
            result.set_type('video')

            for item in picture_tags_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')

            result.set_picture_collector(ELSitePictureCollector())

            i = 1
            for f in picture_rule.get_result():
                result.add_full(FullPictureInfo(abs_href=URL(f['href']), rel_name='%03d.jpg' % i))
                i += 1

            for item in picture_tags_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result

    def get_attr_from_script(self, txt=''):
        t = txt.partition('var flashvars = {')[2].partition('}')[0]
        t1 = t.split(',')
        for i in t1:
            if i.strip().startswith('video_url:'):
                return i.partition(':')[2].strip(" '")
        return ''


class ELSitePictureCollector(PictureCollector):
    def parse_index(self, request, url):
        parser = SiteParser()

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('center', '', '')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        parser.add_rule(picture_rule)

        for data in request:
            parser.feed(data.decode('utf-8'))

        # print(picture_rule.get_result()[0]['src'])

        return picture_rule.get_result()[0]['src']
