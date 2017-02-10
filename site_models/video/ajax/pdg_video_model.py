__author__ = 'Vit'

import json

from setting import Setting
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class PDGvideoSite(BaseSite):
    def start_button_name(self):
        return "PDGvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Professional=URL('https://www.porndig.com/video/'),
                    Videos_Amateur=URL('https://www.porndig.com/amateur/videos/')
                    )

    def startpage(self):
        return URL("https://www.porndig.com/video/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('porndig.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'video_item_wrapper video_item_medium')])
        startpage_rule.add_process_rule_level('a', {'href', 'class', 'title'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        # startpage_rule.set_attribute_filter_function('class',lambda x: x == 'thumbnail')
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'video_wrapper')])
        video_rule.add_process_rule_level('iframe', {'src'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'angular.' in text)
        video_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(video_rule)
        #
        video_href_rule = ParserRule()
        video_href_rule.add_activate_rule_level([('div', 'class', 'single_description_item_info')])
        video_href_rule.add_process_rule_level('a', {'href'})
        video_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(video_href_rule)

        try:
            if base_url.method == 'POST':
                has_more = False
                first_page = False

                with open(fname, encoding='utf-8', errors='ignore') as fd:
                    j = json.load(fd)
                success = j.get('success', False)
                if success:
                    next_data = j['data']
                    content = next_data['content']
                    if len(content) > 0:
                        has_more = next_data['has_more']
                        print('has_more:', has_more)
                        with open(fname, 'w', encoding='utf-8') as fd:
                            fd.write(content)

            else:
                first_page = True
                has_more = True

            self.proceed_parcing(parser, fname)

        except ValueError:
            return ParseResult()

        result = ParseResult()

        if video_rule.is_result():  # len(video_rule.get_result()) > 0:

            # print(video_rule.get_result())

            frame = URL(video_rule.get_result()[0]['src'])
            print(frame)

            from requests_loader import load, LoaderError, get_last_index_cookie

            frame_file = Setting.base_dir + 'frame.html'
            cookie = get_last_index_cookie()
            # print(cookie)

            # urls = list()
            # result.set_type('video')

            try:
                r = load(frame, frame_file, cookie=cookie)
                print(r.text)

                urls = list()

                # print(r.text)

                setup = r.text.replace(' ', '').replace('\\/', '/').partition('vc.player_setup=')[2].partition(';')[0]
                playlist = setup.partition('"playlist":')[2]

                split = playlist.split('"file":"')

                for item in split:
                    if '"label":' in item:
                        part = item.partition('"')
                        url = part[0]
                        label = part[2].partition('"label":"')[2].partition('"')[0]
                        print(label, url)
                        next_data = dict(text=label, url=URL(url + '*'))
                        urls.append(next_data)

                if len(urls) == 1:
                    video = MediaData(urls[0]['url'])
                elif len(urls) > 1:
                    video = MediaData(urls[0]['url'])
                    for item in urls:
                        video.add_alternate(item)
                else:
                    return result

                result.set_video(video)

            except LoaderError as err:
                print(err)

            def add_categories(parcer_result, text):
                for f in parcer_result:
                    if text in f['href']:
                        result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))

            parcer_result = video_href_rule.get_result(['data', 'href'])

            add_categories(parcer_result, '/studios/')
            add_categories(parcer_result, '/pornstars/')
            add_categories(parcer_result, '/channels/')

            return result

        if startpage_rule.is_result():

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            prev_data = None
            if first_page:
                print(base_url.get())

                xhr_data = {'base_url': base_url, 'step': 100}
                next_data = {'main_category_id': '1', 'type': 'post', 'filters[filter_type]': 'date',
                             'filters[filter_period]': ''}

                if base_url.contain('/video/'):
                    next_data['name'] = 'all_videos'
                if base_url.contain('/amateur/videos/'):
                    next_data['main_category_id'] = '4'
                    next_data['name'] = 'all_videos'
                if base_url.contain('-amateur'):
                    next_data['main_category_id'] = '4'
                if base_url.contain('/channels/'):
                    next_data['name'] = 'category_videos'
                    next_data['category_id[]'] = self.quotes(base_url.get(), '/channels/', '/')
                if base_url.contain('/pornstars/'):
                    next_data['name'] = 'pornstar_related_videos'
                    next_data['content_id'] = self.quotes(base_url.get(), '/pornstars/', '/')
                    xhr_data['step'] = 65
                if base_url.contain('/studios/'):
                    next_data['name'] = 'studio_related_videos'
                    next_data['content_id'] = self.quotes(base_url.get(), '/studios/', '/')
                    xhr_data['step'] = 65

                next_data['offset'] = str(xhr_data['step'])

            else:
                next_data = base_url.post_data.copy()
                xhr_data = base_url.xhr_data.copy()
                curr = int(base_url.post_data['offset'])
                next_data['offset'] = str(curr + xhr_data['step'])
                if curr > 100:
                    prev_data = base_url.post_data.copy()
                    prev_data['offset'] = str(curr - xhr_data['step'])

            xhr_href = 'https://www.porndig.com/posts/load_more_posts/'

            result.add_page(ControlInfo('Main', xhr_data['base_url']))

            sorted_data = next_data.copy()
            sorted_data['offset'] = '0'

            for method in ['date', 'views', 'rating', 'duration', 'ctr']:
                data = sorted_data.copy()
                data['filters[filter_type]'] = method
                sorted_url = URL(xhr_href, method='POST', post_data=data, xhr_data=xhr_data)
                result.add_page(ControlInfo('Sorted by {0}(0)'.format(method), sorted_url))

                if prev_data is not None:
                    data = prev_data.copy()
                    data['filters[filter_type]'] = method
                    prev_url = URL(xhr_href, method='POST', post_data=data, xhr_data=xhr_data)
                    result.add_page(ControlInfo('Prev {0}({1})'.format(method, data['offset']), prev_url))
                if has_more:
                    data = next_data.copy()
                    data['filters[filter_type]'] = method
                    next_url = URL(xhr_href, method='POST', post_data=data, xhr_data=xhr_data)
                    result.add_page(ControlInfo('Next {0}({1})'.format(method, data['offset']), next_url))

        return result


if __name__ == "__main__":
    pass
