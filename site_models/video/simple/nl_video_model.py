__author__ = 'Vit'

from base_classes import UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class NLvideoSite(BaseSite):
    def start_button_name(self):
        return "NLvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(New=URL('http://www.sextube.nl/videos/nieuw*'),
                    Videos_Top_Rated=URL('http://www.sextube.nl/videos/hoog-gewaardeerd*'),
                    Popular=URL('http://www.sextube.nl/videos/populair*'),
                    HD=URL('http://www.sextube.nl/videos/hd*'))

    def startpage(self):
        return URL("http://www.sextube.nl/videos/nieuw*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('sextube.nl/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('article', '', '')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination2')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('section', 'class', 'categories')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href', 'title'})
        # startpage_hrefs_rule.set_attribute_modifier_function('title', lambda x: x.replace('Sex films in de categorie ',''))
        parser.add_rule(startpage_hrefs_rule)
        #

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('video', '', '')])
        video_rule.add_process_rule_level('source', {'src'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        video_rule.set_attribute_modifier_function('src', lambda txt: txt + '*')
        parser.add_rule(video_rule)

        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'tags')])
        gallery_href_rule.add_process_rule_level('a', {'href', 'title'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():
            urls = UrlList()
            for item in video_rule.get_result():
                urls.add('default', URL(item['src']))
            result.set_video(urls.get_media_data())

            for f in gallery_href_rule.get_result(['href']):
                result.add_control(ControlInfo(f['title'], URL(f['href'])))
            return result

        if startpage_rule.is_result():
            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            def href_simple(txt=''):
                txt = txt.lower().replace(' ', '').replace('sexfilmsindecategorie', '')
                txt = txt.replace('insexfilms', '').replace('sexfilms', '').replace('inhd', 'HD')
                return txt

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(href_simple(item.get('title', '')), URL(item['href'] + '*')))

        return result


if __name__ == "__main__":
    pass
