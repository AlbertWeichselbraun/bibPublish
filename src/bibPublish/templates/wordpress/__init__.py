#!/usr/bin/env python

'''
bibPublish template configuration

Template namespaces:
    - fieldname: the original value of a variable
    - _fieldname: the formatted value of the variable based on the specified
                  ATTRIBUTE_FORMAT
    - link_fieldname: formatting of urls based on LINK_FORMAT
    - entry_fieldname: formatting of entries based on ENTRY_FORMAT
'''
import os
import os.path

TEMPLATE_PATH = os.path.dirname(__file__)

# name of the main output file
OUTFILE = 'index.html'

ENTRY_ORDER = ('article', 'inproceedings', 'incollection', 'book',
               'unpublished', 'phdthesis', 'mastersthesis')

ATTRIBUTE_CLEANUP_RULES = {
    '--': '-',
    '\\&': '&amp',
    '\n': ' ',
    '{': '',
    '}': '',
    '\\_': '_'
}

ATTRIBUTE_FORMAT = {
    'ID': '{ID}',
    'author': '<span class="author">{author}</span>',
    'editor': '<span class="editor">, Ed. {editor}</span>',
    'title': '<span class="title" title="{title}">“{f"""<a href="{eprint}">'
             '{title}</a>""" if "eprint" in locals() else title}”</span>',
    'year': '<span class="year">{year}</span>',
    'volume': ', <span class="volume">{volume}</span>',
    'number': '(<span class="number">{number}</span>)',
    'pages': ':<span class="pages">{pages}</span>',
    'journal': '<span class="booktitle">{journal}</span>',
    'booktitle': ' <span class="booktitle">{booktitle}</span>',
    'address': ', <span class="address">{address}</span>',
    'publisher': '<span class="publisher">:{publisher}</span>',
    'school': '<span class="school">{school}</span>',
    'eprint': '{eprint}',
    'note': ', {note}',
    'coins': '',
    'keywords': '{keywords}',
    'abstract': '{abstract}',
}

# links: accessible via link.fieldname
LINK_FORMAT = {
    'eprint': '<a class="download" title="{title}" href="{eprint}">'
              '[PDF]</a>',
    'abstract': '<a class="abstract" title="Abstract" '
                'target="_blank" href="abstract/{ID}.html">'
                '[Abstract]</a>',
    'ID': '<a class="bib" target="_blank" title="Citation"'
          'href="bib/{ID}.bib">[BIB]</a>',
}

#
# entries: accessible via entry.fieldname
ENTRY_FORMAT = {
    'article': '{_author}. ({_year}). {_title}. {_journal}'
               '{_volume}{_number}{_pages}{_note}',
    'inproceedings':  '{_author}. ({_year}). {_title}. {_booktitle}'
                      '{_address}{_note}',
    'incollection': '{_author}. ({_year}). {_title}. {_booktitle}'
                    '{_address}{_publisher}{_pages}',
    'book': '{_author}. ({_year}). {_title}. {_publisher}{_address}',
    'unpublished': '{_author}. ({_year}). {_title}{_note}',
    'phdthesis': '{_author}. ({_year}). {_title}, {_school}',
    'mastersthesis': '{_author}. ({_year}). {_title}, {_school}',
}


#
# class used for publishing supplemental material
#
class SupplementalMaterial():

    def __init__(self, output_dir):
        # setup output directories
        self.output_dir_abstracts = os.path.join(output_dir, 'abstract')
        if not os.path.exists(self.output_dir_abstracts):
            os.makedirs(self.output_dir_abstracts)
        self.output_dir_bib = os.path.join(output_dir, 'bib')
        if not os.path.exists(self.output_dir_bib):
            os.makedirs(self.output_dir_bib)

        # read abstracts template
        self.abstract_template = open(os.path.join(TEMPLATE_PATH,
                                                   'abstract.tmpl')).read()

    def generate(self, entry):
        self.generate_abstract(entry)
        self.generate_bibtex(entry)

    def generate_abstract(self, entry):
        if 'abstract' in entry:
            locals().update(entry)
            with open(os.path.join(self.output_dir_abstracts,
                                   (entry['ID'] + '.html')), 'w') as f:
                f.write(eval("f'''" + self.abstract_template + "'''"))

    def generate_bibtex(self, entry):
        with open(os.path.join(self.output_dir_bib,
                               (entry['ID'] + '.bib')), 'w') as f:
            f.write('@' + entry['ENTRYTYPE'] + '{' + entry['ID'] + ",\n")
            entries = ['   {} = {{{}}}'.format(key, value) for key, value in
                       sorted(entry.items())
                       if key not in ('ENTRYTYPE', 'ID',
                                      'citation') and '_' not in key]
            f.write(',\n'.join(entries))
            f.write('\n}')
