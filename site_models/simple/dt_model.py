__author__ = 'Vit'

from base_classes import URL, ControlInfo
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


def get_href(txt, base):
    table = [('%3A', ':'),
             ('%2F', '/'),
             ('%3F', '?'),
             ('%26', '&'),
             ('%3D', '=')]
    # print(txt)


    result = ''
    if '&' in txt or '?' in txt:
        txt = txt.replace('?', '&')
        s = txt.split('&')
        # print(s)
        for str in s:
            if str.startswith('url='):
                url = str[4:]
                result = url
    else:
        result = base + txt

    for i in table:
        result = result.replace(i[0], i[1])

    # print(result)

    return result


def _del_thumb(txt=''):
    t = txt.rpartition('/')
    return t[0] + '/' + t[2].replace('t_', '')


class DTSite(BaseSite):
    def __init__(self, model=AbstractModelFromSiteInterface(), base_addr='e:/out/'):
        super().__init__(model, base_addr)
        self.accepted_sites = ['doctorteen.com/']

    def start_button_name(self):
        return "DT"

    def startpage(self):
        return URL("http://www.doctorteen.com/")

    def can_accept_index_file(self, base_url=URL()):
        for site in self.accepted_sites:
            if base_url.contain(site):
                return True
        return False

    def parse_index_file(self, fname, base_url=URL()):
        print(base_url.get(), base_url.domain())
        parser = SiteParser()

        startpage_rule = ParserRule()
        # startpage_rule.add_activate_rule_level([('div', 'id', 'galbox')])
        startpage_rule.add_activate_rule_level([('div', 'class', 'element')])
        startpage_rule.add_activate_rule_level([('div', 'class', 'image')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: get_href(x, base_url.domain()))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pager')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + '/' + x)
        parser.add_rule(startpage_pages_rule)

        picture_trigger_rule = ParserRule()
        picture_trigger_rule.add_activate_rule_level([('div', 'id', 'gal')])
        picture_trigger_rule.add_process_rule_level('a', {'href'})
        parser.add_rule(picture_trigger_rule)

        picture_rule = ParserRule()
        picture_rule.add_activate_rule_level([('div', 'class', 'elementgal')])
        picture_rule.add_process_rule_level('a', set())
        picture_rule.add_process_rule_level('img', {'src', 'style'})
        picture_rule.set_attribute_modifier_function('src', lambda text: _del_thumb(text))
        parser.add_rule(picture_rule)

        for s in open(fname):
            parser.feed(s)

        result = ParseResult()

        if len(startpage_rule.get_result()) > 0:
            result.set_type('hrefs')
            for item in startpage_rule.get_result(['href', 'src']):
                result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href'] + '*'),
                                           popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'] + '*')))

        if len(picture_trigger_rule.get_result()) > 0:
            result.set_type('pictures')
            i = 1
            for f in picture_rule.get_result(['src']):
                if 'style' in f: continue
                url = URL(f['src'])
                path = self.base_addr.rstrip('/') + url.get_path()
                result.set_gallery_path(path)
                # print(f['src'])
                result.add_full(FullPictureInfo(abs_href=URL(f['src']),
                                                abs_name=path + '%03d.jpg' % i))
                i += 1

        return result


if __name__ == "__main__":
    from lib.file_loader import load

    model = DTSite()

    print('http://www.doctorteen.com/')
    load(URL("http://www.doctorteen.com/"), 'e:/out/index.html')
    model.parse_index_file('e:/out/index.html')

    print('http://www.doctorteen.com/index.php?page=gallery&gal=carina_tease_me')
    load(URL("http://www.doctorteen.com/index.php?page=gallery&gal=carina_tease_me*"), 'e:/out/index.html')
    model.parse_index_file('e:/out/index.html')

    print('http://www.doctorteen.com/index.php?page=gallery&gal=beata_steamy_hot')
    load(URL("http://www.doctorteen.com/index.php?page=gallery&gal=beata_steamy_hot*"), 'e:/out/index.html')
    model.parse_index_file('e:/out/index.html')

    print('http://doctorteen.com/index.php?page=gallery&gal=stacey_ripe_fruits')
    load(URL("http://doctorteen.com/index.php?page=gallery&gal=stacey_ripe_fruits*"), 'e:/out/index.html')
    model.parse_index_file('e:/out/index.html')
