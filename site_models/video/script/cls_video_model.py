__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class CLSvideoSite(BaseSite):
    def start_button_name(self):
        return "CLSvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Most_Recsent=URL('http://ru.tubepornclassic.com/latest-updates/'),
                    Videos_Most_Popular=URL('http://ru.tubepornclassic.com/most-popular/'),
                    Videos_Medium_8to20m=URL(
                        'http://ru.tubepornclassic.com/latest-updates/?duration_to=1200&duration_from=481*'),
                    Videos_Top_Rated=URL('http://ru.tubepornclassic.com/top-rated/'),
                    Videos_Long_20plus=URL('http://ru.tubepornclassic.com/latest-updates/?duration_from=1201*'),
                    Videos_Short=URL('http://ru.tubepornclassic.com/latest-updates/?duration_to=480*'),
                    Categories=URL('http://ru.tubepornclassic.com/categories/')
                    )

    def startpage(self):
        return URL("http://ru.tubepornclassic.com/latest-updates/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('tubepornclassic.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'item  '),
                                                ('div', 'class', 'list-categories')])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'data-original', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('li', {'class'})
        startpage_pages_rule.add_process_rule_level('a', {'href', 'data-query'})
        startpage_pages_rule.set_attribute_filter_function('class', lambda x: x == 'page')
        startpage_pages_rule.set_attribute_modifier_function('data-query', lambda x: x.partition(':')[2])
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)
        #
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
        # gallery_href_rule.set_attribute_filter_function('href',lambda x:'/profiles/' not in x)
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'block-user')])
        gallery_user_rule.add_process_rule_level('a', {'href', 'title'})
        # gallery_user_rule.set_attribute_filter_function('href',lambda x:'/profiles/' in x)
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x + 'videos/', base_url))
        parser.add_rule(gallery_user_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result():

            urls = UrlList()
            for item in video_rule.get_result():
                flashvars = self.quotes(item['data'].replace(' ', '').replace('\n', '').replace('\t', ''),
                                        'flashvars={', '};').split(',')
                fv = dict()
                for flashvar in flashvars:
                    split = flashvar.partition(':')
                    fv[split[0]] = split[2].strip("'\"")

                # file=self.quotes(item['data'],'file:',',').strip(' "')
                urls.add('default', URL(fv['video_url'] + '*'))

            result.set_video(urls.get_media_data())

            for f in gallery_user_rule.get_result(['title', 'href']):
                result.add_control(ControlInfo('"' + f['title'].strip() + '"', URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            return result

        if startpage_rule.is_result():
            for item in startpage_rule.get_result(['href']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['data-original']), href=URL(item['href']),
                                           description=item.get('alt', item.get('title', ''))))

            for item in startpage_pages_rule.get_result(['href', 'data-query']):
                result.add_page(ControlInfo(item['data-query'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
