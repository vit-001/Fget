__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class V24videoSite(BaseSite):
    def start_button_name(self):
        return "V24vid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Most_Recsent=URL('http://www.24videos.tv/latest-updates/'),
                    Videos_Most_Viewed=URL('http://www.24videos.tv/most-popular/'),
                    Videos_Top_Rated=URL('http://www.24videos.tv/top-rated/')
                    )

    def startpage(self):
        return URL("http://www.24videos.tv/latest-updates/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('24videos.tv/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'item  ')])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'data-original', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination-holder')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'player')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'flashvars' in text)
        # video_rule.set_attribute_modifier_function('src',lambda x:self.get_href(x,base_url))
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'info')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():

            urls = UrlList()
            for item in video_rule.get_result():
                flashvars = self.quotes(item['data'].replace(' ', '').replace('\n', '').replace('\t', ''),
                                        'flashvars={', '};').split(',')
                fv = dict()
                for flashvar in flashvars:
                    split = flashvar.partition(':')
                    fv[split[0]] = split[2].strip("'\"")
                files = dict()
                for f in fv:
                    if fv[f].startswith('http://') and fv[f].rpartition('.')[2].strip('/') == 'mp4':
                        file = fv[f]
                        label = fv.get(f + '_text', f)
                        files[label] = file

                for key in sorted(files.keys(), reverse=True):
                    urls.add(key, URL(files[key]))

            result.set_video(urls.get_media_data())

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            return result

        if startpage_rule.is_result():

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['data-original']), href=URL(item['href']),
                                           description=item.get('alt', item.get('title', ''))))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
