__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

class PDGvideoSite(BaseSite):
    def start_button_name(self):
        return "PDGvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Pornstars=URL('http://toseeporn.com/Actor*'),
                    Home=URL('http://toseeporn.com/*'),
                    Search_Example=URL('http://toseeporn.com/Search=asian%20sex%20diary*')
                    )

    def startpage(self):
        return URL("https://www.porndig.com/video/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('porndig.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'video_item_wrapper video_item_medium')])
        startpage_rule.add_process_rule_level('a', {'href','class','title'})
        startpage_rule.add_process_rule_level('img', {'src','alt'})
        # startpage_rule.set_attribute_filter_function('class',lambda x: x == 'thumbnail')
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        startpage_rule.set_attribute_modifier_function('src',lambda x:self.get_href(x,base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'col-xs-12 content-pagination')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_pages_script_rule = ParserRule()
        startpage_pages_script_rule.add_activate_rule_level([('body', '', '')])
        startpage_pages_script_rule.add_process_rule_level('script', {'src'})
        startpage_pages_script_rule.set_attribute_filter_function('src',lambda x: '/bundle.js' in x)
        parser.add_rule(startpage_pages_script_rule)


        tags_rule = ParserRule()
        tags_rule.add_activate_rule_level([('section', 'id', 'footer-tag')])
        tags_rule.add_process_rule_level('a', {'href'})
        tags_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(tags_rule)

        categories_rule = ParserRule()
        categories_rule.add_activate_rule_level([('ul','class','nav navbar-nav')])
        categories_rule.add_process_rule_level('a', {'href'})
        categories_rule.set_attribute_filter_function('href',lambda x: '/Category/' in x and "#" not in x)
        categories_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(categories_rule)


        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'video_wrapper')])
        video_rule.add_process_rule_level('iframe', {'src'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'angular.' in text)
        video_rule.set_attribute_modifier_function('src',lambda x: self.get_href(x,base_url))
        parser.add_rule(video_rule)
        #
        video_href_rule = ParserRule()
        video_href_rule.add_activate_rule_level([('div', 'class', 'single_description_item_info')])
        video_href_rule.add_process_rule_level('a', {'href'})
        video_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(video_href_rule)

        video_sender_rule = ParserRule()
        video_sender_rule.add_activate_rule_level([('div', 'class', 'video_description_wrapper js_video_description')])
        video_sender_rule.add_process_rule_level('a', {'href'})
        video_sender_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(video_sender_rule)


        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result(): #len(video_rule.get_result()) > 0:

            print(video_rule.get_result())

            frame=URL(video_rule.get_result()[0]['src'])
            from requests_loader import load, LoaderError, get_last_index_cookie

            frame_file = Setting.base_dir + 'frame.html'
            cookie=get_last_index_cookie()
            print(cookie)

            urls=list()
            result.set_type('video')

            try:
                r=load(frame,frame_file, cookie=cookie)

                urls=list()

                setup = r.text.replace(' ', '').partition('vc.player_setup=')[2].partition(';')[0]
                playlist = setup.partition('"playlist":')[2]

                split = playlist.split('"file":"')

                for item in split:
                    if '"label":' in item:
                        part = item.partition('"')
                        url = part[0]
                        label = part[2].partition('"label":"')[2].partition('"')[0]
                        print(label, url)
                        data = dict(text=label, url=URL(url + '*'))
                        urls.append(data)

                if len(urls) == 1:
                    video = MediaData(urls[0]['url'])
                elif len(urls) > 1:
                    video = MediaData(urls[0]['url'])
                    for item in urls:
                        video.add_alternate(item)
                else:
                    return result

                result.set_video(video)

            except LoaderError as err:
                print(err)

            def add_categories(parcer_result,text):
                for f in parcer_result:
                    if text in f['href']:
                        result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))

            parcer_result=video_href_rule.get_result(['data', 'href'])

            add_categories(parcer_result,'/studios/')
            add_categories(parcer_result, '/pornstars/')
            add_categories(parcer_result, '/channels/')

            return result

        if startpage_rule.is_result(): #len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item.get('alt','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                label=item['data'].replace(' ','')
                # print(item)
                if len(label)>0:
                    result.add_page(ControlInfo(label, URL(item['href'])))

            if categories_rule.is_result(['href']):
                for item in categories_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))

            if tags_rule.is_result(['href']):
                for item in tags_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item['data'], URL(item['href'])))


            if startpage_pages_script_rule.is_result():
                print(startpage_pages_script_rule.get_result())

        return result




if __name__ == "__main__":
    pass




