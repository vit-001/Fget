__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class XTUBvideoSite(BaseSite):
    def start_button_name(self):
        return "XTUBvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Newest_Short=URL('http://www.submityourflicks.com//?duration=short*'),
                    Videos_Newest_Medium=URL('http://www.submityourflicks.com//?duration=medium*'),
                    Videos_Newest_Long=URL('http://www.submityourflicks.com//?duration=long*'),
                    Videos_Most_Viewed=URL('http://www.submityourflicks.com/most-viewed/'),
                    Videos_Top_Rated=URL('http://www.submityourflicks.com/top-rated/')
                    )

    def startpage(self):
        return URL("http://www.xtube.com/video*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('xtube.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        # startpage_rule.add_activate_rule_level([('section', '', '')])
        startpage_rule.add_activate_rule_level([('article', 'class', 'teaser singleLink hasButtonRow'),
                                                ('article', 'class', 'activity video hasButtonFooter')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'data-lazysrc','alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('nav', 'class', 'clearfix pagination bottom'),
                                                     ('nav', 'class','range rangeCount-2 clearfix')])
        startpage_pages_rule.add_process_rule_level('a', {'href', 'data-href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_pages_rule.set_attribute_modifier_function('data-href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_categories_rule = ParserRule()
        startpage_categories_rule.add_activate_rule_level([('select', 'id', 'input_selectCategories')])
        startpage_categories_rule.add_process_rule_level('option', {'value'})
        startpage_categories_rule.set_attribute_modifier_function('value', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_categories_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'id', 'playerWrapper')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'sources:' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('dl', 'class', 'group')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('nav', 'class', 'profileNav clearfix buttonRow')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        gallery_user_rule.set_attribute_filter_function('href', lambda x: '#videos' in x)
        parser.add_rule(gallery_user_rule)

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

            # for f in gallery_user_rule.get_result():
            #     print(f)
            #     name='"{0}"'.format(f['href'].rpartition('/')[2].partition('#')[0])
            #     result.add_control(ControlInfo(name, URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            return result

        if startpage_rule.is_result():

            for item in startpage_rule.get_result(['href']):
                # print(item)
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item.get('data-lazysrc',item['src'])), href=URL(item['href']), description=item.get('alt''')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                # print(item)
                href=item.get('data-href',item['href'])
                # print(href)
                result.add_page(ControlInfo(href.rpartition('/')[2].strip('*'), URL(href)))

            for item in startpage_categories_rule.get_result():
                result.add_control(ControlInfo(item['data'], URL(item['value'])))

        return result



if __name__ == "__main__":
    pass
