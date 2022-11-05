from datetime import date
import os
from docx.oxml.ns import qn
from PyPDF2 import PdfReader, PdfFileReader
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from dt import date_to_ymd
from docx.oxml import OxmlElement
from docx2pdf import convert


class TextObject:
    def __init__(self, text, x1, y1, x2, y2, page) -> None:
        self.text = text
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.page = page


class LineObject:
    def __init__(self, y1, t_obj_list, page=None):
        self.text_objects = t_obj_list
        self.y1 = y1
        compiled_text = ''
        for arg in t_obj_list:
            compiled_text += arg.text
            compiled_text += ' '
        self.compiled_text = compiled_text
        self.page = page


class BundleEntry:
    def __init__(self, path, tab) -> None:
        self.path = path
        self.tab = tab
        self.file_name = os.path.split(path)[1]
        self.date = self.get_date_from_file()
        self.name = self.get_name_from_file()
        self.pag_num = PdfFileReader(self.path).numPages

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

    # def get_num_pages(self):
    #     page_num = PdfFileReader(self.path).numPages
    #     return page_num


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


class Bundle:
    def __init__(self, path, index_path):
        self.data = {}
        self.name = date_to_ymd(
            date.today()) + ' ' + os.path.basename(path) + '.pdf'
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

    def get_sections(self):
        return list(self.data.keys())

    def get_entries(self, section):
        return self.data[section]


class Index:
    def __init__(self, path):
        self.headings = ('No.', 'Document', 'Date', 'Page No.')
        self.doc = Document(path)
        self.table = self.find_table()

    def find_table(self):
        def get_cell_text(row_cells):
            for c in row_cells:
                yield c.text

        for t in self.doc.tables:
            if tuple(get_cell_text(t.row_cells(0))) == self.headings:
                return t

    def add_text(self, cell, text, alignment):
        def format_text():
            para = cell.paragraphs[0]
            para_fmt = para.paragraph_format
            para_fmt.space_before = 76200
            para_fmt.space_after = 76200

            if alignment == 'centre':
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        cell.text = text
        format_text()

    def add_heading(self, e):
        def set_table_header_bg_color(cell):
            """
            set background shading for Header Rows
            """
            tblCell = cell._tc
            tblCellProperties = tblCell.get_or_add_tcPr()
            clShading = OxmlElement('w:shd')
            clShading.set(qn('w:fill'), "D5D5D5")
            tblCellProperties.append(clShading)
            return cell

        self.table.add_row()
        cells = self.table.rows[-1].cells
        for cell in cells:
            set_table_header_bg_color(cell)

        self.add_text(cells[0], e.section + '.', None)
        self.add_text(cells[1], e.name, None)

    def add_entry(self, entry):
        self.table.add_row()
        cells = self.table.rows[-1].cells
        self.add_text(cells[0], str(entry.tab) + '.', None)
        self.add_text(cells[1], entry.name, None)
        self.add_text(cells[2], str(entry.date), None)

    def input_table_data(self, bundle_data):
        for key in bundle_data:
            self.add_heading(key)

            for entry in bundle_data[key]:
                self.add_entry(entry)

    def input_pag_nums(self, bundle, offset):
        entry_row = 2

        for key in bundle.data:
            for value in bundle.data[key]:
                entry_cell = self.table.rows[entry_row].cells[3]
                if value.pag_num > 1:
                    self.add_text(entry_cell, str(offset + 1) + ' - ' +
                                  str(offset + value.pag_num), 'centre')
                    offset += value.pag_num
                else:
                    offset += value.pag_num
                    self.add_text(entry_cell, str(offset), 'centre')
                entry_row += 1
            entry_row += 1

    def save(self, output_path):
        self.doc.save(output_path)
        self.doc_path = output_path

    def convert(self, output_path):
        convert(self.doc_path, output_path)
        self.pdf_path = output_path

    def get_pag_num(self):
        return PdfReader(self.pdf_path).numPages
