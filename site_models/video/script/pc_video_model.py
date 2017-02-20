__author__ = 'Vit'

from base_classes import UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class PCvideoSite(BaseSite):
    def start_button_name(self):
        return "PCvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Channels=URL('http://www.porn.com/channels*'),
                    Stars=URL('http://www.porn.com/pornstars?o=n*'))

    def startpage(self):
        return URL("http://www.porn.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('.porn.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        def star_get_url(txt=''):
            return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule(debug=False)
        startpage_rule.add_activate_rule_level([('div', 'class', 'main l170'),
                                                ('div', 'class', 'main l200'),
                                                ('div', 'class', 'main'),
                                                ('div', 'class', 'profileRight'),
                                                ('div', 'class', 'main l200 r300')])
        startpage_rule.add_activate_rule_level([('ul', 'class', 'listThumbs'),
                                                ('ul', 'class', 'listProfiles'),
                                                ('ul', 'class', 'listChannels'),
                                                ('ul', 'class', 'listGalleries')])
        startpage_rule.add_process_rule_level('a', {'href', 'class', 'style'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        startpage_rule.set_attribute_modifier_function('style', star_get_url)
        startpage_rule.set_attribute_filter_function('href', lambda x: not '/pictures/' in x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pager')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'sFilters initial'),
                                                      ('ul', 'class', 'sFilters'),
                                                      ('div', 'class', 'listSearches searchOption'),
                                                      ('div', 'class', 'alpha')
                                                      ])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_hrefs_rule.set_attribute_filter_function('title', lambda x: 'Combine Category' not in x)
        parser.add_rule(startpage_hrefs_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('head', '', '')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'streams:[' in text)
        parser.add_rule(video_rule)

        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('p', 'class', 'source tags'),
                                                   ('p', 'class', 'source categories')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('p', 'class', 'source')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_filter_function('href', lambda x: '/profile/' in x)
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x + '/videos', base_url))
        parser.add_rule(gallery_user_rule)

        gallery_actor_rule = ParserRule()
        gallery_actor_rule.add_activate_rule_level([('p', 'class', 'source')])
        gallery_actor_rule.add_process_rule_level('a', {'href'})
        gallery_actor_rule.set_attribute_filter_function('href', lambda x: '/pornstars/' in x)
        gallery_actor_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x + '/videos', base_url))
        parser.add_rule(gallery_actor_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():

            urls = UrlList()
            for item in video_rule.get_result():
                script = item['data'].replace(' ', '')
                sources = self.quotes(script, 'streams:[{', '}]').split('},{')
                for f in sources:
                    label = self.quotes(f, 'id:"', '"')
                    file = self.quotes(f, 'url:"', '"')
                    urls.add(label, URL(file + '*'))

            result.set_video(urls.get_media_data(-1))

            for f in gallery_user_rule.get_result(['href']):
                result.add_control(ControlInfo('"' + f['data'] + '"', URL(f['href'])))

            for f in gallery_actor_rule.get_result(['href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if startpage_rule.is_result():
            #
            # for item in startpage_rule.get_result():
            #     print(item)

            for item in startpage_rule.get_result(['href', 'src']):
                caption = ''
                href = item['href']
                if '/channels/' in href or '/pornstars/' in href:
                    result.set_caption_visible(True)
                    caption = item.get('alt', href.rpartition('/')[2].strip('*').replace('-', ' ').title())
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=caption))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href']):
                result.add_control(ControlInfo(item.get('title', item.get('data', '')), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
