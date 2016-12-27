__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class HDEPvideoSite(BaseSite):
    def start_button_name(self):
        return "HDEPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Newest=URL('http://www.hd-easyporn.com/?o=n*'),
                    Videos_Most_Viewed=URL('http://www.hd-easyporn.com/?o=v*'),
                    Videos_Top_Rated=URL('http://www.hd-easyporn.com/?o=r*'),
                    Videos_Longest=URL('http://www.hd-easyporn.com/?o=d*'),
                    Categories=URL('http://www.hd-easyporn.com/categories/')
                    )

    def startpage(self):
        return URL("http://www.hd-easyporn.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('hd-easyporn.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('section', '', '')])
        startpage_rule.add_activate_rule_level([('div', 'class', 'videos cf')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'data-src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('data-src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        categories_rule = ParserRule()
        # categories_rule.add_activate_rule_level([('section', '', '')])
        categories_rule.add_activate_rule_level([('div', 'class', 'catbox')])
        categories_rule.add_process_rule_level('a', {'href'})
        categories_rule.add_process_rule_level('img', {'data-src', 'alt'})
        categories_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        categories_rule.set_attribute_modifier_function('data-src', lambda x: self.get_href(x, base_url))
        parser.add_rule(categories_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_tags_rule = ParserRule()
        startpage_tags_rule.add_activate_rule_level([('ul', 'class', 'tags cf')])
        startpage_tags_rule.add_process_rule_level('a', {'href'})
        startpage_tags_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_tags_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('video', 'id', 'video_id')])
        video_rule.add_process_rule_level('source', {'src', 'res'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'flashvars' in text)
        video_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'video_header')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():

            urls = UrlList()
            for item in video_rule.get_result():
                urls.add(item['res'], URL(item['src']))
            result.set_video(urls.get_media_data(-1))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            return result

        if startpage_rule.is_result():

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['data-src']), href=URL(item['href']), description=item.get('alt''')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_tags_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

            if base_url.contain('/categories/'):
                result.set_caption_visible(True)

            return result

        if categories_rule.is_result():
            urls = list()
            for item in categories_rule.get_result(['href']):
                if item['href'] in urls:
                    continue
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['data-src']), href=URL(item['href']), description=item.get('alt''')))
                urls.append(item['href'])

            result.set_caption_visible(True)
        return result


if __name__ == "__main__":
    pass
