__author__ = 'Vit'

from urllib.parse import urlparse, parse_qs

from base_classes import URL, ControlInfo
from requests_loader import load
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class DFPvideoSite(BaseSite):
    def start_button_name(self):
        return "DFPvid"

    def startpage(self):
        return URL("http://donfreeporn.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('donfreeporn.com/')

    def parse_index_file(self, fname, base_url=URL()):

        parser = SiteParser()

        def star_get_url(txt=''):
            return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumb')])
        startpage_rule.add_process_rule_level('a', {'title', 'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'wp-pagenavi')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'list')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'id', 'video')])
        video_rule.add_process_rule_level('iframe', {'src'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'flashvars' in text)
        parser.add_rule(video_rule)

        fake_video_rule = ParserRule()
        fake_video_rule.add_activate_rule_level([('div', 'id', 'video')])
        fake_video_rule.add_process_rule_level('div', {})
        # video_rule.set_attribute_filter_function('data', lambda text: 'flashvars' in text)
        parser.add_rule(fake_video_rule)

        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'id', 'extras')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():  # len(video_rule.get_result()) > 0:
            # for item in video_rule.get_result():
            #     print(item)

            src = video_rule.get_result()[0]['src']
            query = parse_qs(urlparse(video_rule.get_result()[0]['src'])[4])

            alternates = list()

            if 'f' in query:
                data = {'data': query['f'][0]}
                php_url = 'http://donfreeporn.com/wp-content/themes/detube/Htplugins/Loader.php*'
                url = URL(php_url, 'POST', post_data=data)

                r = load(url)
                video_url = URL(r.json()['l'][0])
            else:
                r = load(URL(src))
                setup = self.quotes(r.text, 'jwplayer("vplayer").setup(', ');').replace(' ', '')
                sources = self.quotes(setup, 'sources:[{', '}],').split('},{')
                for item in sources:
                    if '.mp4' in item:
                        # print(item)
                        file = self.quotes(item, 'file:"', '"')
                        label = self.quotes(item, 'label:"', '"')
                        # print(file,label)
                        alternates.append(dict(text=label, url=URL(file + '*')))
                if len(alternates) == 0:
                    return result
                video_url = alternates[0]['url']

            video = MediaData(video_url)
            for item in alternates:
                video.add_alternate(item)

            result.set_type('video')
            result.set_video(video)

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if fake_video_rule.is_result():
            print('Broken video on this url')
            return result

        if startpage_rule.is_result():  # len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('title', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href']):
                href = item['href']
                label = href.split('/')[-2]
                # print(label,href)
                result.add_control(ControlInfo(label, URL(href)))

        return result


if __name__ == "__main__":
    pass
