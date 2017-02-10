__author__ = 'Vit'

from base_classes import URL, ControlInfo
from setting import Setting
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class SMvideoSite(BaseSite):
    def start_button_name(self):
        return "SMvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(recent=URL('http://shockingmovies.com/most-recent/'),
                    most_viewed_week=URL('http://shockingmovies.com/most-viewed-week/'),
                    most_viewed_month=URL('http://shockingmovies.com/most-viewed-month/'),
                    most_viewed_all_time=URL('http://shockingmovies.com/most-viewed/'),
                    top_rated=URL('http://shockingmovies.com/top-rated/'),
                    longest=URL('http://shockingmovies.com/longest/'))

    def startpage(self):
        return URL("http://shockingmovies.com/most-recent/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('shockingmovies.com/')

    def get_href(self, txt='', base_url=URL()):
        txt = txt.strip()
        if not txt.endswith('/'):
            txt = txt + "*"
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt
        # print(base_url.get() + txt)
        return base_url.get().rpartition('/')[0] + '/' + txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'clearfix'),
                                                ('div', 'class', 'row clearfix  video-container')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level(
            [('div', 'class', 'btn-group clearfix full-width pagination-block')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_categories_rule = ParserRule()
        startpage_categories_rule.add_activate_rule_level([('ul', 'class', 'main-nav unstyled-list subCategories')])
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
        video_rule.add_activate_rule_level([('body', '', '')])
        video_rule.add_process_rule_level('script', {''})
        video_rule.set_attribute_filter_function('data', lambda text: 'var urls' in text)
        # video_rule.set_attribute_modifier_function('src',lambda txt:txt+'*')
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
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'video-player-list tag-list-block')])
        gallery_href_rule.add_process_rule_level('a', {'href', 'title'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: (self.get_href(x, base_url)))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'video-player-info row')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        # gallery_user_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # gallery_user_rule.set_attribute_filter_function('href',lambda x:'/categories/' in x)
        parser.add_rule(gallery_user_rule)

        all = ''
        for s in open(fname, encoding='utf-8', errors='ignore'):
            parser.feed(s)  # .replace('</b>','</a>'))
            all += s.replace(' ', '')

        result = ParseResult()

        if 'urls.push({' in all:
            video_url = all.partition('urls.push({')[2].partition('"});')[0].partition('file:"')[2]
            video = MediaData(URL(video_url + '*'))

            result.set_type('video')
            result.set_video(video)

            if gallery_user_rule.is_result():
                # print(gallery_user_rule.get_result())
                user_name = gallery_user_rule.get_result()[0]['data'].strip()
                user_number = gallery_user_rule.get_result()[0]['href'].rpartition('-')[2].rstrip('/')

                # print(user_name, user_number)
                result.add_control(ControlInfo('"' + user_name + '"',
                                               URL('http://shockingmovies.com/uploads-by-user/' + user_number + '/')))
                # result.add_control(ControlInfo(user+' gals', URL('http://motherless.com/galleries/member/'+user+'*')))

            for f in gallery_href_rule.get_result(['href']):
                label = f['data'].strip().strip(',')
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

        if startpage_rule.is_result():  # len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                # print(item)
                href = item['href']
                page_number = href.rpartition('/page')[2].rpartition('.')[0]
                result.add_page(ControlInfo(page_number, URL(href)))
                # print(href,page_number)

            if len(startpage_categories_rule.get_result(['href'])) > 0:
                for item in startpage_categories_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('data', ''), URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('data', ''), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
