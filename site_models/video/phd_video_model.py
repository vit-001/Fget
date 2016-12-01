__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load


class PHDvideoSite(BaseSite):
    def start_button_name(self):
        return "PHDvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Featured_Videos=URL('http://www.pornhd.com/?order=featured*'),
                    Newest_Video=URL('http://www.pornhd.com/?order=newest*'),
                    Most_Viewed=URL('http://www.pornhd.com/?order=mostpopular*'),
                    Longest_Video=URL('http://www.pornhd.com/?order=longest*'),
                    Top_Rated_Video=URL('http://www.pornhd.com/?order=toprated*'),
                    Category=URL('http://www.pornhd.com/category?order=alphabetical*'),
                    Channels_Alphabetical=URL('http://www.pornhd.com/channel?order=alphabetical*'),
                    Channels_Most_Popular=URL('http://www.pornhd.com/channel?order=most-popular*'),
                    Channels_Most_Videos=URL('http://www.pornhd.com/channel?order=most-videos*'),
                    Channels_Newest=URL('http://www.pornhd.com/channel?order=newest*')
                    )

    def startpage(self):
        return URL("http://www.pornhd.com/?order=newest*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('pornhd.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('ul', 'class', 'thumbs'),
                                                ('li','class','category')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src','alt','data-original'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pager paging')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('span', {'data-query-key','data-query-value'})
        # startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        channels_rule = ParserRule()
        channels_rule.add_activate_rule_level([('ul', 'class', 'tag-150-list')])
        channels_rule.add_process_rule_level('a', {'href'})
        channels_rule.add_process_rule_level('img', {'src'})
        channels_rule.set_attribute_filter_function('href',lambda x: '/channel/' in x or '/prime/' in x)
        channels_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(channels_rule)

        channel_categories_rule = ParserRule()
        channel_categories_rule.add_activate_rule_level([('ul', 'class', 'link-tag-list long-col')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        channel_categories_rule.add_process_rule_level('span', {'data-query-key','data-query-value'})
        # startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(channel_categories_rule)


        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'player-container')])
        video_rule.add_process_rule_level('script', {})
        video_rule.set_attribute_filter_function('data', lambda text: 'players.push' in text)
        parser.add_rule(video_rule)
        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('ul', 'class', 'video-tag-list')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)



        self.proceed_parcing(parser, fname)

        result = ParseResult(self)

        if video_rule.is_result(): #len(video_rule.get_result()) > 0:
            script = video_rule.get_result()[0]['data'].replace(' ', '').replace('\\', '')
            sources = script.partition("'sources':{")[2].partition('}')[0].split(',')

            urls=list()
            for item in sources:
                part=item.strip("\n\t'").partition("':'")
                if part[2].startswith('http://'):
                    data=dict(text=part[0], url=URL(part[2].strip("'") + '*'))
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

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))
            return result

        def add_key(old, key, value):
            (addr, br, keys) = old.partition('?')
            print(addr, br, keys)
            pairs = keys.split('&')
            print(pairs)
            keys = ''
            found = False
            for pair in pairs:
                if pair.startswith(key):
                    keys += key + '=' + value + '&'
                    found = True
                else:
                    keys += pair + '&'

            if not found:
                keys += key + '=' + value
            return addr + '?' + keys.strip('&')

        def add_pages_info_to_result(rule, description_key='data-query-value'):
            for item in rule.get_result(['data-query-key', 'data-query-value']):
                print(item)
                key = item['data-query-key']
                val = item['data-query-value']
                description=item[description_key].strip('\t')
                old = base_url.get()

                addr = add_key(old, key, val)

                result.add_page(ControlInfo(description, URL(addr + '*')))


        if channels_rule.is_result():
            result.set_type('hrefs')

            for item in channels_rule.get_result():
                # print(item)
                info=item['href'].rpartition('/')[2].strip('*')
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), description=info))

            add_pages_info_to_result(channel_categories_rule, description_key='data')

            # for item in channel_categories_rule.get_result(['data-query-key', 'data-query-value']):
            #     print(item)

            return result

        if startpage_rule.is_result(): #len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                # print(item)
                t_url=item.get('data-original',item['src'])
                result.add_thumb(ThumbInfo(thumb_url=URL(t_url), href=URL(item['href']),description=item.get('alt','')))

            add_pages_info_to_result(startpage_pages_rule)

        return result




if __name__ == "__main__":
    pass




