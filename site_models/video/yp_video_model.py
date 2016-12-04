__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

class YPvideoSite(BaseSite):
    def start_button_name(self):
        return "YPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Released_Sort_Order=URL('http://www.nudeflix.com/browse/scene?order=released*'),
                    Length_Sort_Order=URL('http://www.nudeflix.com/browse/scene?order=length*'),
                    Rating_Sort_Order=URL('http://www.nudeflix.com/browse/scene?order=rating*'),
                    High_Definition_Sort_Order=URL('http://www.nudeflix.com/browse/scene?order=hd*'),


                    Newest_Video=URL('http://www.nudeflix.com/featured/new-releases*'),
                    Recently_Added_Video=URL('http://www.nudeflix.com/featured/recently-added*'),
                    Trending_Video=URL('http://www.nudeflix.com/featured/trending/25*'),
                    Hot_List_Video=URL('http://www.nudeflix.com/featured/hot-list*'),
                    #

                    )

    def startpage(self):
        return URL("http://yourporn.sexy/blog/all/0.html*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('yourporn.sexy/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        # startpage_rule.add_activate_rule_level([('div', 'class', 'post_block')])#
        startpage_rule.add_activate_rule_level([('div', 'class', 'vid_container')])
        startpage_rule.add_process_rule_level('img', {'src'})
        startpage_rule.add_process_rule_level('a', {'href'})
        # startpage_rule.set_attribute_filter_function('src',lambda x: '.jpg' in x)
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'dropdown-menu columns')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        # startpage_hrefs_rule.set_attribute_filter_function('href',lambda x: '/channel/' in x or '/prime/' in x)
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_hrefs_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'post_block')])
        # video_rule.add_process_rule_level('a', {'href'})
        video_rule.add_process_rule_level('video', {'src'})
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('ul', 'class', 'info')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_filter_function('href',lambda x: '#' not in x)
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result(): #len(video_rule.get_result()) > 0:

            # print(video_rule.get_result())

            video = MediaData(URL(video_rule.get_result()[0]['src']))

            result.set_type('video')
            result.set_video(video)

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))
            return result

        if startpage_rule.is_result(): #len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                t_url=item['src']
                result.add_thumb(ThumbInfo(thumb_url=URL(t_url), href=URL(item['href']),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result

if __name__ == "__main__":
    pass




