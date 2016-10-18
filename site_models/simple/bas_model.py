__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo




class BASSite(BaseSite):
    def start_button_name(self):
        return "B&S"

    def startpage(self):
        return URL("http://www.babesandstars.com/galleries/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('babesandstars.com/')

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos=URL('http://www.babesandstars.com/videos/'),
                    Photos=URL('http://www.babesandstars.com/galleries/'),
                    Top100models=URL('http://www.babesandstars.com/top-models/')
        )

    def get_href(self,txt='',base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain()+txt
        return base_url.get().partition('?')[0] + txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        domain = base_url.domain()

        href_rule = ParserRule()  # startpage & model's page
        href_rule.add_activate_rule_level([('div', 'class', 'galleries'),
                                           ('div', 'class', 'models'),
                                           ('div', 'class', 'videos')])
        href_rule.add_activate_rule_level([('div', 'class', 'items')])
        href_rule.add_process_rule_level('a', {'href'})
        href_rule.add_process_rule_level('img', {'src', 'alt'})
        href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        href_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x,base_url))
        parser.add_rule(href_rule)

        href_page_rule = ParserRule()  # page number in model's page
        href_page_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
        href_page_rule.add_process_rule_level('a', {'href'})
        href_page_rule.set_attribute_modifier_function('href', lambda x:self.get_href(x,base_url))
        parser.add_rule(href_page_rule)

        model_litera_rule = ParserRule()
        model_litera_rule.add_activate_rule_level([('span', 'class', 'chars')])
        model_litera_rule.add_process_rule_level('a', {'href'})
        model_litera_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(model_litera_rule)

        picture_rule = ParserRule()  # gallery rule
        picture_rule.add_activate_rule_level([('div', 'class', 'picture')])
        picture_rule.add_process_rule_level('a', {'href'})
        picture_rule.add_process_rule_level('img', {'alt'})
        picture_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(picture_rule)

        video_rule = ParserRule()  # gallery rule
        video_rule.add_activate_rule_level([('div', 'class', 'video')])
        video_rule.add_process_rule_level('source', {'src'})
        # video_rule.add_process_rule_level('img', {'alt'})
        # video_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(video_rule)

        picture_href_rule = ParserRule()  # gallery href's rule
        picture_href_rule.add_activate_rule_level([('div', 'class', 'model')])
        picture_href_rule.add_activate_rule_level([('div', 'class', 'links')])
        picture_href_rule.add_process_rule_level('a', {'href'})
        picture_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult(self)

        if len(video_rule.get_result()) > 0:
            result.set_video(MediaData(URL(video_rule.get_result()[0]['src']+'*')))
            result.set_type('video')

            for f in picture_href_rule.get_result(['href','data']):
                # print(f)
                result.add_control(ControlInfo(text=f['data'], url=URL(f['href'])))
            return result

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            for f in picture_rule.get_result():
                x = FullPictureInfo(abs_href=URL(f['href']), rel_name=f['href'].rpartition('/')[2])
                result.add_full(x)

            for f in picture_href_rule.get_result(['href','data']):
                # print(f)
                result.add_control(ControlInfo(text=f['data'], url=URL(f['href'])))
            return result

        if len(href_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in href_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in model_litera_rule.get_result(['href','data']):
                result.add_control(ControlInfo(item['data'],URL(item['href'])))
            for item in href_page_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))



        return result


if __name__ == "__main__":
    from lib.file_loader import load

    model = TMASite()

    print('http://www.themetart.com/')
    load("http://www.themetart.com/", 'e:/out/index.html')
    model.parse_index_file('e:/out/index.html')

    print('http://www.themetart.com/p/paloma-b/hygm/')
    load("http://www.themetart.com/p/paloma-b/hygm/", 'e:/out/index.html')
    model.parse_index_file('e:/out/index.html')

    print('http://www.themetart.com/p/paloma-b/')
    load("http://www.themetart.com/p/paloma-b/", 'e:/out/index.html')
    model.parse_index_file('e:/out/index.html')





