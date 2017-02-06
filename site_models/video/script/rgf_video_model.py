__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class RGFvideoSite(BaseSite):
    def start_button_name(self):
        return "RGFvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Newest_Short=URL('http://www.submityourflicks.com//?duration=short*'),
                    Videos_Newest_Medium=URL('http://www.submityourflicks.com//?duration=medium*'),
                    Videos_Newest_Long=URL('http://www.submityourflicks.com//?duration=long*'),
                    Videos_Most_Viewed=URL('http://www.submityourflicks.com/most-viewed/'),
                    Videos_Top_Rated=URL('http://www.submityourflicks.com/top-rated/')
                    )

    def startpage(self):
        return URL("http://www.realgfporn.com/most-recent/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('realgfporn.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        # startpage_rule.add_activate_rule_level([('section', '', '')])
        startpage_rule.add_activate_rule_level([('div', 'class', 'post')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination pagination-centered pagination-inverse')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'id', 'mediaspace')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer(' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('ul', 'class', 'stats-list stats-list--plain')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():

            urls = UrlList()
            for item in video_rule.get_result():
                # print(item['data'])
                file = self.quotes(item['data'].replace(' ', ''), 'file:"', '"')
                urls.add('DEFAULT', URL(file))

            result.set_video(urls.get_media_data())

            for f in gallery_href_rule.get_result(['data', 'href']):
                if '/user/' in f['href']:
                    form='"{0}"'
                else:
                    form = '{0}'

                result.add_control(ControlInfo(form.format(f['data']), URL(f['href'])))

            return result

        if startpage_rule.is_result():

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt''')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        return result



if __name__ == "__main__":
    pass
