__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class VPmultiSite(BaseSite):
    # noinspection PyMissingConstructor
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        self.accepted_sites = [
            {'button': 'TA', 'start': 'http://www.temptingangels.org/own', 'test': 'temptingangels.org/',
             'rule': ('div', 'class', 'thumbnail')},
            {'button': 'RP', 'start': 'http://www.rossoporn.com/galleries', 'test': 'rossoporn.com/',
             'rule': ('div', 'class', 'plugs')},
            {'button': 'BC', 'start': 'http://www.babecentrum.com/galleries', 'test': 'babecentrum.com/',
             'rule': ('article', 'class', 'col4 size1 gallery')},
            {'button': 'DYB', 'start': 'http://www.dirtyyoungbitches.com/galleries', 'test': 'dirtyyoungbitches.com/',
             'rule': ('div', 'id', 'index_picture')},
            {'button': 'RPB', 'start': 'http://www.redpornblog.com/galleries', 'test': 'redpornblog.com/',
             'rule': ('div', 'class', 'contentblock')},
            {'button': 'SKP', 'start': 'http://www.sexykittenporn.com/galleries', 'test': 'sexykittenporn.com/',
             'rule': ('div', 'class', 'item')},
            {'button': 'P&S', 'start': 'http://www.pureandsexy.org/own', 'test': 'pureandsexy.org/',
             'rule': ('div', 'class', 'picturecontainer')},
            {'button': 'NS', 'start': 'http://www.novostrong.com/galleries', 'test': 'novostrong.com/',
             'rule': ('div', 'class', 'single_plug')},
            {'button': 'CT', 'start': 'http://www.chickteases.com/galleries', 'test': 'chickteases.com/',
             'rule': ('div', 'class', 'runout2')}]
        for item in self.accepted_sites:
            model.register_site_model(ControlInfo(item['button'], URL(item['start'])))

    def can_accept_index_file(self, base_url=URL()):
        for site in self.accepted_sites:
            if base_url.contain(site['test']):
                return True
        return False

    def get_href(self, txt='', base_url=URL()):
        if txt.startswith('http://'):
            return txt
        if txt.startswith('/'):
            return base_url.domain() + txt + '*'
        return base_url.get().partition('?')[0] + txt + '*'

    def parse_index_file(self, fname, base_url=URL()):
        site = None
        for s in self.accepted_sites:
            if base_url.contain(s['test']):
                site = s

        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([site['rule']])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pager'),
                                                      ('div', 'class', 'navbartext'),
                                                      ('div', 'class', 'navigation'),
                                                      ('div', 'class', 'pager'),
                                                      ('div', 'class', 'col-md-12 pager'),
                                                      ('ul', 'id', 'pager')])
        startpage_pages_rule.add_process_rule_level('a', {'href', 'alt'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('article', 'class', 'b-margin-40 g148 gallery'),
                                              ('div', 'class', 'wrapper_g'),
                                              ('td', 'style', 'background:#ededed;'),
                                              ('div', 'id', 'gallerycont'),
                                              ('div', 'class', 'galleryblock'),
                                              ('div', 'class', 'list gallery'),
                                              ('div', 'class', 'picturecontainer mainpics'),
                                              ('div', 'class', 'single_thumb'),
                                              ('div', 'class', 'minithumbs')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src'})
        picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('/tn_', '/').replace('_tn_', '_'))
        parser.add_rule(picture_rule)

        for s in open(fname, encoding='utf-8'):
            parser.feed(s)

        result = ParseResult()

        if len(startpage_rule.get_result()) > 0:
            # print('Startpage rule')
            result.set_type('hrefs')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

        if len(picture_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result(['src']):
                # print(f)
                result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg' % i))
                i += 1

        return result


if __name__ == "__main__":
    pass
