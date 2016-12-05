__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

class PXvideoSite(BaseSite):
    def start_button_name(self):
        return "PXvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Best_Recent=URL('http://www.pornoxo.com/'),
                    Most_popular=URL('http://www.pornoxo.com/most-viewed/page1.html?s*'),
                    Latest=URL('http://www.pornoxo.com/newest/page1.html?s*'),
                    Top_Rated=URL('http://www.pornoxo.com/top-rated/page1.html?s*'),
                    Longest=URL('http://www.pornoxo.com/longest/page1.html?s*'))

    def startpage(self):
        return URL("http://www.pornoxo.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('pornoxo.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumb vidItem')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        # startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'left-menu-box')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_filter_function('href',lambda x: '/videos/' in x)
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'block videoDetail vidItem')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'content-tags')])
        # gallery_href_rule.add_activate_rule_level([('div', 'class', 'column second')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'user-card')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.add_process_rule_level('span', {'class'})
        # gallery_user_rule.set_attribute_filter_function('href',lambda x:'/profile/' in x)
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_user_rule)

        gallery_user_name_rule = ParserRule()
        gallery_user_name_rule.add_activate_rule_level([('div', 'class', 'user-data')])
        gallery_user_name_rule.add_process_rule_level('span', {'class'})
        # gallery_user_rule.set_attribute_filter_function('href',lambda x:'/profile/' in x)
        # gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x+'/videos',base_url))
        parser.add_rule(gallery_user_name_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace('\t','').replace('\n','')

            # print(video_rule.get_result()[0]['data'])
            # print('len=',len(video_rule.get_result()))

            file=''
            if 'sources:' in script:
                sources=script.partition('sources:')[2].partition(']')[0]
                # print(sources)
                file = sources.partition('file: "')[2].partition('",')[0].strip('"').replace(' ','%20')
            # print(file)
            elif  "filefallback':" in script:
                file=script.replace(' ','').partition("filefallback':\"")[2].partition('",')[0]
                # print(file)
            else:
                return result

            video = MediaData(URL(file))

            result.set_type('video')
            result.set_video(video)

            user_url=gallery_user_rule.get_result(['href'])[0]['href']
            user_name=gallery_user_name_rule.get_result(['data'])[0]['data']
            # print(user_url,user_name)
            result.add_control(ControlInfo('"'+user_name+'"', URL(user_url)))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href','src']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src'].replace(' ','%20')), href=URL(item['href']),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href', 'data'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




