__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo


class TDvideoSite(BaseSite):
    def start_button_name(self):
        return "TDvideo"

    def startpage(self):
        return URL("http://tubedupe.com/")

    def get_start_button_menu_text_url_dict(self):
        return dict(Models=URL('http://tubedupe.com/models/'),
                    Updates=URL('http://tubedupe.com/latest-updates/'),
                    Categories=URL('http://tubedupe.com/categories/'))

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('tubedupe.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumb_300'),
                                                ('div', 'class', 'thumb'),
                                                ('div', 'class', 'th'),
                                                ('div', 'class', 'th_model')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src'})
        # startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
        startpage_pages_rule.add_process_rule_level('a', {'title', 'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('li', 'id', 'categories')])
        startpage_hrefs_rule.add_process_rule_level('a', { 'href'})
        # startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_hrefs_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'player_body')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data',lambda text:'function playStart()' in text)
        parser.add_rule(video_rule)

        picture_href_rule = ParserRule()
        picture_href_rule.add_activate_rule_level([('p', 'class', 'info_category'),
                                                   ('p', 'class', 'info_tags'),
                                                   ('p', 'class', 'info_cast')])
        picture_href_rule.add_process_rule_level('a', {'href'})

        parser.add_rule(picture_href_rule)

        for s in open(fname):
            # print(s)
            parser.feed(s)

        result = ParseResult(self)

        if len(video_rule.get_result())>0:
            result.set_video(MediaData(URL(self.get_attr_from_script(video_rule.get_result()[0]['data']))))
            result.set_type('video')

            for f in picture_href_rule.get_result():
                # print(f)
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href'])))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                if '?from=' in item['href']:
                    result.add_page(ControlInfo(item['data'], URL(item['href']+'*')))
                else:
                    result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result

    def get_attr_from_script(self,txt=''):
        t=txt.partition('var flashvars = {')[2].partition('}')[0]
        t1=t.split(',')
        for i in t1:
            if i.strip().startswith('video_url:'):
                return i.partition(':')[2].strip(" '")
        return ''


if __name__ == "__main__":
    t=TDvideoSite()
    t.parse_index_file('E:/Dropbox/Hobby/PRG/PyWork/FGet/files/index1.html')




