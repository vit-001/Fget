__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class EPvideoSite(BaseSite):
    def start_button_name(self):
        return "EPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Top_Rated_Video=URL('http://www.eporner.com/top-rated/'),
                    Latest_Video=URL('http://www.eporner.com/0/'),
                    Categories=URL('http://www.eporner.com/categories/'))

    def startpage(self):
        return URL("http://www.eporner.com/0/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('eporner.com/')

    def get_href(self,txt='',base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain()+txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'mb'),
                                                ('div', 'class', 'mbhd'),
                                                ('div', 'class', 'mb mbr'),
                                                ('div', 'class', 'mbhd mbr'),
                                                ('div', 'class', 'categoriesbox')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'numlist2')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href',lambda x: base_url.domain() + x)
        parser.add_rule(startpage_pages_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'id', 'movieplayer-box')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data',lambda x:'getScript' in x)
        parser.add_rule(video_rule)

        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'tab-1')])
        # gallery_href_rule.add_activate_rule_level([('td', 'class', 'btnList')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href',lambda x: base_url.domain() + x)
        gallery_href_rule.set_attribute_filter_function('href',lambda x:'/category/'in x or '/search/'in x)
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if len(video_rule.get_result())>0:
            script_url=URL(base_url.domain() + (video_rule.get_result()[0]['data'].partition("getScript('")[2].partition("'")[0]))
            video=EPvideoParser(script_url,self.model)
            result.set_video(video.get_result())
            result.set_type('video')

            for f in gallery_href_rule.get_result(['data','href']):
                # print(f)
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            # print('return')
            return result

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item['alt']))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))
            #
            # for item in startpage_hrefs_rule.get_result(['href', 'data']):
            #     result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


class EPvideoParser():
    def __init__(self,url=URL(),model=AbstractModelFromSiteInterface()):
        # print ('EPVideoParcer:',url.get())

        script_file=Setting.base_dir+'ep_script.txt'

        if safe_load(url,script_file) is not None:
            # print('Loaded')
            setup=''
            process=False
            for line in open(script_file):
                if process:
                    if ';' in line:
                        setup+=line.partition(';')[0]
                        break
                    else:
                        setup+=line
                elif '.setup' in line:
                    setup=line.rpartition('.setup')[2]
                    process=True

            # print(setup)
            self.process_setup(setup)


    def process_setup(self,text=''):
        sources=text.partition('sources:')[2].partition(']')[0].strip(' [')
        # print(sources)
        records=sources.split('}')
        # print(records)
        alternates=list()
        for item in records:
            file=item.partition('file:')[2].partition(',')[0].strip(' "')
            label=item.partition('label:')[2].partition(',')[0].strip(' "')
            if file!='':
                # print(label,file)
                alternates.append(dict(text=label,url=URL(file)))
        # print (alternates)
        # default=self.find_default(alternates)
        # print('Default ',default)
        self.result=MediaData(self.find_default(alternates))
        for item in alternates:
            self.result.add_alternate(item)

    def find_default(self, alternates):
        preferencies=['720p','360p','1080p']

        for x in preferencies:
            for item in alternates:
                if x in item['text']:
                    return item['url']
        return alternates[0]['url']

    def get_result(self):
        return self.result



if __name__ == "__main__":
    pass




