'''
Implements the template mechanism used for translating templates to
the corresponding output documents.
'''

import importlib
import os.path

from bibPublish.entry import Entry

TEMPLATE_PATH = 'bibPublish.templates.'


class Template():

    def __init__(self, template_name, bibtex_entries, output_dir):
        self.template = importlib.import_module(TEMPLATE_PATH + template_name)
        self.bibtex_entries = bibtex_entries

        # setup output infrastructure
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_dir_abstracts = os.path.join(output_dir, 'abstract')
        if not os.path.exists(self.output_dir_abstracts):
            os.makedirs(self.output_dir_abstracts)
        self.output_dir_bib = os.path.join(output_dir, 'bib')
        if not os.path.exists(self.output_dir_bib):
            os.makedirs(self.output_dir_bib)

        # read abstracts template
        self.abstract_template = open(os.path.join(self.template.TEMPLATE_PATH,
                                                   'abstract.tmpl')).read()

    def _load_template(self, section, template_type):
        return open(os.path.join(self.template.TEMPLATE_PATH,
                                 section + template_type)).read()

    def _get_relevant_entries(self, section):
        return sorted([entry for entry in self.bibtex_entries
                       if entry['ENTRYTYPE'] == section],
                      key=lambda x: x['year'],
                      reverse=True)

    def generate_section(self, section):
        output = [self._load_template(section, '-head.tmpl')]
        entry_template = self._load_template(section, '-entry.tmpl')
        for entry in self._get_relevant_entries(section):
            entry = Entry(self.template).format_entry(entry)
            output.append(entry_template.format(**entry))

            # set citation key
            entry['citation'] = entry['entry_' + section]
            self.generate_abstract(entry)
            self.generate_bibtex(entry)
        output.append(self._load_template(section, '-foot.tmpl'))
        return output

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

    def generate_output(self):
        output = [self._load_template('', 'head.tmpl')]
        for section in self.template.ENTRY_ORDER:
            output.extend(self.generate_section(section))
        output.append(self._load_template('', 'foot.tmpl'))

        with open(os.path.join(self.output_dir, 'index.html'), 'w') as f:
            f.write('\n'.join(output).replace(' . ', '. '))
