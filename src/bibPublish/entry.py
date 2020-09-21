#
# Format helpers
#

from typing import Dict


def format_author(author_entry):
    authors = []
    for author in author_entry.replace('\n', ' ').split(' and '):
        if ',' not in author:
            firstname, lastname = author.rsplit(' ', 1)
            author = f'{lastname}, {firstname}'
        authors.append(author)

    return authors[0] if len(authors) == 1 else \
        '{} and {}'.format(', '.join(authors[:-1]), authors[-1])


def format_outlet(entry):
    outlet = [entry.get('journal', None),
              entry.get('booktitle', None),
              f'ISBN: {entry["isbn"]}' if 'isbn' in entry else None,
              f'pages: {entry["pages"]}' if 'pages' in entry else None,
              f'{entry["volume"]}({entry["number"]})'
              if 'volume' in entry and 'number' in entry else None]
    return ", ".join(filter(None, outlet))


#
# Classes
#
class Entry():
    '''
    The Entry class, responsible for formatting a single entry.
    '''

    def __init__(self, template):
        self.template = template

    def normalize(self, value):
        for _search, _replace in self.template.ATTRIBUTE_CLEANUP_RULES.items():
            value = value.replace(_search, _replace)
        return value

    def format_entry(self, entry: Dict[str, str]) -> Dict[str, str]:
        '''
        Returns: a dictionary containing all keys formatted according to
            the format strings specified in the FORMAT dictionary.
        '''
        # format attributes
        locals().update(entry)
        for key, format_string in self.template.ATTRIBUTE_FORMAT.items():
            entry['_' + key] = self.normalize(
                eval("f'''"+format_string+"'''")) if key in entry else ''

        # format links
        for key, format_string in self.template.LINK_FORMAT.items():
            entry['link_' + key] = self.normalize(
                eval("f'''"+format_string+"'''")) if key in entry else ''

        # format bibtex entry
        locals().update(entry)
        for key, format_string in self.template.ENTRY_FORMAT.items():
            entry['entry_' + key] = self.normalize(
                eval("f'''"+format_string+"'''"))

        return entry
