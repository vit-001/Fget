__author__ = 'Vit'
from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite,_iter
from site_models.util import get_href,get_url,quotes


class PXvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "PXvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Best_Recent=URL('http://www.pornoxo.com/'),
                    Most_popular=URL('http://www.pornoxo.com/most-viewed/page1.html?s*'),
                    Latest=URL('http://www.pornoxo.com/newest/page1.html?s*'),
                    Top_Rated=URL('http://www.pornoxo.com/top-rated/page1.html?s*'),
                    Longest=URL('http://www.pornoxo.com/longest/page1.html?s*'))

    def startpage(self):
        return URL("http://www.pornoxo.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('pornoxo.com/')

    def parse_soup(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # parce video page
        video = soup.find('div', {'class': 'videoDetail'})
        if video is not None:
            urls = UrlList()
            script=video.find('script', text=lambda x: 'jwplayer(' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\t', '').replace('\n', '')
                if 'sources:' in data:
                    sources=quotes(data,'sources:[{','}]').split('},{')
                    for item in sources:
                        file = quotes(item, 'file:"', '"')
                        label=quotes(item,'label:"','"')
                        urls.add(label, get_url(file, base_url))
                elif "filefallback':" in data:
                    file=quotes(data,'filefallback\':"','"')
                    urls.add('DEFAULT', get_url(file, base_url))

                result.set_video(urls.get_media_data(-1))

                #adding "user" to video
                user = soup.find('div', {'class': 'user-card'})
                if user is not None:
                    href = user.find('a').attrs['href']
                    username = user.find('span',{'class':'name'}).string
                    result.add_control(ControlInfo(username , get_url(href,base_url),text_color='blue'))

                #adding tags to video
                for item in _iter(soup.find_all('div', {'class': 'content-tags'})):
                    for href in _iter(item.find_all('a')):
                        if href.string is not None:
                            result.add_control(
                                ControlInfo(str(href.string), get_url(href.attrs['href'], base_url)))

                return result

        # parce thumbnail page
        for thumbnail in _iter(soup.find_all('li', {'class': 'thumb-item'})):
            href = get_url(thumbnail.a.attrs['href'], base_url)
            thumb_url = get_url(thumbnail.img.attrs['src'], base_url)
            label=thumbnail.img.attrs.get('alt','')

            duration = thumbnail.find('span', {'class': 'fs11 viddata flr'})
            dur_time = '' if duration is None else str(duration.contents[-1])

            hd_span = thumbnail.find('span', {'class': 'text-active bold'})
            hd = '' if hd_span is None else str(hd_span.string)

            result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=label,
                                       labels=[{'text':dur_time, 'align':'top right'},
                                               {'text':label, 'align':'bottom center'},
                                               {'text': hd, 'align': 'top left'}]))

        #adding tags to thumbs
        tags_container = soup.find('div', {'class': 'left-menu-box-wrapper'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a',{'href':lambda x: '/videos/' in x})):
                result.add_control(ControlInfo(str(tag.string).strip(), get_url(tag.attrs['href'], base_url)))

        #adding pages to thumbs
        pagination = soup.find('div', {'class': 'pagination'})
        if pagination is not None:
            for page in _iter(pagination.find_all('a',{'class': None})):
                if page.string.isdigit():
                    result.add_page(ControlInfo(page.string, get_url(page.attrs['href'], base_url)))

        return result

if __name__ == "__main__":
    pass
