__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class PHDvideoSite(BaseSite):
    def start_button_name(self):
        return "PHDvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Featured_Videos=URL('http://www.pornhd.com/'),
                    Newest_Video=URL('http://www.pornhd.com/videos/newest*'),
                    Most_Viewed=URL('http://www.pornhd.com/videos/mostpopular*'),
                    Longest_Video=URL('http://www.pornhd.com/videos/longest*'),
                    Top_Rated_Video=URL('http://www.pornhd.com/videos/toprated*')
                    )

    def startpage(self):
        return URL("http://www.pornhd.com/videos/newest*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('pornhd.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('ul', 'class', 'thumbs')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt','data-original'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pager paging')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'player-container')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'players.push' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('ul', 'class', 'video-tag-list')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result(): #len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '').replace('\\', '')
            sources = script.partition("'sources':{")[2].partition('}')[0].split(',')

            urls=list()
            for item in sources:
                part=item.strip("\n\t'").partition("':'")
                if part[2].startswith('http://'):
                    data=dict(text=part[0], url=URL(part[2].strip("'") + '*'))
                    urls.append(data)

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

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))
            return result

        if startpage_rule.is_result(): #len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                t_url=item.get('data-original',item['src'])
                result.add_thumb(ThumbInfo(thumb_url=URL(t_url), href=URL(item['href']),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        return result




if __name__ == "__main__":
    pass




