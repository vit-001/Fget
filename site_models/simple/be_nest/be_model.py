__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class BESite(BaseSite):
    def start_button_name(self):
        return "BE"

    def startpage(self):
        return URL("http://www.bravoerotica.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('bravoerotica.com/')

    def get_start_button_menu_text_url_dict(self):
        return dict(Latest_Video=URL('http://www.bravoerotica.com/erotic-tube/latest-updates/'),
                    Updates=URL('http://www.bravoerotica.com/latest_updates.html'),
                    Video=URL('http://www.bravoerotica.com/erotic-tube/'),
                    Models=URL('http://www.bravoerotica.com/erotic-tube/models/'),
                    Movies=URL('http://www.bravoerotica.com/erotic-movies/'),
                    Porn=URL('http://www.bravoerotica.com/porn-erotica/'))

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
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumbs'),
                                                ('div', 'class', 'content_box domain2'),
                                                ('div', 'class', 'video_list'),
                                                ('div', 'class', 'video_list_models'),
                                                ('div', 'class', 'pics_list'),
                                                ('div', 'class', 'movie_thumbs')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', self.get_href)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pages'),
                                                      ('div', 'class', 'pg')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('li', 'class', 'orange dropdown')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_filter_function('href', lambda txt: '/st/' in txt)
        parser.add_rule(startpage_hrefs_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'player')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'video_url:' in text)
        parser.add_rule(video_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'thumb_box')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('t.jpg', '.jpg'))
        parser.add_rule(picture_rule)

        picture_href_rule = ParserRule()
        picture_href_rule.add_activate_rule_level([('div', 'class', 'crumbles'),
                                                   ('div', 'class', 'tags')])
        picture_href_rule.add_process_rule_level('a', {'href', 'title'})
        parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if video_rule.is_result():

            video = MediaData(URL(self.get_attr_from_script(video_rule.get_result()[0]['data'])))
            result.set_video(video)
            result.set_type('video')

            for f in picture_href_rule.get_result():
                # print(f)
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            # print('Startpage rule')
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            for f in picture_rule.get_result():
                result.add_full(FullPictureInfo(rel_name=f['src']))

            for f in picture_href_rule.get_result():
                # print(f)
                result.add_control(ControlInfo(f['title'], URL(f['href'])))

        return result

    def get_attr_from_script(self, txt=''):
        t = txt.partition('var flashvars = {')[2].partition('}')[0]
        t1 = t.split(',')
        for i in t1:
            if i.strip().startswith('video_url:'):
                return i.partition(':')[2].strip(" '")
        return ''


if __name__ == "__main__":
    pass
