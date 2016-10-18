__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class RTvideoSite(BaseSite):
    def start_button_name(self):
        return "RTvideo"

    def get_start_button_menu_text_url_dict(self):
        return dict(Recommended=URL('http://www.redtube.com/recommended*'),
                    Newest=URL('http://www.redtube.com/'),
                    Top_Rated=URL('http://www.redtube.com/top*'),
                    Longest=URL('http://www.redtube.com/longest*'),
                    Most_Viewed_By_Week=URL('http://www.redtube.com/mostviewed*'),
                    Most_Favored_By_Week=URL('http://www.redtube.com/mostfavored*'),
                    Most_Viewed_All_Time=URL('http://www.redtube.com/mostviewed?period=alltime*'),
                    Most_Favored_All_Time=URL('http://www.redtube.com/mostfavored?period=alltime*'))

    def startpage(self):
        return URL("http://www.redtube.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('redtube.com/')

    def get_href(self, txt='', base_url=URL()):
        # print(txt,base_url)
        if txt.startswith('http://'):
            return txt
        if txt.startswith('//'):
            return 'http:' + txt
        if txt.startswith('/'):
            return base_url.domain() + txt
        return ''

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        # print(base_url.domain())
        def star_get_url(txt=''):
            return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule(debug=False)
        startpage_rule.add_activate_rule_level([('ul', 'class', 'video-listing'),
                                                ('ul', 'class', 'video-listing two-in-row'),
                                                ('ul', 'class', 'video-listing four-in-row'),
                                                ('ul', 'class', 'video-listing two-in-row id-recommended-list'),
                                                ('ul', 'class', 'video-listing four-in-row id-recommended-list')])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'data-src'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        startpage_rule.set_attribute_modifier_function('data-src', lambda x: self.get_href(x,base_url) + '*' )
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pageNumbersHolder')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'categories-listing'),
                                                      ('ul', 'class', 'categories-popular-listing')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href','title'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'watch')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'redtube_flv_player' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'video-details')])
        # gallery_href_rule.add_activate_rule_level([('td', 'class', 'links')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        gallery_href_rule.set_attribute_filter_function('href',lambda x: x!='*')
        parser.add_rule(gallery_href_rule)
        #
        # gallery_channel_rule = ParserRule()
        # gallery_channel_rule.add_activate_rule_level([('p', 'class', 'source')])
        # gallery_channel_rule.add_process_rule_level('a', {'href'})
        # gallery_channel_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # parser.add_rule(gallery_channel_rule)

        for s in open(fname, encoding='utf-8'):
            parser.feed(s)  #.replace('</b>','</a>'))

        result = ParseResult(self)

        if len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '').replace('\\','')

            # print(script)
            # print('len=',len(video_rule.get_result()))
            sources = script.partition('sources:{"')[2].partition('"},')[0].split('","')
            # for i in sources:
            #     print(i)

            def parce(txt):
                t=txt.partition('":"')
                label = t[0]
                file = t[2]
                # print(label,file)
                return dict(text=label, url=URL(file + '*'))

            if len(sources) == 1:
                video = MediaData(parce(sources[0])['url'])
            elif len(sources) > 1:
                video = MediaData(parce(sources[0])['url'])
                for item in sources:
                    video.add_alternate(parce(item))
            else:
                return result

            result.set_type('video')
            result.set_video(video)
            #
            # for f in gallery_channel_rule.get_result(['data', 'href']):
            #     result.add_control(ControlInfo(f['data'], URL(f['href'])))

            links=set()
            for f in gallery_href_rule.get_result(['data', 'href']):
                if f['href'] not in links:
                    label=f['data'].replace('\t','')
                    if label=='':
                        label=f['href'].rpartition('/')[2]
                    # print(f)
                    result.add_control(ControlInfo(label, URL(f['href'])))
                    links.add(f['href'])
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print (item)
                result.add_thumb(ThumbInfo(thumb_url=URL(item['data-src']), href=URL(item['href']),description=item.get('title','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                # print(item)
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href', 'title'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'title']):
                    result.add_control(ControlInfo(item['title'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




