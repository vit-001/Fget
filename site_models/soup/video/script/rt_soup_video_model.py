__author__ = 'Vit'
from bs4 import BeautifulSoup

from base_classes import UrlList,URL
from site_models.base_site_model import ParseResult,ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite,_iter
from site_models.util import get_href,get_url,quotes


class RTvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "RTvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Recommended=URL('http://www.redtube.com/recommended*'),
                    Newest=URL('http://www.redtube.com/'),
                    Top_Rated=URL('http://www.redtube.com/top*'),
                    Longest=URL('http://www.redtube.com/longest*'),
                    Most_Viewed_By_Week=URL('http://www.redtube.com/mostviewed*'),
                    Most_Favored_By_Week=URL('http://www.redtube.com/mostfavored*'),
                    Most_Viewed_All_Time=URL('http://www.redtube.com/mostviewed?period=alltime*'),
                    Most_Favored_All_Time=URL('http://www.redtube.com/mostfavored?period=alltime*'),
                    Pornstars=URL('http://www.redtube.com/pornstar/alphabetical*'),
                    Channels_Alphabetical=URL('http://www.redtube.com/channel/alphabetical*'),
                    Channels_Top_Rated=URL('http://www.redtube.com/channel/top-rated*'),
                    Channels_Recommended=URL('http://www.redtube.com/channel/recommended*'),
                    Channels_Recently_Updated=URL('http://www.redtube.com/channel/recently-updated*'),
                    Channels_Most_Subscribed=URL('http://www.redtube.com/channel/most-subscribed*'),
                    Channels_Most_Viewed=URL('http://www.redtube.com/channel/most-viewed*')
                    )

    def startpage(self):
        return URL("http://www.redtube.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('redtube.com/')

    def parse_soup(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # parce video page
        video = soup.find('div', {'class': 'watch'})
        if video is not None:
            urls = UrlList()
            script=video.find('script', text=lambda x: 'redtube_flv_player' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\\', '')
                sources=quotes(data,'sources:{','}').split(',')
                for item in sources:
                    file = quotes(item, '":"', '"')
                    label=quotes(item,'"','"')
                    urls.add(label, get_url(file, base_url))

                urls.sort()
                result.set_video(urls.get_media_data(-1))

                # parsing video information
                video_detail=soup.find('div', {'class': 'video-details'})
                # first add user reference
                user_container=video_detail.find('td',{'class':'withbadge'})
                if user_container is not None:
                    user=user_container.find('a')
                    if user is not None:
                        href = user.attrs['href']
                        username = user.string
                        result.add_control(ControlInfo(username , get_url(href,base_url),text_color='blue'))
                # stars in video adding
                stars_container=video_detail.find('ul',{'class':'pornstars-in-video'})
                stars=_iter(stars_container.find_all('li',{'class':None},recursive=False))
                for star in stars:
                    href=star.find('a')
                    if href is not None:
                        info=list(star.find('span',{'class':'pornstar-info'}).stripped_strings)
                        name=info[0]+' '+info[1]
                        url=get_url(href.attrs['href'],base_url)
                        result.add_control(ControlInfo(name, url, text_color='magenta'))
                # other tags
                for links_container in _iter(video_detail.find_all('td', {'class': 'links'})):
                    for href in _iter(links_container.find_all('a',{'href': lambda x: 'javascript' not in x})):
                        if href.string is not None:
                            result.add_control(
                                ControlInfo(str(href.string), get_url(href.attrs['href'], base_url)))
                return result


        thumbnail_containers=soup.find_all('ul', {'class': ['video-listing']})
        channel_containers =soup.find_all('ul', {'class': ['channels-list']})
        stars_containers=soup.find_all('ul', {'class': ['pornStarsThumbs']})

        if thumbnail_containers is not None and len(thumbnail_containers)>0:
            # parce thumbnail page
            for thumbnail_container in thumbnail_containers:
                for thumbnail in _iter(thumbnail_container.find_all('li')):
                    href = get_url(thumbnail.a.attrs['href'], base_url)
                    thumb_url = get_url(thumbnail.img.attrs['data-src'], base_url)
                    label=thumbnail.img.attrs.get('alt','')

                    duration = thumbnail.find('span', {'class': 'video-duration'})
                    dur_time = '' if duration is None else str(duration.string).strip()

                    hd_span = thumbnail.find('span', {'class': 'hd-video'})
                    hd = '' if hd_span is None else '  HD'

                    result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=label,
                                               labels=[{'text':dur_time, 'align':'top right'},
                                                       {'text':label, 'align':'bottom center'},
                                                       {'text': hd, 'align': 'top left'}]))

        elif channel_containers is not None and len(channel_containers)>0:
            # parce channels page
            for channel_container in channel_containers:
                for channel in _iter(channel_container.find_all('li')):
                    href = get_url(channel.a.attrs['href'], base_url)
                    logo=channel.find('span',{'class':'channel-logo'})
                    img=logo.find('img')
                    if img is None:
                        img = channel.find('img')
                    thumb_url = get_url(img.attrs.get('data-src',img.attrs['src']), base_url)
                    label = channel.img.attrs.get('alt', '')

                    num_videos_span = channel.find('span', text=lambda x: 'videos' in str(x))
                    num_videos = '' if num_videos_span is None else str(num_videos_span.string).strip()

                    result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=label,
                                               labels=[{'text': num_videos, 'align': 'top right'},
                                                       {'text': label, 'align': 'bottom center'}]))

        elif stars_containers is not None and len(stars_containers)>0:
            # parce stars page
            print(' Pornhub server blocked. Stars image unavailable')
            for stars_container in stars_containers:
                for star in _iter(stars_container.find_all('li')):
                    # print(thumbnail)

                    href = get_url(star.a.attrs['href'], base_url)
                    img = star.find('img')
                    thumb_url = get_url(img.attrs['src'], base_url)
                    label = img.attrs.get('alt', '')

                    num_videos_span = star.find('span', text=lambda x: 'Videos' in str(x))
                    num_videos = '' if num_videos_span is None else str(num_videos_span.string)

                    # print('============================')
                    result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=label,
                                               labels=[{'text': num_videos, 'align': 'top right'},
                                                       {'text': label, 'align': 'bottom center'}]))
            # adding tags to stars page
            tags_containers = _iter(soup.find_all('ul', {'class': ['abc-categories']}))
            for tags_container in tags_containers:
                for tag in _iter(tags_container.find_all('a')):
                    # print(tag)
                    result.add_control(ControlInfo(str(tag.string), get_url(tag.attrs['href'], base_url)))

        #adding tags to thumbs
        tags_containers = _iter(soup.find_all('ul', {'class': ['categories-listing','categories-popular-listing']}))
        for tags_container in tags_containers:
            for tag in _iter(tags_container.find_all('a')):
                result.add_control(ControlInfo(str(tag.attrs['title']), get_url(tag.attrs['href'], base_url)))

        #adding pages to thumbs
        pagination = soup.find('div', {'class': 'pages'})
        if pagination is not None:
            for page in _iter(pagination.find_all('a')):
                num='' if page.string is None else str(page.string)
                if num.isdigit():
                    result.add_page(ControlInfo(num, get_url(page.attrs['href'], base_url)))

        return result

if __name__ == "__main__":
    pass
