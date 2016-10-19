__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class TZvideoSite(BaseSite):
    def start_button_name(self):
        return "TZvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Hottest=URL('https://www.thumbzilla.com/'),
                    Newest=URL('https://www.thumbzilla.com/newest*'),
                    Top=URL('https://www.thumbzilla.com/top*'),
                    Trending=URL('https://www.thumbzilla.com/trending*'),
                    Popular=URL('https://www.thumbzilla.com/popular*'),
                    HD=URL('https://www.thumbzilla.com/hd*'),
                    Homemade=URL('https://www.thumbzilla.com/homemade*'))

    def startpage(self):
        return URL("https://www.thumbzilla.com/newest*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('thumbzilla.com/')

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://') or txt.startswith('https://'):
            return txt
        if txt.startswith('/'):
            return 'https://'+base_url.domain() + txt
        return ''

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        # print(base_url.domain())
        def star_get_url(txt=''):
            return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule(debug=False)
        startpage_rule.add_activate_rule_level([('ul', 'class', 'responsiveListing')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'data-original'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        startpage_rule.set_attribute_modifier_function('data-original',lambda x:x.replace('//','https://'))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('section', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'categoryList')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        # startpage_hrefs_rule.add_process_rule_level('span', {''})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('body', '', '')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'videoVars' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'videoInfoTop')])
        # gallery_href_rule.add_activate_rule_level([('td', 'class', 'links')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*' )
        # gallery_href_rule.set_attribute_filter_function('href',lambda x: x!='*')
        parser.add_rule(gallery_href_rule)
        #
        # gallery_channel_rule = ParserRule()
        # gallery_channel_rule.add_activate_rule_level([('p', 'class', 'source')])
        # gallery_channel_rule.add_process_rule_level('a', {'href'})
        # gallery_channel_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # parser.add_rule(gallery_channel_rule)

        for s in open(fname, encoding='utf-8',errors='ignore'):
            parser.feed(s)  #.replace('</b>','</a>'))

        result = ParseResult(self)

        if len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '')#.replace('\\','')

            # print(script)

            urls=list()

            while '"quality_' in script:
                nxt=script.partition('"quality_')[2]

                t=nxt.partition('":"')
                label=t[0]
                file=t[2].partition('",')[0].replace('%2F','/').replace('%3F','?').replace('%26','&').replace('%3D','=')
                # print (label, file)
                urls.append(dict(text=label, url=URL('https:'+file + '*')))
                script=nxt

            if len(urls) == 1:
                video = MediaData(urls[0]['url'])
            elif len(urls) > 1:
                default=urls[len(urls) - 1]['url']
                for t in urls:
                    if '720p' in t['text']:
                        default=t['url']
                video = MediaData(default)
                for item in urls:
                    video.add_alternate(item)
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
                result.add_thumb(ThumbInfo(thumb_url=URL(item['data-original']), href=URL(item['href']),description=item.get('title','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                # print(item)
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    href=item['href']
                    txt=href.rstrip('*').rpartition('/')[2]
                    # print(item)
                    result.add_control(ControlInfo(txt, URL(href)))

        return result


if __name__ == "__main__":
    pass




