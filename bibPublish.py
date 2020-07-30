#!/usr/bin/env python3

'''
bibPublish - publishes bibtex files

(C)opyrights 2020 Albert Weichselbraun
'''

import bibtexparser
import os.path
from bibtexparser.bparser import BibTexParser
from optparse import OptionParser
from json import load

DEFAULT_TEMPLATE = 'wordpress'
TEMPLATE_PATH = os.path.expanduser('~/.bibTexSuite/templates')
TEMPLATE_CONFIG = 'config.json'

REQUIRED_ATTRIBUTES = ('title', 'volume', 'number', 'pages', 'note',
                       'editor', 'address', 'eprint', 'booktitle', 'keywords')

GENERATED_ATTRIBUTES = ('citation', 'coins', '_bibpublish')


class Entry():

    def __init__(self, config):
        self.cleanup = config['string_replacements']
        self.attribute_expansions = config['attribute_expansions']
        self.links = config['links']

    def normalize(self, value):
        for _search, _replace in self.cleanup.items():
            value = value.replace(_search, _replace)
        return value

    def prepare(self, entry):
        keys = set(entry.keys()).union(REQUIRED_ATTRIBUTES)
        for k in keys:
            value = self.normalize(entry[k]) if k in entry else ''
            if k in self.attribute_expansions and value:
                value = self.attribute_expansions[k].format(value)
            entry[k] = value

        entry['author'] = self.format_author(entry)
        entry['coins'] = ''
        entry['outlet'] = self.format_outlet(entry)
        entry['citation'] = '[{ID}] {author} ({year}) "{title}", ' \
            '{outlet}'.format(**entry)
        entry['_bibpublish'] = ''

        for k in self.links:
            if k in entry:
                entry['_'+k] = self.links[k].format(**entry)
        return entry

    def format_author(self, entry):
        authors = []
        for author in entry['author'].split(' and '):
            if ',' not in author:
                firstname, lastname = author.rsplit(' ')
                author = f'{lastname}, {firstname}'
            authors.append(author)

        return authors[0] if len(authors) == 1 else \
            '{} and {}'.format(', '.join(authors[:-1]), authors[-1])

    def format_outlet(self, entry):
        outlet = [entry.get('journal', None),
                  entry.get('booktitle', None),
                  f'ISBN: {entry["isbn"]}' if 'isbn' in entry else None,
                  f'pages: {entry["pages"]}' if 'pages' in entry else None,
                  f'{entry["volume"]}({entry["number"]})'
                  if 'volume' in entry and 'number' in entry else None]
        return ", ".join(filter(None, outlet))


class Template():

    def __init__(self, template_path, bibtex_entries, output_dir):
        self.template_path = template_path
        self.bibtex_entries = bibtex_entries
        self.output_dir = output_dir
        self.config = load(open(os.path.join(template_path, TEMPLATE_CONFIG)))
        self.abstract_template = open(os.path.join(template_path,
                                                   'abstract.html')).read()

    def _load_template(self, section, template_type):
        return open(os.path.join(self.template_path,
                                 section + template_type)).read()

    def _get_relevant_entries(self, section):
        return sorted([entry for entry in bibtex_entries
                       if entry['ENTRYTYPE'] == section],
                      key=lambda x: x['year'],
                      reverse=True)

    def generate_section(self, section):
        html = [self._load_template(section, '-head.html')]
        entry_template = self._load_template(section, '-entry.html')
        for entry in self._get_relevant_entries(section):
            entry = Entry(self.config).prepare(entry)
            html.append(entry_template.format(**entry))
            self.generate_abstract(entry)
        html.append(self._load_template(section, '-foot.html'))
        return html

    def generate_abstract(self, entry):
        if 'abstract' in entry:
            with open(os.path.join(self.output_dir, (entry['ID'] + '.html')),
                      'w') as f:
                f.write(self.abstract_template.format(**entry))

    def generate_html(self):
        html = []
        for section in self.config['output_order']:
            html.extend(self.generate_section(section))

        with open(os.path.join(self.output_dir, 'index.html'), 'w') as f:
            f.write('\n'.join(html))


def parse_options():
    """ parses the options specified by the user """
    parser = OptionParser()
    parser.add_option("-o", "--output-dir", dest="output_dir", default='.',
                      help="output directory.")
    parser.add_option("-t", "--template", dest="template",
                      default=DEFAULT_TEMPLATE,
                      help=f"template to use ({DEFAULT_TEMPLATE}).")
    parser.add_option("--template-path", dest="template_path",
                      default=TEMPLATE_PATH,
                      help=f"specify another template path ({TEMPLATE_PATH}))")

    return parser.parse_args()



'''
MAIN
'''
options, args = parse_options()
parser = BibTexParser()
parser.add_missing_from_crossref = True
with open(args[0]) as bibfile:
    bibtex_entries = bibtexparser.load(bibfile, parser).entries

    template = Template(os.path.join(options.template_path, options.template),
                        bibtex_entries, options.output_dir)
    template.generate_html()
