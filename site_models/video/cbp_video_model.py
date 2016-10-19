__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class CBPvideoSite(BaseSite):
    def start_button_name(self):
        return "CBPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(HD=URL('http://collectionofbestporn.com/tag/hd-porn*'),
                    Latest=URL('http://collectionofbestporn.com/most-recent*'),
                    Home=URL('http://collectionofbestporn.com*'),
                    TopRated=URL('http://collectionofbestporn.com/top-rated*'),
                    MostViewed=URL('http://collectionofbestporn.com/most-viewed*'),
                    Categories=URL('http://collectionofbestporn.com/channels/'),
                    Longest=URL('http://collectionofbestporn.com/longest*'))

    def startpage(self):
        return URL("http://collectionofbestporn.com/most-recent*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('collectionofbestporn.com/')

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt
        return base_url.get().rpartition('/')[0]+'/'+txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'video-thumb')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        # startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x )
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*')
        parser.add_rule(startpage_pages_rule)

        # startpage_hrefs_rule = ParserRule()
        # startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'listTags listTags5')])
        # # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        # startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        # startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # parser.add_rule(startpage_hrefs_rule)
        #
        # video_rule = ParserRule()
        # video_rule.add_activate_rule_level([('div', 'id', 'player')])
        # video_rule.add_process_rule_level('script', {})
        # video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        # parser.add_rule(video_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('video', '', '')])
        video_rule.add_process_rule_level('source', {'src','label','res'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        parser.add_rule(video_rule)

        #
        gallery_href_rule = ParserRule()
        # gallery_href_rule.add_activate_rule_level([('div', 'class', 'option')])
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'tags-container')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        # gallery_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
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
            sources=list()

            for item in video_rule.get_result(['src','res']):
                sources.append(dict(text=item['res'],url=URL(item['src'])))

            if len(sources) == 1:
                video = MediaData(sources[0]['url'])
            elif len(sources) > 1:
                video = MediaData(sources[len(sources) - 1]['url'])
                for item in sources:
                    video.add_alternate(item)
            else:
                return result

            result.set_type('video')
            result.set_video(video)

            for f in gallery_href_rule.get_result(['data', 'href']):
                #print(f)
                result.add_control(ControlInfo(f['data'], URL(f['href']+'*')))
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href','src']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            # if len(startpage_hrefs_rule.get_result(['href', 'data'])) > 0:
            #     for item in startpage_hrefs_rule.get_result(['href', 'data']):
            #         result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




