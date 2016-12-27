__author__ = 'Vit'

from base_classes import URL, ControlInfo
from setting import Setting
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class PTvideoSite(BaseSite):
    def start_button_name(self):
        return "PTvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(All_Videos=URL('http://www.porntrex.com/videos?t=a*'),
                    Added_Today=URL('http://www.porntrex.com/videos?t=t*'),
                    Added_This_Week=URL('http://www.porntrex.com/videos?t=w*'),
                    Added_Tis_Month=URL('http://www.porntrex.com/videos?t=m*'),
                    Photo_Most_Recent=URL('http://www.porntrex.com/albums?o=mr*'),
                    Photo_Most_Photos=URL('http://www.porntrex.com/albums?o=mp*'),
                    Photo_Top_Rated=URL('http://www.porntrex.com/albums?o=tr*'),
                    Photo_Most_Viewed=URL('http://www.porntrex.com/albums?o=mv*')
                    )

    def startpage(self):
        return URL("http://www.porntrex.com/videos*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('porntrex.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        # def star_get_url(txt=''):
        #     return txt.partition('(')[2].partition(')')[0]

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'well wellov well-sm'),
                                                ('div', 'class', 'col-sm-4 m-t-15')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt', 'data-original'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'btn-group')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        # startpage_hrefs_rule.set_attribute_filter_function('href',lambda x: '/videos/' in x)
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'container')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'nuevoplayer' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'm-t-10 overflow-hidden catmenu')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule()
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'pull-left user-container')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x + '/videos', base_url))
        gallery_user_rule.set_attribute_filter_function('href', lambda x: '/user/' in x)
        parser.add_rule(gallery_user_rule)

        photo_rule = ParserRule()
        photo_rule.add_activate_rule_level([('div', 'class', 'panel-body')])
        photo_rule.add_process_rule_level('a', {'href'})
        photo_rule.set_attribute_filter_function('href', lambda text: '/photos/' in text)
        photo_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(photo_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():  # len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data']

            urls = list()
            for item in script.split(';'):
                if 'var video' in item:
                    part = item.strip().partition('video_')[2].partition('=')
                    data = dict(text=part[0], url=URL(part[2].strip("'") + '*'))
                    urls.append(data)

            if len(urls) == 1:
                video = MediaData(urls[0]['url'])
            elif len(urls) > 1:
                video = MediaData(urls[-1]['url'])
                for item in urls:
                    video.add_alternate(item)
            else:
                return result

            result.set_type('video')
            result.set_video(video)

            #
            # for f in gallery_channel_rule.get_result(['data', 'href']):
            #     result.add_control(ControlInfo(f['data'], URL(f['href'])))
            if gallery_user_rule.is_result():
                for item in gallery_user_rule.get_result():
                    # print(item)
                    # print('*'+item['data'].strip()+'*')
                    username = item['data'].strip()
                    if username != '':
                        result.add_control(ControlInfo('"' + username + '"', URL(item['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if photo_rule.is_result():
            result.set_type('pictures')
            base_dir = base_url.get_path(base=Setting.base_dir)
            result.set_gallery_path(base_dir)

            for item in photo_rule.get_result():
                name = item['href'].rpartition('/')[2].strip('*')
                picture = FullPictureInfo(abs_href=URL(item['href']), rel_name=name)
                picture.set_base(base_dir)
                result.add_full(picture)

            return result

        if startpage_rule.is_result():  # len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                t_url = self.get_href(item.get('data-original', item['src']), base_url)
                t_href = item['href']
                # print(t_href)
                if '/album/' in t_href:
                    # print(t_href)
                    t_href = t_href.replace('/album/', '/album/slideshow/')
                    # print(t_href)

                result.add_thumb(ThumbInfo(thumb_url=URL(t_url), href=URL(t_href), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('title', item.get('data', '')), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
