'''
Implements the template mechanism used for translating templates to
the corresponding output documents.
'''

import importlib
import os.path

from bibPublish.entry import Entry

TEMPLATE_PATH = 'bibpPublish.tempate.'


class Template():

    def __init__(self, template_name, bibtex_entries, output_dir):
        self.template = importlib.import_module(TEMPLATE_PATH + template_name)
        self.bibtex_entries = bibtex_entries
        self.output_dir = output_dir
        self.abstract_template = open(os.path.join(self.template.TEMPLATE_PATH,
                                                   'abstract.tmpl')).read()

    def _load_template(self, section, template_type):
        return open(os.path.join(self.template_path,
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
            entry = Entry(self.config).format_entry(entry)
            output.append(entry_template.format(**entry))
            self.generate_abstract(entry)
        output.append(self._load_template(section, '-foot.tmpl'))
        return output

    def generate_abstract(self, entry):
        if 'abstract' in entry:
            with open(os.path.join(self.output_dir, (entry['ID'] + '.tmpl')),
                      'w') as f:
                f.write(self.abstract_template.format(**entry))

    def generate_output(self):
        output = []
        for section in self.config['output_order']:
            output.extend(self.generate_section(section))

        with open(os.path.join(self.output_dir, 'index.html'), 'w') as f:
            f.write('\n'.join(output).replace(' . ', '. '))
