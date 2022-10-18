from datetime import date
import os
from PyPDF2 import PdfReader, PdfFileReader


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
        self.pag_num = self.get_num_pages()

    def get_date_from_file(self):
        date_str = self.file_name[0:10]
        year = int(date_str[:4])
        month = int(date_str[5:7])
        day = int(date_str[8:])
        return date(year, month, day)

    def get_name_from_file(self):
        name = self.file_name[13:]
        # only works when len(file_extension) = 3
        name = name[:-4]
        return name

    def get_num_pages(self):
        page_num = PdfFileReader(self.path).numPages
        return page_num
