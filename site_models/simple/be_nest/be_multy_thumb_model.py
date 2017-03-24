__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


def get_href(txt):
    # print(txt)
    if '&' in txt or '?' in txt:
        txt = txt.replace('?', '&')
        s = txt.split('&')
        # print(s)
        for str in s:
            if str.startswith('url='):
                url = str[4:]
                return url
    else:
        return txt


class BEmultiThumbSite(BaseSite):
    # noinspection PyMissingConstructor
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        PJmenu = dict(Pics=URL('http://www.passionatejoy.com/'),
                      Movies=URL('http://www.passionatejoy.com/adult-movies/'))
        FPEmenu = dict(Pics=URL('http://www.freepornerotica.com/'),
                       Movies=URL('http://www.freepornerotica.com/porn-movies/'))
        PBmenu = dict(Pics=URL('http://www.pornobump.com/'), Movies=URL('http://www.pornobump.com/Porno-videos/'))
        FPSmenu = dict(Pics=URL('http://www.freepornosalute.com/'),
                       Movies=URL('http://www.freepornosalute.com/Porno-videos/'))

        NHmenu = dict(Pics=URL('http://www.nuhunter.com/'), Movies=URL('http://www.nuhunter.com/sex-videos/'))
        JPmenu = dict(Pics=URL('http://www.jewelporn.com/'), Movies=URL('http://www.jewelporn.com/adult-movies/'))
        PRmenu = dict(Pics=URL('http://www.pornoreact.com/'), Movies=URL('http://www.pornoreact.com/sex-videos/'))

        self.accepted_sites = [
            {'button': 'PJ', 'start': 'http://www.passionatejoy.com/', 'test': 'passionatejoy.com/', 'menu': PJmenu},
            {'button': 'FPE', 'start': 'http://www.freepornerotica.com/', 'test': 'freepornerotica.com/',
             'menu': FPEmenu},
            {'button': 'PB', 'start': 'http://www.pornobump.com/', 'test': 'pornobump.com/', 'menu': PBmenu},
            {'button': 'FPS', 'start': 'http://www.freepornosalute.com/', 'test': 'freepornosalute.com/',
             'menu': FPSmenu},

            {'button': 'NH', 'start': 'http://www.nuhunter.com/', 'test': 'nuhunter.com/', 'menu': NHmenu},
            {'button': 'JP', 'start': 'http://www.jewelporn.com/', 'test': 'jewelporn.com/', 'menu': JPmenu},
            {'button': 'PR', 'start': 'http://www.pornoreact.com/', 'test': 'pornoreact.com/', 'menu': PRmenu},
            {'button': 'Herge', 'start': 'http://www.hegrebeauties.com/', 'test': 'hegrebeauties.com/'},

            {'button': 'MetArt', 'start': 'http://www.metbabes.com/', 'test': 'metbabes.com/'},
            {'button': 'Femjoy', 'start': 'http://www.femandjoy.com/', 'test': 'femandjoy.com/'},
            {'button': 'FTV', 'start': 'http://www.ftvdreams.com/', 'test': 'ftvdreams.com/'},
            {'button': 'MPL', 'start': 'http://www.mplcuties.com/', 'test': 'mplcuties.com/'},

            {'button': 'XArt', 'start': 'http://www.xartgirls.com/', 'test': 'xartgirls.com/'},
            {'button': 'BravoGirls', 'start': 'http://www.bravogirls.com/', 'test': 'bravogirls.com/'},
            ]
        for item in self.accepted_sites:
            model.register_site_model(ControlInfo(text=item['button'], url=URL(item['start']),
                                                  menu_text_url_dict=item.get('menu', None)))

    def can_accept_index_file(self, base_url=URL()):
        for site in self.accepted_sites:
            if base_url.contain(site['test']):
                return True
        return False

    def get_href(self, txt):
        # print(txt)
        if '&' in txt or '?' in txt:
            txt = txt.replace('?', '&')
            s = txt.split('&')
            # print(s)
            for str in s:
                if str.startswith('http://'):
                    return str
                if str.startswith('url='):
                    url = str[4:]
                    return url
        else:
            return txt

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumbs'),
                                                ('div', 'class', 'movie_thumbs')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', self.get_href)
        parser.add_rule(startpage_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if len(startpage_rule.get_result()) > 0:
            # print('Startpage rule')
            for item in startpage_rule.get_result():
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))
        else:
            print(base_url.get(), ' not parsed by BEmultiThumbSite. Add rule.')

        return result


if __name__ == "__main__":
    pass
