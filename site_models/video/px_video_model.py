__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class PXvideoSite(BaseSite):
    def start_button_name(self):
        return "PXvideo"

    def get_start_button_menu_text_url_dict(self):
        return dict(Best_Recent=URL('http://www.pornoxo.com/'),
                    Most_popular=URL('http://www.pornoxo.com/most-viewed/page1.html?s*'),
                    Latest=URL('http://www.pornoxo.com/newest/page1.html?s*'),
                    Top_Rated=URL('http://www.pornoxo.com/top-rated/page1.html?s*'),
                    Longest=URL('http://www.pornoxo.com/longest/page1.html?s*'))

    def startpage(self):
        return URL("http://www.pornoxo.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('pornoxo.com/')

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://'):
            return txt+'*'
        if txt.startswith('/'):
            return base_url.domain() + txt
        return base_url.get().rpartition('/')[0]+'/'+txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumb vidItem')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        # startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'channels')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'block videoDetail vidItem')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('td', 'class', 'al infoDivs')])
        # gallery_href_rule.add_activate_rule_level([('div', 'class', 'column second')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
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
            script = video_rule.get_result()[0]['data'].replace('\t','').replace('\n','')

            #print(video_rule.get_result()[0]['data'])
            # print('len=',len(video_rule.get_result()))
            sources=script.partition('sources:')[2].partition(']')[0]
            print(sources)
            file = sources.partition('file: "')[2].partition('",')[0].strip('"').replace(' ','%20')
            print(file)
            video = MediaData(URL(file))

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

            for item in startpage_rule.get_result(['href','src']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src'].replace(' ','%20')), href=URL(item['href']),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href', 'data'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




