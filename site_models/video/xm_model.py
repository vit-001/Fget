__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo


class XMvideoSite(BaseSite):
    def start_button_name(self):
        return "XMvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Photos=URL('http://ru.xhamster.com/photos/'))

    def startpage(self):
        return URL("http://ru.xhamster.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('xhamster.com/')

    def get_href(self,txt='',base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain()+txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule(debug=True)
        startpage_rule.add_activate_rule_level([('div', 'class', 'boxC videoList clearfix'),
                                                ('div', 'class', 'gallery')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        # startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pager')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href',lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'id', 'menuLeft')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_modifier_function('href',lambda x: self.get_href(x,base_url))
        startpage_hrefs_rule.set_attribute_filter_function('href',lambda text:'/channels/' in text or
                                                                            '/photos/niches/'in text)
        parser.add_rule(startpage_hrefs_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'id', 'player')])
        video_rule.add_process_rule_level('video', {'file'})
        # video_rule.set_attribute_filter_function('data',lambda text:'function playStart()' in text)
        parser.add_rule(video_rule)

        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'id', 'videoInfoBox'),
                                                   ('div', 'id', 'galleryInfoBox')])
        gallery_href_rule.add_activate_rule_level([('td', 'class', 'btnList')])
        gallery_href_rule.add_process_rule_level('a', {'href','title'})
        gallery_href_rule.set_attribute_modifier_function('href',lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        picture_rule = ParserRule()  # gallery rule
        picture_rule.add_activate_rule_level([('div', 'class', 'gallery iItem ')])
        picture_rule.add_activate_rule_level([('div', 'class', 'img vam')])
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('_160', '_1000'))
        parser.add_rule(picture_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if len(video_rule.get_result())>0:
            result.set_video(MediaData(URL(video_rule.get_result()[0]['file']+'*')))
            result.set_type('video')

            for f in gallery_href_rule.get_result():
                # print(f)
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            i=1
            for f in picture_rule.get_result():
                x = FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg'%i)
                result.add_full(x)
                i+=1
                # print(f['src'])

            for f in gallery_href_rule.get_result():
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item['alt']))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result

    def get_attr_from_script(self,txt=''):
        t=txt.partition('var flashvars = {')[2].partition('}')[0]
        t1=t.split(',')
        for i in t1:
            if i.strip().startswith('video_url:'):
                return i.partition(':')[2].strip(" '")
        return ''


if __name__ == "__main__":
    t=TDvideoSite()
    t.parse_index_file('E:/Dropbox/Hobby/PRG/PyWork/FGet/files/index1.html')




