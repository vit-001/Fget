__author__ = 'Vit'

from html.parser import HTMLParser
from urllib.request import urlretrieve


class Attribute:
    def __init__(self, attrs):
        self.attrs = attrs

    def get(self, name):
        for attr in self.attrs:
            if attr[0] == name:
                return attr[1]
        return ''


class AnalyserHTMLParser(HTMLParser):
    def __init__(self, tag_to_analyse='div'):
        HTMLParser.__init__(self)
        self.tag_to_analyse = tag_to_analyse
        self.classes = {}

    def handle_starttag(self, tag, attrs):
        # print ("Start tag:", tag)
        # for attr in attrs:
        # print ("     attr:", attr)

        # attr=Attribute(attrs)

        if tag == self.tag_to_analyse:
            for attr in attrs:
                print(attr)


if __name__ == "__main__":
    parser = AnalyserHTMLParser()
    # parser.feed('<html><head><title>Test</title></head>'
    # '<body><h1>Parse me!</h1></body></html>')

    print('loading...')
    urlretrieve("http://www.bravoerotica.com/mpl-studios/tara/bubblicious/", 'e:/out/index.html')
    print('loaded ok.')

    for s in open('e:/out/index.html'):
        parser.feed(s)

    a = {'a', 'b', 'c'}


