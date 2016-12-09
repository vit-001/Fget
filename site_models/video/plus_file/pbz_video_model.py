__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
import json
from requests_loader import load

class PBZvideoSite(BaseSite):
    def start_button_name(self):
        return "PBZvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Most_Recsent=URL('https://www.veronicca.com/videos?o=mr*'),
                    Videos_Most_Viewed=URL('https://www.veronicca.com/videos?o=mv*'),
                    Videos_Most_Commented=URL('https://www.veronicca.com/videos?o=md*'),
                    Videos_Top_Rated=URL('https://www.veronicca.com/videos?o=tr*'),
                    Videos_Top_Favorited=URL('https://www.veronicca.com/videos?o=tf*'),
                    Videos_Longest=URL('https://www.veronicca.com/videos?o=lg*'),
                    Channels=URL('https://www.veronicca.com/channels*')
                    )

    def startpage(self):
        return URL("http://pornbraze.com/recent/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('pornbraze.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'video')])
        startpage_rule.add_process_rule_level('a', {'href','title'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination pagination-lg')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'nav nav-stacked navigation')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        # startpage_hrefs_rule.set_attribute_filter_function('href',lambda x: '/videos/' in x)
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'id', 'player')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        # video_rule.set_attribute_modifier_function('src',lambda x:self.get_href(x,base_url))
        parser.add_rule(video_rule)

        video2_rule = ParserRule()
        video2_rule.add_activate_rule_level([('div', 'id', 'video')])
        video2_rule.add_process_rule_level('script', {'src'})
        video2_rule.set_attribute_filter_function('src', lambda text: 'pornbraze.com/' in text)
        video2_rule.set_attribute_modifier_function('src',lambda x:self.get_href(x,base_url))
        parser.add_rule(video2_rule)

        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'col-xs-12 col-sm-12 col-md-12')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result(): #len(video_rule.get_result()) > 0:

            urls=list()
            for item in video_rule.get_result():
                # print(item['data'])
                script=item['data'].replace(' ','')
                if 'sources:[{' in script:
                    txt='[{'+self.quotes(item['data'].replace(' ',''),'sources:[{','}]')+'}]'
                    j=json.loads(txt)
                    for j_data in j:
                        # print(j_data)
                        if j_data['file'] is not '':
                            data = dict(text=j_data['label'], url=URL(j_data['file']+'*'))
                            urls.append(data)
                elif 'sources:' in script:
                    if video2_rule.is_result(['src']):
                        # print(video2_rule.get_result())
                        php_url=URL(video2_rule.get_result(['src'])[0]['src'])
                        # print(php_url)
                        res=load(php_url)
                        # print(res.text)
                        bitrates=self.quotes(res.text,"'bitrates':[{","}]").split('},{')
                        # print(bitrates)
                        for line in bitrates:
                            print(line)
                            video_url=self.quotes(line,"'file':'","'")
                            label=self.quotes(line,'label:"','"')
                            data = dict(text=label, url=URL(video_url + '*'))
                            urls.append(data)


            if len(urls) == 1:
                video = MediaData(urls[0]['url'])
            elif len(urls) > 1:
                video = MediaData(urls[0]['url'])
                for item in urls:
                    video.add_alternate(item)
            else:
                return result

            result.set_type('video')
            result.set_video(video)

            for f in gallery_href_rule.get_result(['data', 'href']):
                # print(f)
                href=f['href'].replace('*','/')
                label=f['data']
                if '/users/' in href:
                    href=href+'/videos/public/'
                    label='"'+label+'"'

                result.add_control(ControlInfo(label, URL(href)))

            return result

        if startpage_rule.is_result():
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item.get('alt',item.get('title',''))))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result():
                label=item['href'].strip('*/').rpartition('/')[2]
                result.add_control(ControlInfo(label, URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




