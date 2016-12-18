__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo, UrlList

class CBPvideoSite(BaseSite):
    def start_button_name(self):
        return "CBPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(HD=URL('http://collectionofbestporn.com/tag/hd-porn*'),
                    Latest=URL('http://collectionofbestporn.com/most-recent*'),
                    TopRated=URL('http://collectionofbestporn.com/top-rated*'),
                    MostViewed=URL('http://collectionofbestporn.com/most-viewed*'),
                    Categories=URL('http://collectionofbestporn.com/channels/'),
                    Longest=URL('http://collectionofbestporn.com/longest*'))

    def startpage(self):
        return URL("http://collectionofbestporn.com/most-recent*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('collectionofbestporn.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'video-thumb')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) )
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)


        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('video', '', '')])
        video_rule.add_process_rule_level('source', {'src','label','res'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        parser.add_rule(video_rule)

        gallery_href_rule = ParserRule()
        # gallery_href_rule.add_activate_rule_level([('div', 'class', 'option')])
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'tags-container')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        # gallery_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        parser.add_rule(gallery_href_rule)


        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result():

            urls=UrlList()
            for item in video_rule.get_result(['src','res']):
                urls.add(item['res'],URL(item['src']))

            result.set_video(urls.get_media_data(-1))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href']+'*')))
            return result

        if startpage_rule.is_result():
            # for item in startpage_rule.get_result():
            #     print(item)

            for item in startpage_rule.get_result(['href','src']):
                href=item['href']
                if '/category/' in href:
                    result.set_caption_visible(True)
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(href),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




