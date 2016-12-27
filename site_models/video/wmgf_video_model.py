__author__ = 'Vit'

from base_classes import URL, ControlInfo
from setting import Setting
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class WMGFvideoSite(BaseSite):
    def start_button_name(self):
        return "WMGFvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_New=URL('http://www.watchmygf.me/new/'),
                    Videos_Top_Rated=URL('http://www.watchmygf.me/rated/'),
                    Videos_Longest=URL('http://www.watchmygf.me/longest/'),
                    Categories=URL('http://www.watchmygf.me/categories/'),
                    Photo_New=URL('http://www.watchmygf.me/photos/new/'),
                    Channel_Rating=URL('http://www.watchmygf.me/channels/rated/'),
                    Photo_Top_Rated=URL('http://www.watchmygf.me/photos/rated/'),
                    Channel_Popular=URL('http://www.watchmygf.me/channels/popular/'),
                    Channel_New=URL('http://www.watchmygf.me/channels/new/'),
                    Girls=URL('http://www.watchmygf.me/girls/')
                    )

    def startpage(self):
        return URL("http://www.watchmygf.me/new/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('watchmygf.me/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        # def star_get_url(txt=''):
        #     return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'list_videos'),
                                                ('div', 'class', 'list_albums'),
                                                ('div', 'class', 'list_videos model-girls-list'),
                                                ('div', 'class', 'list_videos list_channel')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'model-alpha')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        # startpage_hrefs_rule.set_attribute_filter_function('href',lambda x: '/videos/' in x)
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'vids')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'video_url' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'video-categories')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule(collect_data=True)
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'video-added-info')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        # gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x+'/videos',base_url))
        gallery_user_rule.set_attribute_filter_function('href', lambda x: '/members/' in x)
        parser.add_rule(gallery_user_rule)

        photo_rule = ParserRule()
        photo_rule.add_activate_rule_level([('div', 'class', 'zoom-gallery')])
        photo_rule.add_process_rule_level('a', {'href'})
        # photo_rule.set_attribute_filter_function('href', lambda text: '/photos/' in text)
        photo_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(photo_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        def add_href_and_user_to_result():
            if gallery_user_rule.is_result(['href']):
                for item in gallery_user_rule.get_result(['href']):
                    # print(item)
                    username = item['data'].strip().partition('Added by ')[2].partition(' ')[0]
                    # print(username)
                    if username != '':
                        result.add_control(
                            ControlInfo('"' + username + ' videos"', URL(item['href'] + 'public_videos/')))
                        result.add_control(ControlInfo('"' + username + ' photos"', URL(item['href'] + 'albums/')))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

        if video_rule.is_result():  # len(video_rule.get_result()) > 0:

            # for item in video_rule.get_result():
            #     print('=============================')
            #     print(item['data'])

            script = video_rule.get_result()[0]['data'].replace(' ', '')
            # print(script)

            url = script.partition("video_url:'")[2].partition("'")[0]
            # print(url)

            video = MediaData(URL(url))
            result.set_type('video')
            result.set_video(video)

            add_href_and_user_to_result()
            return result

        if photo_rule.is_result():
            result.set_type('pictures')
            base_dir = base_url.get_path(base=Setting.base_dir) + base_url.get().rpartition('/')[2] + '/'
            result.set_gallery_path(base_dir)
            # print(base_dir)

            for item in photo_rule.get_result():
                name = item['href'].rpartition('/')[2].strip('*')
                picture = FullPictureInfo(abs_href=URL(item['href']), rel_name=name)
                picture.set_base(base_dir)
                result.add_full(picture)

            add_href_and_user_to_result()

            return result

        if startpage_rule.is_result():  # len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('data', item.get('title', '')), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
