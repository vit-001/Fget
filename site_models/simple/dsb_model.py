__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo


class DSBSite(BaseSite):
    def start_button_name(self):
        return "DSB"

    def startpage(self):
        return URL("http://www.definebabe.com/")#galleries/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('definebabe.com/')

    def get_href(self,txt='',base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain()+txt
        return base_url.get().partition('?')[0] + txt

    def gal_href_filter(self,x=''):
        if x.find('/galleries/')!=-1:
            return True
        if x.find('/view/')!=-1:
            return True
        return False

    def thumb_href_filter(self,x=''):
        if x.find('/videos/')!=-1:
            return False
        if x.find('/video/')!=-1:
            return False
        if x.find('/gallery/')!=-1:
            return True
        if x.find('/galleries/')!=-1:
            return True
        if x.find('/view/')!=-1:
            return True
        if x.find('/models/')!=-1:
            return True
        return False

    def thumb_src_filter(self,x=''):
        if x.find('none.gif')!=-1:
            return False
        return True

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        domain = base_url.domain()

        href_rule = ParserRule()  # startpage & model's page
        href_rule.add_activate_rule_level([('div', 'id', 'lst-galleries'),
                                           ('div', 'class', 'lblock'),
                                           ('div', 'class', 'modal_info_full')])
        href_rule.add_process_rule_level('a', {'href'})
        href_rule.add_process_rule_level('img', {'src', 'alt'})
        href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        href_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x,base_url))
        href_rule.set_attribute_filter_function('href',self.thumb_href_filter)
        href_rule.set_attribute_filter_function('src',self.thumb_src_filter)
        parser.add_rule(href_rule)

        href_page_rule = ParserRule()  # page number in model's page
        href_page_rule.add_activate_rule_level([('div', 'class', 'pages'),
                                                ('div', 'class', 'cat')])
        href_page_rule.add_process_rule_level('a', {'href'})
        href_page_rule.set_attribute_modifier_function('href', lambda x:self.get_href(x,base_url))
        parser.add_rule(href_page_rule)

        model_litera_rule = ParserRule()
        model_litera_rule.add_activate_rule_level([('div', 'class', 'babe_index')])
        model_litera_rule.add_process_rule_level('a', {'href'})
        model_litera_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(model_litera_rule)

        model_more_rule = ParserRule()
        model_more_rule.add_activate_rule_level([('div', 'class', 'more'),
                                                 ('div', 'id', 'MoreCont')])
        model_more_rule.add_process_rule_level('a', {'href'})
        model_more_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        model_more_rule.set_attribute_filter_function('href',self.thumb_href_filter)
        parser.add_rule(model_more_rule)

        picture_rule = ParserRule()  # gallery rule
        picture_rule.add_activate_rule_level([('div', 'class', 'lblock')])
        # picture_rule.add_activate_rule_level([('ul', 'class', 'block')])
        picture_rule.add_process_rule_level('a', {'href'})
        picture_rule.add_process_rule_level('img', {'alt'})
        picture_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        picture_rule.set_attribute_filter_function('href',lambda x:x.endswith('.jpg'))
        parser.add_rule(picture_rule)

        picture_href_rule = ParserRule()  # gallery href's rule
        picture_href_rule.add_activate_rule_level([('div', 'id', 'ModelMenu'),
                                                   ('div', 'class', 'lblock')])
        picture_href_rule.add_process_rule_level('a', {'href','title'})
        picture_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        picture_href_rule.set_attribute_filter_function('href',self.gal_href_filter)
        parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult(self)

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            i=1
            for f in picture_rule.get_result():
                x = FullPictureInfo(abs_href=URL(f['href']), rel_name='%03d.jpg'%i)
                result.add_full(x)
                i+=1

            for f in picture_href_rule.get_result(['href','title']):
                # print(f)
                result.add_control(ControlInfo(text=f['title'], url=URL(f['href'])))
            return result

        if len(href_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in href_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in model_more_rule.get_result(['href','data']):
                result.add_control(ControlInfo(item['data'],URL(item['href'])))
            for item in model_litera_rule.get_result(['href','data']):
                result.add_control(ControlInfo(item['data'],URL(item['href'])))
            for item in href_page_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))



        return result


if __name__ == "__main__":
    pass


