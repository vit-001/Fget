__author__ = 'Vit'
from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite,_iter
from site_models.util import get_href,get_url,quotes

class PCvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "PCvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Channels=URL('http://www.porn.com/channels*'),
                    Stars=URL('http://www.porn.com/pornstars?o=n*'),
                    Categories=URL('http://www.porn.com/categories*'),
                    Video_Longest=URL('http://www.porn.com/videos?o=l*'),
                    Video_Newest=URL('http://www.porn.com/videos'),
                    Video_Top_Rated_Week=URL('http://www.porn.com/videos?o=r7*'),
                    Video_Top_Rated_Month=URL('http://www.porn.com/videos?o=r30*'),
                    Video_Top_Rated_All_Time=URL('http://www.porn.com/videos?o=r*'),
                    Video_Popular_Week=URL('http://www.porn.com/videos?o=f7*'),
                    Video_Popular_Month=URL('http://www.porn.com/videos?o=f30*'),
                    Video_Popular_All_Time=URL('http://www.porn.com/videos?o=f*'),
                    Video_Viewed_Week=URL('http://www.porn.com/videos?o=v7*'),
                    Video_Viewed_Month=URL('http://www.porn.com/videos?o=v30*'),
                    Video_Viewed_All_Time=URL('http://www.porn.com/videos?o=v*')
                    )

    def startpage(self):
        return URL("http://www.porn.com/videos*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('.porn.com/')

    def parse_soup(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):

        mainw = soup.find('div', {'class': ['mainw','profileContent']})

        # parce video page
        head = soup.find('head')
        if head is not None:

            script=head.find('script',text=lambda x:'streams:' in str(x))
            if script is not None:
                urls = UrlList()
                data = str(script).replace(' ', '')
                sources = quotes(data, 'streams:[{', '}]').split('},{')
                for f in sources:
                    label = quotes(f, 'id:"', '"')
                    url = get_url(quotes(f, 'url:"', '"'),base_url)
                    if url.contain('.mp4'):
                        urls.add(label, url)

                result.set_video(urls.get_media_data(-1))

                # adding tags to video
                vid_source=mainw.find('div',{'class':'vidSource'})
                for item in _iter(vid_source.find_all('a',href=lambda x: '#' not in x)):
                    color=None
                    href=item.attrs['href']
                    if '/pornstars/' in href:
                        color='magenta'
                        href +='/videos'
                    if '/profile/' in href:
                        color='blue'
                        href += '/videos'
                    label=str(item.string)
                    result.add_control(ControlInfo(label, get_url(href,base_url), text_color=color))

                return result

        # parce thumbnail page
        thumbs_list = mainw.find('ul', {'class': ['listThumbs', 'listChannels','listProfiles','listTags']})
        if thumbs_list is not None:
            for thumbnail in _iter(thumbs_list.find_all('li')):
                href = thumbnail.a.attrs['href']
                url=get_url(href,base_url)

                hd_span = thumbnail.find('span', {'class': 'hd'})
                hd = '' if hd_span is None else '  HD'

                if '/videos/' in href or '/pornstars/' in href:
                    thumb_url = get_url(thumbnail.img.attrs['src'], base_url)

                    duration = thumbnail.find('span', {'class': 'added'})
                    dur_time = '' if duration is None else str(duration.string)

                    caption = thumbnail.find('a', {'class': ['title','name']})
                    label = '' if caption is None else str(caption.string)

                    result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=url, popup=label,
                                               labels=[{'text': dur_time, 'align': 'top right'},
                                                       {'text': label, 'align': 'bottom center'},
                                                       {'text': hd, 'align': 'top left'}]))
                elif '/channels/' in href:
                    logo=thumbnail.find('img',{'class':'logo'})
                    thumb_url = get_url(logo.attrs['src'], base_url)

                    title = thumbnail.find('span', {'class': 'title'})
                    label = '' if title is None else str(title.string)

                    count_span = thumbnail.find('span', {'class': 'count'})
                    count = '' if count_span is None else str(count_span.string)

                    result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=url, popup=label,
                                               labels=[{'text': count, 'align': 'top right'},
                                                       {'text': label, 'align': 'bottom center'},
                                                       {'text': hd, 'align': 'top left'}]))

        # adding tags to thumbs
        tags_container = soup.find('div', {'class': 'listFilters'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a',{'class':None})):
                title = tag.attrs.get('title', '')
                count = tag.find('span', {'class': 'count'})
                count_str = '' if count is None else count.string
                result.add_control(ControlInfo('{0}({1})'.format(title, count_str), get_url(tag.attrs['href'], base_url)))

        # adding alpha to thumbs
        alpha_container = soup.find('div', {'class': 'alpha'})
        if alpha_container is not None:
            for alpha in _iter(alpha_container.find_all('a')):
                result.add_control(ControlInfo(str(alpha.string), get_url(alpha.attrs['href'], base_url)))

        #adding pages to thumbs
        pagination = soup.find('div', {'class': 'pager'})
        if pagination is not None:
            for page in _iter(pagination.find_all('a')):
                if page.string.isdigit():
                    result.add_page(ControlInfo(page.string, get_url(page.attrs['href'], base_url)))

        return result

if __name__ == "__main__":
    pass
