__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

class GBvideoSite(BaseSite):
    def start_button_name(self):
        return "GBvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Recent=URL('http://gobdsm.com/latest-updates/?from=0*'),
                    Top_Rated_All_Time=URL('http://gobdsm.com/top-rated/'),
                    Top_Rated_Today=URL('http://gobdsm.com/top-rated/today/'),
                    Top_Rated_Week=URL('http://gobdsm.com/top-rated/week/'),
                    Top_Rated_Month=URL('http://gobdsm.com/top-rated/month/'),
                    Popular_All_Time=URL('http://gobdsm.com/most-popular/'),
                    Popular_Today=URL('http://gobdsm.com/most-popular/today/'),
                    Popular_Week=URL('http://gobdsm.com/most-popular/week/'),
                    Popular_Month=URL('http://gobdsm.com/most-popular/month/'))

    def startpage(self):
        return URL("http://gobdsm.com/latest-updates/?from=0*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('gobdsm.com/')

    def get_href(self, txt='', base_url=URL()):
        txt=txt.strip()
        if not txt.endswith('/'):
            txt=txt+"*"
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt
        # print(base_url.get() + txt)
        return base_url.get().rpartition('/')[0]+'/' + txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        # def star_get_url(txt=''):
        #     return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'image ')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) )
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'sub_menu dark-menu'),
                                                      ('div', 'class', 'sub-menu dark-menu')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href','title'})
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
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'block_content')])
        # gallery_href_rule.add_activate_rule_level([('td', 'colspan', '2')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_filter_function('href',lambda x:'/tags/' in x or '/categories/' in x)
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'block_content')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_filter_function('href',lambda x:'/members/' in x )
        # gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        # gallery_user_rule.set_attribute_filter_function('href',lambda x:'/categories/' in x)
        parser.add_rule(gallery_user_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result(): #len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '')#.replace('\\','')
            # print(script)
            file = script.partition("video_url:'")[2].partition("',")[0]
            # print(file)
            video = MediaData(URL(file))

            result.set_type('video')
            result.set_video(video)

            #
            # for f in gallery_channel_rule.get_result(['data', 'href']):
            #     result.add_control(ControlInfo(f['data'], URL(f['href'])))
            if gallery_user_rule.is_result():
                # print(gallery_user_rule.get_result()[0])
                username=gallery_user_rule.get_result()[0].get('data','***')
                user=gallery_user_rule.get_result()[0]['href'].rstrip('/').rpartition('/')[2]

                # print(user)
                result.add_control(ControlInfo('"'+username+'"', URL('http://gobdsm.com/members/'+user+'/public_videos/')))
                # result.add_control(ControlInfo(user+' gals', URL('http://motherless.com/galleries/member/'+user+'*')))


            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if startpage_rule.is_result(): #len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('title',item.get('data','')), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




