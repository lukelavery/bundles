from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx2pdf import convert
from PyPDF2 import PdfReader


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
        return len(PdfReader(self.pdf_path).pages)
