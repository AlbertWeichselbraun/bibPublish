#!/usr/bin/env python

from typing import Dict


class HtmlEntryFormatter():
    ''' Formats a bibliographic entry.

    Returns: A dictionary of all relevant fields + the formatted entry in
             'entry'.
    '''

    FORMAT = {'author': '<span class="author">{author}</span>',
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
              'eprint': '<a class="download" title="{title}" href="{eprint}">'
                        '[PDF]</a>',
              'abstract': '<a class="abstract" title="Abstract" '
                          'target="_blank" href="abstract/{ID}.html">'
                          '[Abstract]</a>',
              'bib': '<a class="bib" target="_blank" title="Citation"'
                     'href="bibtex/{ID}.bib">[BIB]</a>',
              }

    CITATION = {
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

    def __init__(self, formatter):
        self.formatter = formatter

    def format_entry(self, entry: Dict[str, str]) -> Dict[str, str]:
        '''
        Returns: a dictionary containing all keys formatted according to
            the format strings specified in the FORMAT dictionary.
        '''
        res = {}
        for key, format_string in self.FORMAT.items():
            res[key] = format_string.format(**entry) if key in entry else ''
        return res
