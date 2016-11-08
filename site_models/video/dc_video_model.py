__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule
from base_classes import URL, ControlInfo
from setting import Setting

from loader import safe_load

import site_models.util as util


class DCvideoSite(BaseSite):
    def start_button_name(self):
        return "DCvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Galleries_Recent=URL('http://www.deviantclip.com/galleries?sort=recent*'),
                    Galleries_Most_Pictures=URL('http://www.deviantclip.com/galleries?sort=pictures*'),
                    Galleries_Top_Rated=URL('http://www.deviantclip.com/galleries?sort=rated*'),
                    Galleries_Most_Viewed=URL('http://www.deviantclip.com/galleries?sort=viewed*'),
                    Videos_Longest=URL('http://www.deviantclip.com/videos?sort=longest*'),
                    Videos_Most_Popular=URL('http://www.deviantclip.com/videos?sort=popular*'),
                    Videos_Recent=URL('http://www.deviantclip.com/videos*'),
                    Videos_Most_Viewed=URL('http://www.deviantclip.com/videos?sort=viewed*'),
                    Videos_Top_Rated=URL('http://www.deviantclip.com/videos?sort=rated*'),
                    Videos_Featured=URL('http://www.deviantclip.com/videos?sort=editorchoice*'))

    def startpage(self):
        return URL("http://www.deviantclip.com/videos*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('deviantclip.com/')

    def get_href(self, txt='', base_url=URL()):
        txt=txt.strip()
        if not txt.endswith('/'):
            txt=txt+"*"
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt
        # print(base_url.get() + txt)
        return base_url.get().rpartition('/')[0]+'/' + txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('span', 'class', 'thumb_container_box short'),
                                                ('span', 'class', 'thumb_container_box long')])
        startpage_rule.add_process_rule_level('a', {'href','title'})
        startpage_rule.add_process_rule_level('img', {'src'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) )
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'main-sectionpaging')])
        # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: util.get_href(x,base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'simple-list simple-list--channels')])
        # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href','title'})
        # startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url) + '*')
        parser.add_rule(startpage_hrefs_rule)
        #
        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('video', '', '')])
        video_rule.add_process_rule_level('source', {'src','id'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        video_rule.set_attribute_modifier_function('src',lambda txt:txt+'*')
        parser.add_rule(video_rule)

        video_script_rule = ParserRule()
        video_script_rule.add_activate_rule_level([('body', '', '')])
        video_script_rule.add_process_rule_level('script', {})
        video_script_rule.set_attribute_filter_function('data', lambda text: 'shows:' in text)
        # video_script_rule.set_attribute_modifier_function('src',lambda txt:txt+'*')
        parser.add_rule(video_script_rule)

        gallery_rule=ParserRule()
        gallery_rule.add_activate_rule_level([('div', 'id', 'slideshow')])
        gallery_rule.add_process_rule_level('a', {'index'})
        gallery_rule.add_process_rule_level('img', {'src'})
        # video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
        gallery_rule.set_attribute_modifier_function('src',lambda txt:txt.replace('/thumbs/','/'))
        parser.add_rule(gallery_rule)

        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'added')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: util.get_href(x,base_url))
        parser.add_rule(gallery_href_rule)

        # gallery_channel_rule = ParserRule()
        # gallery_channel_rule.add_activate_rule_level([('div', 'class', 'video-info-uploaded float-right')])
        # gallery_channel_rule.add_process_rule_level('a', {'href'})
        # gallery_channel_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
        # gallery_channel_rule.set_attribute_filter_function('href',lambda x:'/categories/' in x)
        # parser.add_rule(gallery_channel_rule)

        for s in open(fname, encoding='utf-8',errors='ignore'):
            parser.feed(s)  #.replace('</b>','</a>'))

        result = ParseResult(self)

        if video_script_rule.is_result() or video_rule.is_result():
            files=set()

            script=video_script_rule.get_result()[0]['data'].replace(' ','')
            streams=script.partition('"streams":[')[2].partition('],')[0]
            streams=util.decode_text(streams)
            # print(streams)
            while '"file":"' in streams:
                split=streams.partition('"file":"')
                # print(split)
                split2=split[2].partition('"')
                file=split2[0]+'*'
                streams=split2[2]
                # print(file)
                files.add(file)
            # print(files)

            default_vid = None
            for item in video_rule.get_result():
                files.add(item['src'])
                if 'id' not in item:
                    default_vid = item['src']
                    # print('default=',item['src'])

            # print(files)

            if default_vid is None:
                if len(files)==0: return result
                default_vid=files.pop()
            else:
                files.discard(default_vid)

            video = MediaData(URL(default_vid))
            for item in files:
                video.add_alternate(dict(text=item[-5:-1],url=URL(item)))

            result.set_type('video')
            result.set_video(video)

            for f in gallery_href_rule.get_result(['href']):
                label=f['data'].strip()

                result.add_control(ControlInfo(label, URL(f['href'])))

            return result


        if gallery_rule.is_result():
            result.set_type('pictures')
            url=URL(gallery_rule.get_result()[0]['src']+'*')
            base_dir=url.get_path(base=Setting.base_dir)
            result.set_gallery_path(base_dir)
            for f in gallery_rule.get_result():
                fname=int(f['index'])
                # print(fname)
                picture=FullPictureInfo(abs_href=URL(f['src']+'*'), rel_name='pic{0:03d}.jpg'.format(fname))
                picture.set_base(base_dir)
                result.add_full(picture)

            for f in gallery_href_rule.get_result(['href']):
                label=f['data'].strip()

                result.add_control(ControlInfo(label, URL(f['href'])))

            return result



        if startpage_rule.is_result(): #len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')

            for item in startpage_rule.get_result(['href']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item.get('title','')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            if len(startpage_hrefs_rule.get_result(['href'])) > 0:
                for item in startpage_hrefs_rule.get_result(['href', 'data']):
                    result.add_control(ControlInfo(item.get('title',item.get('data','')), URL(item['href'])))

        return result


if __name__ == "__main__":
    pass




