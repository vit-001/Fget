__author__ = 'Vit'

import json

from base_classes import UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class EXTvideoSite(BaseSite):
    def start_button_name(self):
        return "EXTvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Most_Popular=URL('http://www.extremetube.com/videos?o=mv*'),
                    Higest_Rating=URL('http://www.extremetube.com/videos?o=tr*'),
                    Longest=URL('http://www.extremetube.com/videos?o=lg*'),
                    New=URL('http://www.extremetube.com/videos*')
                    )

    def startpage(self):
        return URL("http://www.extremetube.com/videos*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('extremetube.com/')

    def parse_index_file(self, fname, base_url=URL()):
        if base_url.contain('format=json'):
            xhr_page = True
        else:
            xhr_page = False

        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'relative margin-auto video-box-wrapper normal-box')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'alt', 'data-srcmedium'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'video-container')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'flashvars=' in text.replace(' ', ''))
        # video_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(video_rule)
        #
        video_href_rule = ParserRule()
        video_href_rule.add_activate_rule_level([('div', 'class', 'ibInfo js_ibInfo')])
        video_href_rule.add_process_rule_level('a', {'href'})
        video_href_rule.set_attribute_filter_function('href', lambda x: 'javascript' not in x)
        video_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(video_href_rule)

        video_user_rule = ParserRule()
        video_user_rule.add_activate_rule_level([('div', 'class', 'ibLine1')])
        video_user_rule.add_process_rule_level('a', {'href'})
        # video_user_rule.set_attribute_filter_function('href',lambda x: 'javascript' not in x)
        video_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(video_user_rule)

        if not xhr_page:
            self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result():
            urls = UrlList()
            for item in video_rule.get_result():
                flashvars = self.quotes(item['data'].replace(' ', ''), 'flashvars={', '};').replace('\\', '').split(
                    ',"')
                for v in flashvars:
                    if v.startswith('quality_'):
                        label = self.quotes(v, 'quality_', '"')
                        file = self.quotes(v, ':"', '"')
                        urls.add(label, URL(file + '*'))

            result.set_video(urls.get_media_data(-1))

            for f in video_user_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo('"' + f['data'] + '"', URL(f['href'])))

            for f in video_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            return result

        if xhr_page:

            def parce_data(data, buttons_added, base_url, items_name='items'):
                xhr_data = base_url.xhr_data
                items = data[items_name]
                nav = data['navigation']
                last_page = nav['lastPage']
                if last_page is None: last_page = 1
                curr_page = int(base_url.get().rpartition('page=')[2])
                pattern = nav['urlPattern'].replace('[%pageId%]', '{}') + '*'

                for item in items:
                    thumb_url = item['thumb_url']
                    title = item['specialchars_title']
                    url = item['video_link']
                    result.add_thumb(ThumbInfo(thumb_url=URL(thumb_url), href=URL(url + '*'), description=title))

                # print('Page {} of {}'.format(curr_page, last_page), pattern.format(curr_page))
                if not buttons_added:
                    result.add_page(ControlInfo('1', xhr_data['base_url']))

                    p_from = curr_page - 5
                    if p_from < 2: p_from = 2

                    p_to = curr_page + 5
                    if p_to > last_page: p_to = last_page

                    for x in range(p_from, p_to):
                        url = URL(pattern.format(x), xhr_data=xhr_data)
                        if x == curr_page: x = str(x) + '(this)'
                        result.add_page(ControlInfo(str(x), url))

                    last_url = URL(pattern.format(last_page), xhr_data=xhr_data)
                    result.add_page(ControlInfo(str(last_page), last_url))
                    buttons_added = True

                return buttons_added

            with open(fname) as fp:
                try:
                    json_data = json.load(fp)
                    buttons_added = False
                    if base_url.contain('/keyword/'):
                        for i in json_data:
                            buttons_added = parce_data(i, buttons_added, base_url)
                    elif base_url.contain('/users/'):
                        parce_data(json_data['response'], buttons_added, base_url, items_name='videos')
                    else:
                        for i in json_data:
                            buttons_added = parce_data(json_data[i], buttons_added, base_url)
                except ValueError:
                    pass
            return result

        if startpage_rule.is_result():

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['data-srcmedium']), href=URL(item['href']),
                                           description=item.get('alt', '')))

            xhr_data = {'base_url': base_url}

            next_url = URL(base_url.get() + '*', xhr_data=xhr_data)  # +'?format=json&number_pages=1&page=2*'
            next_url.add_query([('format', 'json'), ('number_pages', '1'), ('page', '2')])
            result.add_page(ControlInfo('next', next_url))

        return result


if __name__ == "__main__":
    pass
