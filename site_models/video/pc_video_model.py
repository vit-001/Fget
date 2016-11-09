__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class PCvideoSite(BaseSite):
    def start_button_name(self):
        return "PCvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Channels=URL('http://www.porn.com/channels'),
                    Stars=URL('http://www.porn.com/pornstars'))

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
        startpage_rule.set_attribute_filter_function('href',lambda x: not '/pictures/'in x)
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
                                                      ('div', 'class', 'listSearches searchOption')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        startpage_hrefs_rule.set_attribute_filter_function('title',lambda x: 'Combine Category' not in x)
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
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('p', 'class', 'source')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_filter_function('href',lambda x:'/profile/' in x)
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x+'/videos',base_url))
        parser.add_rule(gallery_user_rule)

        for s in open(fname, encoding='utf-8',errors='ignore'):
            parser.feed(s)  #.replace('</b>','</a>'))

        result = ParseResult(self)

        if len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '')
            sources = script.partition('streams:[{')[2].partition('}]')[0].split('},{')
            #print(sources)

            def parce(txt):
                label = txt.partition('id:"')[2].partition('"')[0]
                file = txt.partition('url:"')[2].partition('"')[0]
                print(label,file)
                return dict(text=label, url=URL(file + '*'))

            urls=list()
            for item in sources:
                data=parce(item)
                if data['url']!=URL('*'):
                    urls.append(data)

            #print(urls)

            if len(urls) == 1:
                video = MediaData(urls[0]['url'])
            elif len(urls) > 1:
                video = MediaData(urls[-1]['url'])
                for item in urls:
                    video.add_alternate(item)
            else:
                return result

            result.set_type('video')
            result.set_video(video)

            for f in gallery_user_rule.get_result(['href']):
                # print(f)
                result.add_control(ControlInfo('"'+f['data']+'"', URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            if len(startpage_rule.get_result(['href', 'style'])) > 0:
                if Setting.site_debug: print('HREF with STYLE')
                for item in startpage_rule.get_result(['href', 'style']):
                    if Setting.site_debug: print(item['href'], item['style'])
                    result.add_thumb(ThumbInfo(thumb_url=URL(item['style']), href=URL(item['href'])))
            else:
                if Setting.site_debug: print('HREF with SRC')
                for item in startpage_rule.get_result(['href', 'src']):
                    if Setting.site_debug: print(item['href'], item['src'])
                    result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href'])))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href', 'title'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'title']):
                    result.add_control(ControlInfo(item['title'], URL(item['href'])))
            else:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




