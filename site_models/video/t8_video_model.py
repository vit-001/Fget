__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class T8videoSite(BaseSite):
    def start_button_name(self):
        return "T8vid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Newest=URL('http://www.tube8.com/newest.html*'),
                    Newest_long=URL('http://www.tube8.com/newest.html?filter_duration=long*'),
                    Newest_medium=URL('http://www.tube8.com/newest.html?filter_duration=medium*'),
                    Newest_short=URL('http://www.tube8.com/newest.html?filter_duration=short*'),
                    Featured=URL('http://www.tube8.com/latest.html*'),
                    Featured_long=URL('http://www.tube8.com/latest.html?filter_duration=long*'),
                    Featured_medium=URL('http://www.tube8.com/latest.html?filter_duration=medium*'),
                    Featured_short=URL('http://www.tube8.com/latest.html?filter_duration=short*'))

    def startpage(self):
        return URL("http://www.tube8.com/newest.html*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('tube8.com/')

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        # def star_get_url(txt=''):
        #     return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule(debug=False)
        startpage_rule.add_activate_rule_level([('div', 'class', 'video_box'),
                                                ('div', 'class', 'box-thumbnail')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        # startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # startpage_rule.set_attribute_modifier_function('style', star_get_url)
        # startpage_rule.set_attribute_filter_function('href',lambda x: not '/pictures/'in x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'id', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        # startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'id', 'videos_categories')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        # startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(startpage_hrefs_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'id', 'playerContainer')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'flashvars' in text)
        parser.add_rule(video_rule)

        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('li', 'class', 'tag-list'),
                                                   ('li', 'class', 'video-category')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        # gallery_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('span', 'id', 'videoUsername')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: x.replace('/user/', '/user-videos/'))
        parser.add_rule(gallery_user_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '').replace('\\', '')
            flashvars = script.partition('flashvars={')[2].partition('};')[0]
            # print(flashvars)

            # def parce(txt):
            #     label = txt.partition('id:"')[2].partition('"')[0]
            #     file = txt.partition('url:"')[2].partition('"')[0]
            #     print(label,file)
            #     return dict(text=label, url=URL(file + '*'))

            urls = list()

            while '"quality_' in flashvars:
                nxt = flashvars.partition('"quality_')[2]

                t = nxt.partition('":"')
                label = t[0]
                file = t[2].partition('",')[0]
                # print (label, file)
                if file.startswith('http://'):
                    urls.append(dict(text=label, url=URL(file + '*')))
                flashvars = nxt

            # print(urls)

            if len(urls) == 1:
                video = MediaData(urls[0]['url'])
            elif len(urls) > 1:
                video = MediaData(urls[len(urls) - 1]['url'])
                for item in urls:
                    video.add_alternate(item)
            else:
                return result

            result.set_type('video')
            result.set_video(video)

            for f in gallery_user_rule.get_result(['data', 'href']):
                username = '"' + f['href'].split('/')[-2] + '"'
                result.add_control(ControlInfo(username, URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
