import os
import tempfile
from datetime import date
from PyPDF2 import PdfReader
from documents import Documents
from index import Index


class Bundle:
    def __init__(self, path, index_path):
        self.data = {}
        self.name = f'{date.today().year}.{date.today().month}.{date.today().day} {os.path.basename(path)}.pdf'
        tab = 1

        for d in os.listdir(path):
            entry_list = []
            sub_dir = os.path.join(path, d)

            if os.path.isdir(sub_dir):
                section = BundleSection(sub_dir)

                for f in os.listdir(sub_dir):
                    entry_list.append(BundleEntry(
                        path=os.path.join(sub_dir, f), tab=tab))
                    tab = tab + 1

                self.data[section] = entry_list

        self.index = Index(index_path)
        self.documents = Documents(self)

    def get_tmpdir(self):
        tmpdir = tempfile.TemporaryDirectory()

        self.paths.update({
            'index_pdf_path': os.path.join(tmpdir.name, "index.pdf"),
            'index_doc_path': os.path.join(tmpdir.name, "index.docx"),
            'documents_pdf_path': os.path.join(
                tmpdir.name, "documents.pdf"),
            'bundle_path': os.path.join(tmpdir.name, "bundle.pdf"),
            'pag_path': os.path.join(tmpdir.name, "pagination.pdf"),
            'output_path': os.path.join(
                self.paths['output_path'], self.bundle.name)
        })

        return tmpdir

    def get_sections(self):
        return list(self.data.keys())

    def get_entries(self, section=None):
        if section != None:
            return self.data[section]
        else:
            entries = []
            for key in self.data:
                for entry in self.data[key]:
                    entries.append(entry)
            return entries

    def get_paths(self):
        paths = []
        for key in self.data:
            for entry in self.data[key]:
                paths.append(entry.path)
        return paths


class BundleEntry:
    def __init__(self, path, tab) -> None:
        self.path = path
        self.tab = tab
        self.file_name = os.path.split(path)[1]
        self.date = self.get_date_from_file()
        self.name = self.get_name_from_file()
        self.pag_num = len(PdfReader(self.path).pages)

    def get_date_from_file(self):
        date_str = self.file_name[0:10]
        year = int(date_str[:4])
        month = int(date_str[5:7])
        day = int(date_str[8:])
        return date(year, month, day)

    def get_name_from_file(self):
        name = self.file_name[13:]
        name = name[:-4]
        return name


class BundleSection:
    def __init__(self, path):
        self.dir_name = os.path.split(path)[1]
        self.section, self.name = self.scrape_dir_name()
        self.path = path

    def scrape_dir_name(self):
        dir_name = self.dir_name
        for i in range(len(dir_name)):
            if dir_name[i] == '.' and dir_name[i + 1] == ' ':
                return dir_name[:i], dir_name[i+2:]
