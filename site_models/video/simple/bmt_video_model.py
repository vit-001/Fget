__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class BMTvideoSite(BaseSite):
    def start_button_name(self):
        return "BMTvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Most_Recsent=URL('http://beemtube.com/most-recent/'),
                    Videos_Most_Viewed=URL('http://beemtube.com/most-viewed/'),
                    Videos_Medium_5to20m=URL('http://beemtube.com/duration/medium/'),
                    Videos_Top_Rated=URL('http://beemtube.com/top-rated/'),
                    Videos_Long_20plus=URL('http://beemtube.com/duration/long/'),
                    Videos_Short=URL('http://beemtube.com/duration/short/'),
                    Channels=URL('http://beemtube.com/channels/'),
                    Categories=URL('http://beemtube.com/categories/')
                    )

    def startpage(self):
        return URL("http://beemtube.com/most-recent/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('beemtube.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'contents videos')])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'id', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'contents')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        # video_rule.set_attribute_modifier_function('src',lambda x:self.get_href(x,base_url))
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'info_holder')])
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'l')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_filter_function('href', lambda x: '/profiles/' not in x)
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'info_holder')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_filter_function('href', lambda x: '/profiles/' in x)
        gallery_user_rule.set_attribute_modifier_function('href',
                                                          lambda x: self.get_href(x.replace('.html', '/videos/'),
                                                                                  base_url))
        parser.add_rule(gallery_user_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result():

            urls = UrlList()
            for item in video_rule.get_result():
                file = self.quotes(item['data'], 'file:', ',').strip(' "')
                urls.add('default', URL(file + '*'))

            result.set_video(urls.get_media_data())

            for f in gallery_user_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo('"' + f['data'].strip() + '"', URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            return result

        if startpage_rule.is_result():
            for item in startpage_rule.get_result(['href']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),
                                           description=item.get('alt', item.get('title', ''))))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
