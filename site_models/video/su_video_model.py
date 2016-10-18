__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class SUvideoSite(BaseSite):
    def start_button_name(self):
        return "SUvideo"

    def get_start_button_menu_text_url_dict(self):
        return dict(Hall_of_fame=URL('http://sexu.com/top/all/'),
                    Sorted_by_date=URL('http://sexu.com/top/recent/'),
                    Popular_today=URL('http://sexu.com/top/today/'))

    def startpage(self):
        return URL("http://sexu.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('sexu.com/')

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        def star_get_url(txt=''):
            return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumb')])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'src','data-original'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x )
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'listTags listTags5')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('body', '', '')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer("jw_video").setup' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('ul', 'class', 'stickerNav')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(gallery_href_rule)
        #
        # gallery_channel_rule = ParserRule()
        # gallery_channel_rule.add_activate_rule_level([('p', 'class', 'source')])
        # gallery_channel_rule.add_process_rule_level('a', {'href'})
        # gallery_channel_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # parser.add_rule(gallery_channel_rule)

        for s in open(fname, encoding='utf-8'):
            parser.feed(s)  #.replace('</b>','</a>'))

        result = ParseResult(self)

        if len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data']#.replace(' ', '').replace('\\','')

            # print(script)
            # print('len=',len(video_rule.get_result()))
            sources = script.partition('"sources":[{')[2].partition('}]')[0].split('},{')
            # for i in sources:
            #     print(i)

            def parce(txt):
                label = txt.partition('"label":"')[2].partition('"')[0]
                file = txt.partition('"file":"')[2].partition('"')[0]
                # print(label,file)
                return dict(text=label, url=URL(file + '*'))

            if len(sources) == 1:
                video = MediaData(parce(sources[0])['url'])
            elif len(sources) > 1:
                video = MediaData(parce(sources[len(sources) - 1])['url'])
                for item in sources:
                    video.add_alternate(parce(item))
            else:
                return result

            result.set_type('video')
            result.set_video(video)
            #
            # for f in gallery_channel_rule.get_result(['data', 'href']):
            #     result.add_control(ControlInfo(f['data'], URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href','data-original']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['data-original']), href=URL(item['href']),description=item.get('title','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href', 'data'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




