__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class TSPvideoSite(BaseSite):
    def start_button_name(self):
        return "TSPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Pornstars=URL('http://toseeporn.com/Actor*'),
                    Home=URL('http://toseeporn.com/*'),
                    Search_Example=URL('http://toseeporn.com/Search=asian%20sex%20diary*')
                    )

    def startpage(self):
        return URL("http://toseeporn.com/Category/West%20Porn*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('toseeporn.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'fixed-content')])
        startpage_rule.add_process_rule_level('a', {'href','class'})
        startpage_rule.add_process_rule_level('div', {'style'})
        startpage_rule.set_attribute_filter_function('class',lambda x: x == 'thumbnail')
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        startpage_rule.set_attribute_modifier_function('style',lambda x:x.partition("url('")[2].partition("')")[0])
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'col-xs-12 content-pagination')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

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
        video_rule.add_activate_rule_level([('body', '', '')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'angular.' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'row tag-area')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result(): #len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '')
            json_file_url=self.get_href(self.quotes(script,"host:'","'"),base_url)
            # print(json_file_url)

            from requests_loader import load, LoaderError

            json_file = Setting.base_dir + 'tsp_video.json'

            urls=list()
            result.set_type('video')

            try:
                r=load(URL(json_file_url),json_file)

                links=set()
                for item in r.json()['mediaSources']:
                    # print(item)
                    if item['source'] not in links:
                        data = dict(text=item['quality'], url=URL(item['source'] + '*'))
                        urls.append(data)
                        links.add(item['source'])

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

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))
            return result

        if startpage_rule.is_result(): #len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                result.add_thumb(ThumbInfo(thumb_url=URL(item['style']), href=URL(item['href']),description=item.get('alt','')))

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

        return result




if __name__ == "__main__":
    pass




