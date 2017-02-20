__author__ = 'Vit'

from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class DudeSite(BaseSite):
    def start_button_name(self):
        return "PornDude"

    def get_start_button_menu_text_url_dict(self):
        return dict(tube_sites=URL('https://theporndude.com/top-porn-tube-sites*'),
                    asian_tube_sites=URL('https://theporndude.com/top-asian-porn-tube-sites*'),
                    arab_tube_sites=URL('https://theporndude.com/top-arab-porn-tube-sites*'),
                    black_tube_sites=URL('https://theporndude.com/top-ebony-porn-tube-sites*'),
                    indian_tube_sites=URL('https://theporndude.com/top-indian-porn-tube-sites*'),
                    latin_tube_sites=URL('https://theporndude.com/top-latin-porn-tube-sites*'),
                    fetish_tube_sites=URL('https://theporndude.com/top-fetish-porn-tube-sites*'),
                    tgp_sites=URL('https://theporndude.com/best-porn-tgp-sites*')
                    )

    def startpage(self):
        return URL("https://theporndude.com/top-porn-tube-sites*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('theporndude.com/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'url_link_container')])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'src'})
        # startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x,base_url))
        # startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x,base_url))
        parser.add_rule(startpage_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if startpage_rule.is_result():
            # result.set_type('hrefs')
            # hrefs=json.dumps(startpage_rule.get_result())
            # print(hrefs)
            acc = 0

            with open('urls.lst', 'w') as fd:
                for item in startpage_rule.get_result(['href']):
                    data = item['data']
                    href = item['href']

                    if '/go/' in href:
                        href = 'http://' + href.partition('/go/')[2]

                    if not href.endswith('/'):
                        href += '/'

                    model = self.model

                    if (model.can_accept_url(URL(href))):
                        l = '{0:<27} {1:<35}- accepted'.format(data, href)
                        acc += 1
                    else:
                        l = '{0:<27} {1:<35}'.format(data, href)

                    print(l)
                    fd.write(l + '\n')
                    # result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),description=item.get('alt',item.get('title',''))))

            print('Accepted=', acc)

        return result


if __name__ == "__main__":
    pass
