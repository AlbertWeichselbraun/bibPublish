#!/usr/bin/env python

'''
bibPublish template configuration
'''
from os.path import basename

TEMPLATE_PATH = basename(__file__)

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
    'author': '<span class="author">{author}</span>',
    'editor': '<span class="editor">, Ed. {editor}</span>',
    'title': '<span class="title" title="{title}">“{title}”</span>',
    'volume': '<span class="volume">{volume}</volume>',
    'number': '(<span class="number">{number}</span>)',
    'pages': ':<span class="pages">{pages}</span>',
    'journal': '<span class="booktitle">{journal}</span>',
    'booktitle': ', <span class="booktitle">{booktitle}</span>',
    'address': ', <span class="address">{address}</span>',
    'publisher': '<span class="publisher">:{publisher}</span>',
    'note': ', {note}',
    'coins': '',
    'eprint': '<a class="download" title="{title}" href="{eprint}">'
              '[PDF]</a>',
    'abstract': '<a class="abstract" title="Abstract" '
                'target="_blank" href="abstract/{ID}.html">'
                '[Abstract]</a>',
    'bib': '<a class="bib" target="_blank" title="Citation"'
           'href="bibtex/{ID}.bib">[BIB]</a>',
}

ENTRY_FORMAT = {
    'article': '{author}. ({year}). {title}. {journal} '
               '{number}({volume}):{pages}{note}',
    'inproceedings':  '{author}. ({year}). {title}. {booktitle}'
                      '{address}{note}',
    'incollection': '{author}. ({year}). {title}. {booktitle}'
                    '{address}{publisher}{pages}',
    'book': '{author}. ({year}). {title}. {publisher}{address}',
    'unpublished': '{author}. ({year}). {title}{note}',
    'phdthesis': '{author}. ({year}). {title}, {school}',
    'masterthesis': '{author}. ({year}). {title}, {school}',
}
