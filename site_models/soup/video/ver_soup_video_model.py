__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from bs4 import BeautifulSoup

class VERvideoSoupSite(BaseSite):
    def start_button_name(self):
        return "VERvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Videos_Most_Recsent=URL('https://www.veronicca.com/videos?o=mr*'),
                    Videos_Most_Viewed=URL('https://www.veronicca.com/videos?o=mv*'),
                    Videos_Most_Commented=URL('https://www.veronicca.com/videos?o=md*'),
                    Videos_Top_Rated=URL('https://www.veronicca.com/videos?o=tr*'),
                    Videos_Top_Favorited=URL('https://www.veronicca.com/videos?o=tf*'),
                    Videos_Longest=URL('https://www.veronicca.com/videos?o=lg*'),
                    Channels=URL('https://www.veronicca.com/channels*')
                    )

    def startpage(self):
        return URL("https://www.veronicca.com/videos?o=mr*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('veronicca.com/')

    def parse_index_file(self, fname, base_url=URL()):

        result = ParseResult()
        with open(fname,encoding='utf-8', errors='ignore') as fd:
            soup=BeautifulSoup(fd,'lxml')

            video = soup.find('div',{'class':'video-container'})

            if video is not None:
                urls = UrlList()
                for source in video.find_all('source'):
                    urls.add(source.attrs['res'], self.get_url(source.attrs['src'],base_url))
                result.set_video(urls.get_media_data(-1))

                user=soup.find('div', {'class':'pull-left user-container'})
                for string in user.stripped_strings:
                    print(string)
                print(user.stripped_strings)
                if user is not None:

                    hrefs=user.find_all('a', href=lambda x: '#' not in x)
                    for href in hrefs:
                        # print(href)
                        # print(href.attrs, href.string)
                        result.add_control(ControlInfo(str(href.string), self.get_url(href.attrs['href'],base_url)))



                tags=soup.find_all('div', {'class':'m-t-10 overflow-hidden'})
                if tags is not None:
                    for item in tags:
                        hrefs=item.find_all('a')
                        for href in hrefs:
                            result.add_control(ControlInfo(str(href.string), self.get_url(href.attrs['href'],base_url)))



                # tags=soup.find_all('div', {'class':'m-t-10 overflow-hidden'})
                # # print(tags)
                # for item in tags:
                #     hrefs=item.find_all('a')
                #     for href in hrefs:
                #         print(href.attrs['href'],str(href.string))
                #     print('===========')
                # print(len(tags))

                # for f in gallery_user_rule.get_result(['data', 'href']):
                #     result.add_control(ControlInfo('"' + f['data'].strip() + '"', URL(f['href'])))
                #
                # for f in gallery_href_rule.get_result(['data', 'href']):
                #     result.add_control(ControlInfo(f['data'], URL(f['href'])))

                return result



            for thumbnail in soup.find_all('div',{'class':'well well-sm hover'}):
                # print(thumbnail)
                href=self.get_url(thumbnail.a.attrs['href'],base_url)
                description=thumbnail.a.img.attrs['alt']
                if len(description)>35:
                    description=description[:35]+'...'
                thumb_url = self.get_url(thumbnail.img.attrs['src'], base_url)
                duration = thumbnail.find('div', {'class': "duration"}).contents[0].strip()+'\n'

                result.add_thumb(ThumbInfo(thumb_url=thumb_url,href=href,description=duration+description))

            tags=soup.find('ul', {'class': 'drop2 hidden-xs'})
            if tags is not None:
                for tag in tags.find_all('a'):
                    result.add_control(ControlInfo(str(tag.string).strip(), self.get_url(tag.attrs['href'],base_url)))

            pagination=soup.find('ul', {'class': 'pagination'})
            if pagination is not None:
                for page in pagination.find_all('a'):
                    if page.string.isdigit():
                        result.add_page(ControlInfo(page.string, self.get_url(page.attrs['href'],base_url)))


        result.set_caption_visible(True)
        return result




        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'well well-sm hover'),
                                                ('div', 'class', 'channelContainer')])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)


        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'm-t-10 overflow-hidden')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        gallery_user_rule = ParserRule(collect_data=True)
        gallery_user_rule.add_activate_rule_level([('div', 'class', 'pull-left user-container')])
        gallery_user_rule.add_process_rule_level('a', {'href'})
        gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        gallery_user_rule.set_attribute_filter_function('href', lambda x: '#' not in x)
        parser.add_rule(gallery_user_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():
            urls = UrlList()
            for item in video_rule.get_result():
                urls.add(item['res'], URL(item['src']))

            result.set_video(urls.get_media_data(-1))

            for f in gallery_user_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo('"' + f['data'].strip() + '"', URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))

            return result

        if startpage_rule.is_result():
            for item in startpage_rule.get_result(['href']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),
                                           description=item.get('alt', item.get('title', ''))))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                label = item['href'].strip('*').rpartition('/')[2]
                result.add_control(ControlInfo(label, URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
