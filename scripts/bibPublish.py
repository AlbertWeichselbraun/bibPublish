#!/usr/bin/env python3

'''
bibPublish - publishes bibtex files

(C)opyrights 2020 Albert Weichselbraun
'''

import bibtexparser
from bibtexparser.bparser import BibTexParser
from optparse import OptionParser

from bibPulish import Template

DEFAULT_TEMPLATE = 'wordpress'


def parse_options():
    """ parses the options specified by the user """
    parser = OptionParser()
    parser.add_option("-o", "--output-dir", dest="output_dir", default='.',
                      help="output directory.")
    parser.add_option("-t", "--template", dest="template",
                      default=DEFAULT_TEMPLATE,
                      help=f"template to use ({DEFAULT_TEMPLATE}).")
    return parser.parse_args()


'''
MAIN
'''
options, args = parse_options()
parser = BibTexParser()
parser.add_missing_from_crossref = True
with open(args[0]) as bibfile:
    bibtex_entries = bibtexparser.load(bibfile, parser).entries

    template = Template(options.template, bibtex_entries, options.output_dir)
    template.generate_output()
