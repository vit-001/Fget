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


class VPSite(BaseSite):
    def start_button_name(self):
        return "VP"

    def startpage(self):
        return URL("http://www.vibraporn.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('vibraporn.com/')

    def parse_index_file(self, fname, base_url=URL()):
        print(base_url.domain())
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'single_plug')])
        startpage_rule.add_process_rule_level('a', {'href'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        parser.add_rule(startpage_rule)

        # startpage_pages_rule = ParserRule()
        # startpage_pages_rule.add_activate_rule_level([('div', 'id', 'nav')])
        # startpage_pages_rule.add_process_rule_level('a', {'href'})
        # startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.get().partition('?')[0] + x+'*')
        # parser.add_rule(startpage_pages_rule)
        #
        # picture_rule = ParserRule()
        # picture_rule.add_activate_rule_level([('div', 'class', 'gallery_w')])
        # picture_rule.add_process_rule_level('a', set())
        # picture_rule.add_process_rule_level('img', {'src','class'})
        # picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('/tn_', '/'))
        # parser.add_rule(picture_rule)
        #
        # picture_href_rule = ParserRule()
        # picture_href_rule.add_activate_rule_level([('div', 'class', 'tags')])
        # picture_href_rule.add_process_rule_level('a', {'href'})
        # picture_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain()+x)
        # parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = []

        for item in startpage_rule.get_result():
            result.append(item['href'])

        # result = ParseResult(self)
        #
        # if len(startpage_rule.get_result()) > 0:
        #     # print('Startpage rule')
        #     result.set_type('hrefs')
        #     for item in startpage_rule.get_result():
        #         result.add_thumb(
        #             ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']+'*'), description=item.get('alt', '')))
        #
        #     for item in startpage_pages_rule.get_result(['href', 'data']):
        #         result.add_page(ControlInfo(item['data'], URL(item['href'])))
        #
        # if len(picture_rule.get_result()) > 0:
        #     result.set_type('pictures')
        #     i = 1
        #     for f in picture_rule.get_result(['src', 'class']):
        #         # print(f)
        #         result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg' % i))
        #         i += 1
        #
        #     for f in picture_href_rule.get_result():
        #         # print(f)
        #         result.add_control(ControlInfo(f['data'].replace(',',''), URL(f['href'])))
        #
        return result


class VP2Site(BaseSite):
    def start_button_name(self):
        return "VP"

    def startpage(self):
        return URL("http://www.vibraporn.com/")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('vibraporn.com/')

    def parse_index_file(self, fname, base_url=URL()):
        print(base_url.domain())
        parser = SiteParser()
        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('body', '', '')])
        startpage_rule.add_process_rule_level('form', {'action'})
        # startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        parser.add_rule(startpage_rule)

        # startpage_pages_rule = ParserRule()
        # startpage_pages_rule.add_activate_rule_level([('div', 'id', 'nav')])
        # startpage_pages_rule.add_process_rule_level('a', {'href'})
        # startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.get().partition('?')[0] + x+'*')
        # parser.add_rule(startpage_pages_rule)
        #
        # picture_rule = ParserRule()
        # picture_rule.add_activate_rule_level([('div', 'class', 'gallery_w')])
        # picture_rule.add_process_rule_level('a', set())
        # picture_rule.add_process_rule_level('img', {'src','class'})
        # picture_rule.set_attribute_modifier_function('src', lambda text: text.replace('/tn_', '/'))
        # parser.add_rule(picture_rule)
        #
        # picture_href_rule = ParserRule()
        # picture_href_rule.add_activate_rule_level([('div', 'class', 'tags')])
        # picture_href_rule.add_process_rule_level('a', {'href'})
        # picture_href_rule.set_attribute_modifier_function('href', lambda x: base_url.domain()+x)
        # parser.add_rule(picture_href_rule)

        for s in open(fname):
            parser.feed(s)

        result = []

        for item in startpage_rule.get_result():
            result.append(item['action'])

        # result = ParseResult(self)
        #
        # if len(startpage_rule.get_result()) > 0:
        #     # print('Startpage rule')
        #     result.set_type('hrefs')
        #     for item in startpage_rule.get_result():
        #         result.add_thumb(
        #             ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']+'*'), description=item.get('alt', '')))
        #
        #     for item in startpage_pages_rule.get_result(['href', 'data']):
        #         result.add_page(ControlInfo(item['data'], URL(item['href'])))
        #
        # if len(picture_rule.get_result()) > 0:
        #     result.set_type('pictures')
        #     i = 1
        #     for f in picture_rule.get_result(['src', 'class']):
        #         # print(f)
        #         result.add_full(FullPictureInfo(abs_href=URL(f['src']), rel_name='%03d.jpg' % i))
        #         i += 1
        #
        #     for f in picture_href_rule.get_result():
        #         # print(f)
        #         result.add_control(ControlInfo(f['data'].replace(',',''), URL(f['href'])))
        #
        return result


if __name__ == "__main__":
    from lib.__file_loader import load

    domains = dict()

    model = VPSite()
    model2 = VP2Site()

    # http://www.vibraporn.com/?from=15


    for i in range(0, 500, 15):
        site = URL('http://www.vibraporn.com/?from=%d' % i)

        print(site.get())
        load(site, 'e:/out/index.html')
        result = model.parse_index_file('e:/out/index.html')

        for item in result:
            site = URL(item)

            load(site, 'e:/out/index.html')
            result2 = model2.parse_index_file('e:/out/index.html')

            domain = URL(result2[0]).domain()

            print(result2)
            domains[domain] = domains.get(domain, 0) + 1

        print(domains.keys())
