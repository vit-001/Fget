__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from setting import Setting
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class HRvideoSite(BaseSite):
    def start_button_name(self):
        return "HRvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(recent=URL('http://www.heavy-r.com/videos/recent/'),
                    most_viewed=URL('http://www.heavy-r.com/videos/most_viewed/'),
                    top_rated=URL('http://www.heavy-r.com/videos/top_rated/'),
                    featured=URL('http://www.heavy-r.com/videos/featured/'))

    def startpage(self):
        return URL("http://www.heavy-r.com/videos/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('heavy-r.com/')

    def get_href(self, txt='', base_url=URL()):
        if not txt.endswith('/'):
            txt = txt + "*"
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt
        return ''

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'video-item compact')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_categories_rule = ParserRule()
        startpage_categories_rule.add_activate_rule_level([('nav', 'class', 'video-categories')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_categories_rule.add_process_rule_level('a', {'href'})
        # startpage_categories_rule.set_attribute_filter_function('href',lambda x:'/free_porn/' in x)
        startpage_categories_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_categories_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'cat-menu hidden-xs')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        startpage_hrefs_rule.set_attribute_filter_function('href', lambda x: '/free_porn/' in x)
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('video', '', '')])
        video_rule.add_process_rule_level('source', {'src'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        video_rule.set_attribute_modifier_function('src', lambda txt: txt + '*')
        parser.add_rule(video_rule)

        gallery_rule = ParserRule()
        gallery_rule.add_activate_rule_level([('div', 'id', 'galleryImages')])
        gallery_rule.add_process_rule_level('a', {})
        gallery_rule.add_process_rule_level('img', {'src'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        gallery_rule.set_attribute_modifier_function('src', lambda txt: txt.replace('/thumbs/', '/'))
        parser.add_rule(gallery_rule)

        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'tags')])
        gallery_href_rule.add_process_rule_level('a', {'href', 'title'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: (self.get_href(x, base_url)))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'uploaded')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        # gallery_user_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # gallery_user_rule.set_attribute_filter_function('href',lambda x:'/categories/' in x)
        parser.add_rule(gallery_user_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():  # len(video_rule.get_result()) > 0:
            urls = UrlList()
            for item in video_rule.get_result():
                urls.add('default', URL(item['src']))
            result.set_video(urls.get_media_data(-1))

            if gallery_user_rule.is_result():
                user = gallery_user_rule.get_result()[0]['href'].rpartition('/')[2]
                result.add_control(
                    ControlInfo('"' + user + '"', URL('http://www.heavy-r.com/user/' + user + '?pro=videos*')))

            for f in gallery_href_rule.get_result(['href']):
                label = f['data'].strip()
                if label == '':
                    label = f['title']
                result.add_control(ControlInfo(label, URL(f['href'])))

            return result

        if gallery_rule.is_result():
            result.set_type('pictures')
            url = URL(gallery_rule.get_result()[0]['src'] + '*')
            base_dir = url.get_path(base=Setting.base_dir)
            result.set_gallery_path(base_dir)
            for f in gallery_rule.get_result():
                picture = FullPictureInfo(abs_href=URL(f['src'] + '*'), rel_name=f['src'].rpartition('/')[2])
                picture.set_base(base_dir)
                result.add_full(picture)

            for f in gallery_href_rule.get_result(['href']):
                label = f['data'].strip()
                if label == '':
                    label = f['title']
                if '/user/' in f['href']:
                    split = f['href'].rpartition('-')
                    base = split[0].partition('/user/')[0]
                    # print(split)
                    # print(base)
                    result.add_control(ControlInfo(label + ' videos', URL(base + '/uploads-by-user/' + split[2])))
                    result.add_control(
                        ControlInfo(label + ' gals', URL(base + '/uploads-by-user/' + split[2] + '?photos=1')))
                else:
                    result.add_control(ControlInfo(label, URL(f['href'])))

            return result

        if startpage_rule.is_result():
            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_categories_rule.get_result(['href'])) > 0:
                for item in startpage_categories_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('data', ''), URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('data', ''), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
