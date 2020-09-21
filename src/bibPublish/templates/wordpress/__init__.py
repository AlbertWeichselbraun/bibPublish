#!/usr/bin/env python

'''
bibPublish template configuration
'''
from os.path import dirname

TEMPLATE_PATH = dirname(__file__)

ENTRY_ORDER = 'article',
ENTRY_ORDER = ('article', 'incollection', 'inproceedings', 'book',
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
    'title': '<span class="title" title="{title}">“{title}”</span>',
    'year': '<span class="year">{year}</span>',
    'volume': '<span class="volume">{volume}</span>',
    'number': ' (<span class="number">{number}</span>)',
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

# links: accessible via url_eprint
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
# entries: accessible via _entry
ENTRY_FORMAT = {
    'article': '{author}. ({year}). {title}. {journal} '
               '{volume}{number}{pages}{note}',
    'inproceedings':  '{author}. ({year}). {title}. {booktitle}'
                      '{address}{note}',
    'incollection': '{author}. ({year}). {title}. {booktitle}'
                    '{address}{publisher}{pages}',
    'book': '{author}. ({year}). {title}. {publisher}{address}',
    'unpublished': '{author}. ({year}). {title}{note}',
    'phdthesis': '{author}. ({year}). {title}, {school}',
    'mastersthesis': '{author}. ({year}). {title}, {school}',
}
