__author__ = 'Vit'

from html.parser import HTMLParser


class Attribute:
    def __init__(self, attrs=list()):
        self.attrs = attrs

    def get(self, name):
        for attr in self.attrs:
            if attr[0] == name:
                return attr[1]
        return ''

    def __str__(self):
        return self.attrs.__str__()


class ParserRule():
    def __init__(self, debug=False, collect_data=False):

        self.debug = debug
        self.collect_data=collect_data

        self.tag_no_end = ['img', 'meta','param']

        self.result = []

        self.activate = []
        self.activate_level = 0
        self.active = False

        self.process = []
        self.getting_entry = False

        self.modifiers = dict()
        self.filters=dict()

        self.tags = set()
        self.level = 0

    def add_activate_rule_level(self, activate_tag_attr_value_tuples=list()):
        self.activate.append(activate_tag_attr_value_tuples)
        for (tag, attr, value) in activate_tag_attr_value_tuples:
            self.tags.add(tag)

    def add_process_rule_level(self, tag='', attributes=set('')):
        self.process.append((tag, attributes))
        self.tags.add(tag)

    def set_attribute_modifier_function(self, attr='', function=lambda text: text):
        self.modifiers[attr] = function

    def set_attribute_filter_function(self,attr='',function=lambda text:True):
        self.filters[attr]=function

    def process_attrs(self, attrs=Attribute(), attr_set=set()):
        for attribute in attr_set:
            value = attrs.get(attribute)
            if value != '':
                if attribute in self.modifiers:
                    # print (value)
                    value = self.modifiers[attribute](value)
                    # print(value)
                self.current_entry[attribute] = value

    def scan_start_tag(self, tag='', attr=Attribute()):
        if tag in self.tags:
            self.level += 1
            if self.debug: print('  ' * self.level, '<', tag, attr, '>')
            if tag in self.tag_no_end:
                self.level -= 1

        # if self.debug: print('  ' * self.level, '<', tag, attr, '>')

        if self.active:
            if self.getting_entry: return
            (process_tag, process_attr) = self.process[self.process_level]
            if tag == process_tag:
                if self.process_level == 0:
                    self.start_process_level = self.level
                self.process_attrs(attr, process_attr)
                self.process_level += 1
                # self.process_tag = process_tag
                if self.process_level == len(self.process):
                    self.getting_entry = True
                    if tag in self.tag_no_end:
                        self.start_process_level += 1  # ???????????????????????????????
                        self.scan_end_tag(tag)
        else:
            for (rule_tag, rule_attr, rule_attr_value) in self.activate[self.activate_level]:
                if tag == rule_tag and attr.get(rule_attr) == rule_attr_value:
                    self.activate_level += 1
                    if self.activate_level == len(self.activate):
                        self.active = True
                        if self.debug: print('.............Activate............')
                        # if self.debug: print(self.process_level,self.start_process_level)
                        self.current_entry = dict()
                        self.deactive_level = self.level - 1
                        self.process_level = 0
                        self.start_process_level = 0

    def scan_end_tag(self, tag=''):
        # if self.debug: print('  ' * self.level, '</', tag, '>')
        if tag in self.tags:
            if tag not in self.tag_no_end:
                if self.debug: print('  ' * self.level, '</', tag, '>')
                self.level -= 1

        if self.active:
            if self.level == self.start_process_level - 1:
                if self.getting_entry:
                    if self.debug: print('.........Getting entry', self.current_entry)
                    self.result.append(self.current_entry)
                    self.current_entry = dict()
                    self.process_level = 0
                    self.getting_entry = False
                else:
                    self.process_level = 0
            if self.level == self.deactive_level:
                self.active = False
                self.activate_level = 0
                if self.debug: print('...........Deactivate............')


    def scan_data(self, data=''):
        # if self.debug: print('  ' * self.level, data)
        if self.active:
            if self.collect_data:
                self.current_entry['data'] = self.current_entry.get('data','')+data
            else:
                self.current_entry['data'] = data

    def is_result(self, needed_tags=list()):
        return len(self.get_result(needed_tags))>0

    def get_result(self, needed_tags=list()):

        filtered_result=list()
        if len(self.filters)==0:
            filtered_result=self.result
        else:
            for item in self.result:
                flag=True
                for filter_tag in self.filters:
                    if not self.filters[filter_tag](item.get(filter_tag,'')):
                        flag=False
                if flag:
                    filtered_result.append(item)

        if len(needed_tags) == 0:
            return filtered_result
        else:
            corrected_result = list()
            for item in filtered_result:
                for tag in needed_tags:
                    if tag not in item: break
                else:
                    corrected_result.append(item)
            return corrected_result


class SiteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rules = []

    def add_rule(self, rule=ParserRule()):
        self.rules.append(rule)

    def handle_starttag(self, tag, attrs):
        attr = Attribute(attrs)
        for rule in self.rules:
            rule.scan_start_tag(tag, attr)

    def handle_endtag(self, tag):
        for rule in self.rules:
            rule.scan_end_tag(tag)

    def handle_data(self, data):
        # print(data)
        for rule in self.rules:
            rule.scan_data(data)

if __name__ == "__main__":

    from lib.__file_loader import load

    parser = SiteParser()

    models_rule = ParserRule(debug=True)  # all models page rule
    models_rule.add_activate_rule_level([('div', 'class', 'block models')])
    models_rule.add_activate_rule_level([('div', 'class', 'thumbs')])
    models_rule.add_process_rule_level('a', {'href'})
    models_rule.add_process_rule_level('img', {'src', 'alt'})
    models_rule.set_attribute_modifier_function('href', lambda x: "http://www.themetart.com/" + x)
    parser.add_rule(models_rule)

    href_model_page_rule = ParserRule()  # page number in model's page
    href_model_page_rule.add_activate_rule_level([('div', 'class', 'block galleries'),
                                                  ('div', 'class', 'block models')])
    href_model_page_rule.add_activate_rule_level([('ul', 'class', 'pagination')])
    href_model_page_rule.add_process_rule_level('a', {'href'})
    href_model_page_rule.set_attribute_modifier_function('href', lambda x: "http://www.themetart.com/" + x)
    parser.add_rule(href_model_page_rule)

    print('loading...')
    load("http://www.themetart.com/models/", 'e:/out/index.html')
    print('loaded ok.')

    for s in open('e:/out/index.html'):
        parser.feed(s)

    for r in models_rule.get_result():
        print(r)

    print()

    for r in href_model_page_rule.get_result(['data', 'href']):
        print(r)