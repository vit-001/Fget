__author__ = 'Vit'

from base_classes import URL, ControlInfo, UrlList
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule

from bs4 import BeautifulSoup

class MLvideoSoupSite(BaseSite):
    def start_button_name(self):
        return "MLvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Galleries_Recently_Updated=URL('http://motherless.com/galleries/updated*'),
                    Galleries_Most_Viewed=URL('http://motherless.com/galleries/viewed*'),
                    Galleries_Most_Favorited=URL('http://motherless.com/galleries/favorited*'),
                    Videos_Recent=URL('http://motherless.com/videos/recent*'),
                    Videos_Most_Viewed=URL('http://motherless.com/videos/viewed*'),
                    Videos_Most_Favoritede=URL('http://motherless.com/videos/favorited*'),
                    Videos_Popular=URL('http://motherless.com/videos/popular*'),
                    Videos_Live=URL('http://motherless.com/live/videos*'),
                    Videos_All_Time_Most_Viewed=URL('http://motherless.com/videos/all/viewed*'),
                    Videos_All_Time_Most_Favorited=URL('http://motherless.com/videos/all/favorited*'),
                    Videos_Archived=URL('http://motherless.com/videos/archives*'))

    def startpage(self):
        return URL("http://motherless.com/videos/recent?page=1*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('motherless.com/')

    def parse_index_file(self, fname, base_url=URL()):
        result = ParseResult()

        with open(fname,encoding='utf-8', errors='ignore') as fd:
            soup=BeautifulSoup(fd, "html.parser")

            video = soup.find('div',{'id':'content'})
            if video is not None:
                urls = UrlList()
                is_video=False
                for script in video.find_all('script', text=lambda x: 'jwplayer(' in x):
                    data=str(script.string).replace(' ','')
                    file=self.quotes(data, '"file":"','"')
                    urls.add('DEFAULT', self.get_url(file,base_url))
                    is_video=True
                result.set_video(urls.get_media_data())

                if is_video:
                    user=soup.find('div', {'class':'thumb-member-username'})
                    if user is not None:
                        href=user.find('a').attrs['href']
                        username=href.rpartition('/')[2]

                        result.add_control(ControlInfo('"'+username+' uploads"', URL('http://motherless.com/u/' + username + '*')))
                        result.add_control(ControlInfo('"'+username+' gals"', URL('http://motherless.com/galleries/member/' + username + '*')))


                    tags=soup.find_all('div', {'id':'media-tags-container'})
                    if tags is not None:
                        for item in tags:
                            hrefs=item.find_all('a')
                            for href in hrefs:
                                # print(href)
                                if href.string is not None:
                                    result.add_control(ControlInfo(str(href.string), self.get_url(href.attrs['href'],base_url)))

                    return result

            content=soup.find_all('div',{'class':['content-inner']})
            if content is not None:
                for item in content:
                    thumbs=item.find_all('div',{'class':'thumb'})
                    if thumbs is not None:
                        for thumbnail in thumbs:
                            captions=[s for s in thumbnail.stripped_strings]
                            href=self.get_url(thumbnail.a.attrs['href'],base_url)
                            description=captions[0]
                            thumb_url = self.get_url(thumbnail.img.attrs['src'], base_url)
                            dur_time = captions[1]
                            result.add_thumb(ThumbInfo(thumb_url=thumb_url,href=href,description=description, duration=dur_time, show_description=False))

            tags=soup.find('ul', {'class': 'drop2 hidden-xs'})
            if tags is not None:
                for tag in tags.find_all('a'):
                    result.add_control(ControlInfo(str(tag.string).strip(), self.get_url(tag.attrs['href'],base_url)))

            pagination=soup.find('div', {'class': 'pagination_link'})
            if pagination is not None:
                for page in pagination.find_all('a'):
                    # print(page)
                    if page.string.isdigit():
                        result.add_page(ControlInfo(page.string, self.get_url(page.attrs['href'],base_url)))

        result.set_caption_visible(True)
        return result


        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'sub_menu dark-menu'),
                                                      ('div', 'class', 'sub-menu dark-menu')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url) + '*')
        parser.add_rule(startpage_hrefs_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():
            urls = UrlList()
            for item in video_rule.get_result():
                file = self.quotes(item['data'].replace(' ', ''), '"file":"', '"')
                urls.add('default', URL(file + '*'))

            result.set_video(urls.get_media_data())

            if gallery_user_rule.is_result():
                user = gallery_user_rule.get_result()[0]['href'].rpartition('/')[2]
                result.add_control(ControlInfo('"' + user + ' uploads"', URL('http://motherless.com/u/' + user + '*')))
                result.add_control(
                    ControlInfo('"' + user + ' gals"', URL('http://motherless.com/galleries/member/' + user + '*')))

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'], URL(f['href'])))
            return result

        if startpage_rule.is_result():
            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item.get('title', item.get('data', '')), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass
