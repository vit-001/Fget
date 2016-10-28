__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class VPvideoSite(BaseSite):
    def start_button_name(self):
        return "VPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Top_Rated_Video=URL('http://www.vporn.com/rating'),
                    Latest_Video=URL('http://www.vporn.com/newest'),
                    HD_video=URL('http://www.vporn.com/newest/hd'))

    def startpage(self):
        return URL("http://www.vporn.com/newest/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('vporn.com/')

    def get_href(self,txt='',base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain()+txt

    def parse_index_file(self, fname, base_url=URL()):
        print ('VP parsing')

        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'bx'),
                                                ('div', 'class', 'bx lastrow')])
        startpage_rule.add_process_rule_level('a', {'href','class'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagerwrap')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        # startpage_pages_rule.set_attribute_modifier_function('href',lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'video_panel')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data',lambda text:'var flashvars' in text)
        parser.add_rule(video_rule)


        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'tagas-secondrow')])
        # gallery_href_rule.add_activate_rule_level([('td', 'class', 'btnList')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href',lambda x: base_url.domain() + x+'*')
        # gallery_href_rule.set_attribute_filter_function('href',lambda x:'/category/'in x or '/search/'in x)
        parser.add_rule(gallery_href_rule)

        for s in open(fname, encoding='utf-8',errors='ignore'):
            # print(s)
            parser.feed(s.replace('</b>','</a>'))

        result = ParseResult(self)

        if len(video_rule.get_result())>0:
            script=video_rule.get_result()[0]['data'].replace(' ','')

            def get_url_from_script(script='',var=''):
                data=script.partition('flashvars.'+var+'="')[2].partition('"')[0]
                # print(var,data)
                if data.startswith('http://'):return URL(data)

            videoUrlLow=get_url_from_script(script,'videoUrlLow')
            videoUrlLow2=get_url_from_script(script,'videoUrlLow2')
            videoUrlMedium=get_url_from_script(script,'videoUrlMedium')
            videoUrlMedium2=get_url_from_script(script,'videoUrlMedium2')
            videoUrlHD=get_url_from_script(script,'videoUrlHD')
            videoUrlHD2=get_url_from_script(script,'videoUrlHD2')

            def add_alternate(video,txt,url):
                if url is not None:video.add_alternate(dict(text=txt,url=url))

            # video=MediaData(videoUrlMedium)

            if videoUrlMedium is not None:
                video=MediaData(videoUrlMedium)
            elif videoUrlLow is not None:
                video=MediaData(videoUrlLow)
            else:
                print('No url found')
                return result


            add_alternate(video,'Low', videoUrlLow)
            add_alternate(video,'Low2', videoUrlLow2)
            add_alternate(video,'Medium', videoUrlMedium)
            add_alternate(video,'Medium', videoUrlMedium2)
            add_alternate(video,'HD', videoUrlHD)
            add_alternate(video,'HD', videoUrlHD2)

            result.set_type('video')
            result.set_video(video)

            for f in gallery_href_rule.get_result(['data','href']):
                # print(f)
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            # print('return')
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item['alt']))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            # for item in startpage_hrefs_rule.get_result(['href', 'data']):
            #     result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result

if __name__ == "__main__":
    pass




