__author__ = 'Vit'

from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite, _iter
from site_models.util import get_href,get_url,quotes


class RGFvideoSite(BaseSoupSite):
    def start_button_name(self):
        return "RGFvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Most_Recent=URL('http://www.realgfporn.com/most-recent/'),
                    Categories=URL('http://www.realgfporn.com/channels/'),
                    Longest=URL('http://www.realgfporn.com/longest/'),
                    Most_Viewed=URL('http://www.realgfporn.com/most-viewed/'),
                    Top_Rated=URL('http://www.realgfporn.com/top-rated/')
                    )

    def startpage(self):
        return URL("http://www.realgfporn.com/most-recent/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('realgfporn.com/')

    def parse_soup(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # parce video page
        content = soup.find('div', {'id': 'mediaspace'})
        if content is not None:
            urls = UrlList()
            is_video = False
            for script in _iter(content.find_all('script', text=lambda x: 'jwplayer(' in x)):
                data = str(script.string).replace(' ', '')
                file = quotes(data, 'file:"', '"')
                urls.add('DEFAULT', get_url(file, base_url))
                is_video = True

            if is_video:
                result.set_video(urls.get_media_data())

                #adding tags to video
                tags=list()
                for item in _iter(soup.find_all('div', {'class': 'more-content'})):
                    for href in _iter(item.find_all('a')):
                        if href.string is not None:
                            if '/user/' in href.attrs['href']:
                                result.add_control(ControlInfo('"'+str(href.string)+'"', get_url(href.attrs['href'], base_url)))
                            else:
                                tags.append(ControlInfo(str(href.string), get_url(href.attrs['href'], base_url)))

                for item in tags:
                    result.add_control(item)

                return result

        # # parce categories page
        # categories = set()
        # for category in _iter(soup.find_all('div', {'class': 'catbox'})):
        #     href = get_url(category.a.attrs['href'], base_url)
        #     thumb_url = get_url(category.img.attrs['data-src'], base_url)
        #     title = str(category.find('div', {'class': 'title'}).string)
        #
        #     if title not in categories:
        #         result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=title,
        #                                    labels=[{'text': title, 'align': 'top right'}]))
        #         categories.add(title)

        # parce thumbnail page
        for thumbnail in _iter(soup.find_all('div',{'class':'post'})):
            href=get_url(thumbnail.a.attrs['href'],base_url)
            description=thumbnail.a.img.attrs['alt']
            thumb_url = get_url(thumbnail.img.attrs['src'], base_url)
            print(description,thumb_url)
            duration=thumbnail.find('b',{'class':'post-duration'})
            if duration is not None:
                dur_time = str(duration.string)
            else:
                dur_time=''
            result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                       labels=[{'text':dur_time, 'align':'top right'},{'text':description, 'align':'bottom center'}]))

        tags_container=soup.find('div',{'class':'site-cats'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a')):
                result.add_control(ControlInfo(str(tag.string), get_url(tag.attrs['href'],base_url)))

        pagination=soup.find('div', {'class': 'pagination'})
        if pagination is not None:
            for page in _iter(pagination.find_all('a')):
                if page.string is not None and page.string.isdigit():
                    result.add_page(ControlInfo(page.string, get_url(page.attrs['href'],base_url)))
        return result


        return result

if __name__ == "__main__":
    pass
