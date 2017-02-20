__author__ = 'Vit'

from base_classes import UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class RTvideoSite(BaseSite):
    def start_button_name(self):
        return "RTvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Recommended=URL('http://www.redtube.com/recommended*'),
                    Newest=URL('http://www.redtube.com/'),
                    Top_Rated=URL('http://www.redtube.com/top*'),
                    Longest=URL('http://www.redtube.com/longest*'),
                    Most_Viewed_By_Week=URL('http://www.redtube.com/mostviewed*'),
                    Most_Favored_By_Week=URL('http://www.redtube.com/mostfavored*'),
                    Most_Viewed_All_Time=URL('http://www.redtube.com/mostviewed?period=alltime*'),
                    Most_Favored_All_Time=URL('http://www.redtube.com/mostfavored?period=alltime*'),
                    Pornstars=URL('http://www.redtube.com/pornstar/alphabetical*'),
                    Channels_Alphabetical=URL('http://www.redtube.com/channel/alphabetical*'),
                    Channels_Top_Rated=URL('http://www.redtube.com/channel/top-rated*'),
                    Channels_Recommended=URL('http://www.redtube.com/channel/recommended*'),
                    Channels_Recently_Updated=URL('http://www.redtube.com/channel/recently-updated*'),
                    Channels_Most_Subscribed=URL('http://www.redtube.com/channel/most-subscribed*'),
                    Channels_Most_Viewed=URL('http://www.redtube.com/channel/most-viewed*')
                    )

    def startpage(self):
        return URL("http://www.redtube.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('redtube.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        # print(base_url.domain())
        def star_get_url(txt=''):
            return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule(debug=False)
        startpage_rule.add_activate_rule_level([('ul', 'class', 'video-listing'),
                                                ('ul', 'class', 'video-listing two-in-row'),
                                                ('ul', 'class', 'video-listing four-in-row'),
                                                ('ul', 'class', 'video-listing two-in-row id-recommended-list'),
                                                ('ul', 'class', 'video-listing four-in-row id-recommended-list')
                                                ])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'data-src', 'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('data-src', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pageNumbersHolder')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'categories-listing'),
                                                      ('ul', 'class', 'categories-popular-listing'),
                                                      ('ul', 'class', 'abc-categories newAbcCategories')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_hrefs_rule)

        pornstars_rule = ParserRule()
        pornstars_rule.add_activate_rule_level([('div', 'id', 'all_pornstars')])
        pornstars_rule.add_process_rule_level('a', {'href'})
        pornstars_rule.add_process_rule_level('img', {'src', 'alt'})
        # pornstars_rule.set_attribute_filter_function('href',lambda x: '/channel/' in x or '/prime/' in x)
        pornstars_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(pornstars_rule)

        pornstars_hrefs_rule = ParserRule()
        pornstars_hrefs_rule.add_activate_rule_level([('ul', 'class', 'abc-categories newAbcCategories')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        pornstars_hrefs_rule.add_process_rule_level('a', {'href'})
        pornstars_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(pornstars_hrefs_rule)

        channels_rule = ParserRule(debug=False)
        channels_rule.add_activate_rule_level([('ul', 'class', 'channels-list three-in-row')])
        channels_rule.add_process_rule_level('a', {'href'})
        channels_rule.add_process_rule_level('img', {'src', 'data-src', 'alt'})
        channels_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        channels_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        channels_rule.set_attribute_modifier_function('data-src', lambda x: self.get_href(x, base_url))
        parser.add_rule(channels_rule)

        channels_hrefs_rule = ParserRule()
        channels_hrefs_rule.add_activate_rule_level([('div', 'class', 'channel-filters-categories')])
        # channels_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        channels_hrefs_rule.add_process_rule_level('a', {'href', 'title'})
        channels_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(channels_hrefs_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'watch')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'redtube_flv_player' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'video-details')])
        # gallery_href_rule.add_activate_rule_level([('td', 'class', 'links')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        gallery_href_rule.set_attribute_filter_function('href', lambda x: x != '*')
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():
            urls = UrlList()
            for item in video_rule.get_result():
                script = item['data'].replace(' ', '').replace('\\', '')
                sources = self.quotes(script, 'sources:{"', '"},').split('","')
                for f in sources:
                    t = f.partition('":"')
                    label = t[0]
                    file = self.get_href(t[2], base_url)
                    urls.add(label, URL(file))

            result.set_video(urls.get_media_data())

            for f in gallery_href_rule.get_result(['data', 'href']):
                href = f['href']
                label = f['data']
                if '/redtube/' in href or '/tag/' in href:
                    result.add_control(ControlInfo(label, URL(href)))
                elif '/pornstar/' in href:
                    ps_name = href.rstrip('*').rpartition('/')[2].replace('+', ' ').title()
                    result.add_control(ControlInfo(ps_name, URL(href)))
                else:
                    # adding user
                    result.add_control(ControlInfo("'" + label + "'", URL(href.replace('*', '/videos*'))))
            return result

        if pornstars_rule.is_result():
            result.set_caption_visible(True)
            for item in pornstars_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in pornstars_hrefs_rule.get_result(['href']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))
            return result

        if channels_rule.is_result():
            result.set_caption_visible(True)
            for item in channels_rule.get_result(['href']):
                thumb_href = item.get('data-src', item.get('src'))
                descr = item.get('alt', '').title()
                result.add_thumb(ThumbInfo(thumb_url=URL(thumb_href), href=URL(item['href']), popup=descr))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in channels_hrefs_rule.get_result(['href']):
                result.add_control(ControlInfo(item['title'], URL(item['href'])))
            return result

        if startpage_rule.is_result():
            for item in startpage_rule.get_result(['href']):
                thumb_href = item.get('data-src', item.get('src'))
                descr = item.get('title', item.get('alt', ''))
                result.add_thumb(ThumbInfo(thumb_url=URL(thumb_href), href=URL(item['href']), popup=descr))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'title']):
                result.add_control(ControlInfo(item['title'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
