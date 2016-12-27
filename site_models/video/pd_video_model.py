__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class PDvideoSite(BaseSite):
    def start_button_name(self):
        return "PDvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Recent=URL('http://www.porndreamer.com/latest-updates/'),
                    Top_Rated_Today=URL('http://www.porndreamer.com/top-rated/today/'),
                    Top_Rated_Last_Week=URL('http://www.porndreamer.com/top-rated/week/'),
                    Top_Rated_Month=URL('http://www.porndreamer.com/top-rated/month/'),
                    Top_Rated_All_Time=URL('http://www.porndreamer.com/top-rated/'),
                    Popular_Today=URL('http://www.porndreamer.com/most-popular/today/'),
                    Popular_Last_Week=URL('http://www.porndreamer.com/most-popular/week/'),
                    Popular_Month=URL('http://www.porndreamer.com/most-popular/month/'),
                    Popular_All_Time=URL('http://www.porndreamer.com/most-popular/'),
                    Longest=URL('http://www.porndreamer.com/longest/')
                    )

    def startpage(self):
        return URL("http://www.porndreamer.com/latest-updates/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('porndreamer.com/')

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'inner_wrap')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt', 'data-original'})
        # startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'holder_list')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href', 'title'})
        # startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*')
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'player')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'video_url:' in text or 'jwplayer(' in text)
        parser.add_rule(video_rule)
        #
        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'tools_watch')])
        gallery_user_rule.add_process_rule_level('a', {'href', 'title'})
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: x + 'public_videos/')
        gallery_user_rule.set_attribute_filter_function('href', lambda x: '/members/' in x)
        parser.add_rule(gallery_user_rule)

        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'tools_watch')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        # gallery_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        gallery_href_rule.set_attribute_filter_function('href', lambda x: '/categories/' in x or '/tags/' in x)
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():  # len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '')  # .replace('\\','')
            # print(script)
            file = 'Not found!!!!'
            if 'jwplayer(' in script:
                file = script.partition('file:"')[2].partition('",')[0]  # +'*'
            elif "video_url:'" in script:
                file = script.partition("video_url:'")[2].partition("',")[0]  # +'*'
            # print(file)
            video = MediaData(URL(file))

            result.set_type('video')
            result.set_video(video)

            #
            # for f in gallery_channel_rule.get_result(['data', 'href']):
            #     result.add_control(ControlInfo(f['data'], URL(f['href'])))

            f = gallery_user_rule.get_result(['href'])[0]
            # print(f)
            result.add_control(ControlInfo('"' + f['data'] + '"', URL(f['href'])))

            for f in gallery_href_rule.get_result(['href']):
                # print(f)
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if startpage_rule.is_result():  # len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                result.add_thumb(ThumbInfo(thumb_url=URL(item['data-original']), href=URL(item['href']),
                                           description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('title', item.get('data', '')), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
