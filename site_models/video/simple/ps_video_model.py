__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo, UrlList
from setting import Setting

class PSvideoSite(BaseSite):
    def start_button_name(self):
        return "PSvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Latest=URL('http://pervertslut.com/latest-updates/'),
                    Top_Rated=URL('http://pervertslut.com/top-rated/'),
                    Most_Viewed=URL('http://pervertslut.com/most-popular/'))

    def startpage(self):
        return URL("http://pervertslut.com/latest-updates/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('pervertslut.com/')

    def parse_index_file(self, fname, base_url=URL()):

        print('This site is very slow, be patient')

        parser = SiteParser()

        def star_get_url(txt=''):
            return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'item  ')])
        startpage_rule.add_process_rule_level('a', {'href','title'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination-holder')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'list')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'player')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'flashvars' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'item')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result():
            urls=UrlList()
            for item in video_rule.get_result():
                file=self.quotes(item['data'].replace(' ', ''),"video_url:'","'")
                urls.add('default',URL(file))

            result.set_video(urls.get_media_data())

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if startpage_rule.is_result():
            for item in startpage_rule.get_result(['href']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href']):
                href=item['href']
                label=href.split('/')[-2]
                # print(label,href)
                result.add_control(ControlInfo(label, URL(href)))

        return result


if __name__ == "__main__":
    pass




