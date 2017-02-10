__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class SKWvideoSite(BaseSite):
    def start_button_name(self):
        return "SKWvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(HD=URL('http://www.spankwire.com/categories/Straight/HD/Submitted/83*'),
                    Top_Rated_Today=URL('http://www.spankwire.com/home1/Straight/Today/Rating*'),
                    Top_Rated_Week=URL('http://www.spankwire.com/home1/Straight/Week/Rating*'),
                    Top_Rated_Month=URL('http://www.spankwire.com/home1/Straight/Month/Rating*'),
                    Top_Rated_Year=URL('http://www.spankwire.com/home1/Straight/Year/Rating*'),
                    Top_Rated_All_time=URL('http://www.spankwire.com/home1/Straight/All_Time/Rating*'),
                    Most_Viewed_Today=URL('http://www.spankwire.com/home1/Straight/Today/Views*'),
                    Most_Viewed_Week=URL('http://www.spankwire.com/home1/Straight/Week/Views*'),
                    Most_Viewed_Month=URL('http://www.spankwire.com/home1/Straight/Month/Views*'),
                    Most_Viewed_Year=URL('http://www.spankwire.com/home1/Straight/Year/Views*'),
                    Most_Viewed_All_time=URL('http://www.spankwire.com/home1/Straight/All_Time/Views*'))

    def startpage(self):
        return URL("http://www.spankwire.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('spankwire.com/')

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
        startpage_rule.add_activate_rule_level([('div', 'class', 'thmb-wrapper')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt', 'data-src', 'data-original'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'id', 'divPagination')])
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
        video_rule.add_activate_rule_level([('div', 'id', 'videoContainer')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'playerData.cdnPath' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'video-info-tags float-left')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(gallery_href_rule)

        gallery_channel_rule = ParserRule()
        gallery_channel_rule.add_activate_rule_level([('div', 'class', 'video-info-uploaded float-right')])
        gallery_channel_rule.add_process_rule_level('a', {'href'})
        gallery_channel_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        gallery_channel_rule.set_attribute_filter_function('href', lambda x: '/categories/' in x)
        parser.add_rule(gallery_channel_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'video-info-uploaded float-right')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        gallery_user_rule.set_attribute_filter_function('href', lambda x: '/user/' in x)
        parser.add_rule(gallery_user_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():  # len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '')  # .replace('\\','')

            # print(video_rule.get_result()[0]['data'])
            # print(script)
            # print('len=',len(video_rule.get_result()))
            lines = script.split('\n')

            data = list()

            for i in lines:
                if i.strip().startswith('playerData.cdnPath'):
                    if "''" not in i:
                        data.append(i.strip())
                        # print(i.strip())

            def parce(txt):
                label = txt.partition('playerData.cdnPath')[2].partition('=')[0]
                file = txt.partition("'")[2].partition("'")[0].replace('%3A', ':').replace('%2F', '/').replace('%26',
                                                                                                               '&')
                # print(label,file)
                return dict(text=label, url=URL(file + '*'))

            if len(data) == 1:
                video = MediaData(parce(data[0])['url'])
            elif len(data) > 1:
                video = MediaData(parce(data[len(data) - 1])['url'])
                for item in data:
                    video.add_alternate(parce(item))
            else:
                return result

            result.set_type('video')
            result.set_video(video)

            for f in gallery_user_rule.get_result(['data', 'href']):
                # print(f)
                result.add_control(ControlInfo('"' + f['data'] + '"', URL(f['href'])))

            for f in gallery_channel_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if startpage_rule.is_result():  # len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                if 'data-src' in item.keys():
                    src = item['data-src']
                elif 'data-original' in item.keys():
                    src = item['data-original']
                elif 'src' in item.keys():
                    src = item['src']
                else:
                    print('New key found. Need rewrite "startpage_rule"')
                    continue
                # print(src,item.get('src',''),item.get('data-src',''))
                result.add_thumb(ThumbInfo(thumb_url=URL(src), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href', 'data'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
