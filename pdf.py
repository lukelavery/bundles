from os import path
from PyPDF2 import PdfMerger, PdfWriter, PdfReader, PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
import PyPDF2
from reportlab.pdfgen import canvas
from models import LineObject
from directory import list_doc_paths
from pathlib import Path
from typing import Iterable, Any
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTPage
from models import TextObject


def pdf_merger(pdf_paths, output_path):
    merger = PdfMerger()

    for pdf in pdf_paths:
        merger.append(pdf)

    merger.write(output_path)
    merger.close()


def pagGen(merged_path, output_path):

    # todo: save as temp file???

    c = canvas.Canvas(output_path)

    reader = PdfReader(merged_path)
    pages = len(reader.pages)

    for i in range(pages):
        x1, y1, x2, y2 = reader.getPage(i).mediaBox

        page_num = c.getPageNumber()
        text = str(page_num)
        c.setFont('Helvetica-Bold', 15)
        c.drawString(x2 - 30, y1 + 20, text)
        c.setPageSize((x2, y2))
        c.showPage()
    c.save()


def applyPag(merged_path, pag_path, output_path):

    reader1 = PdfReader(pag_path)
    writer = PdfWriter()
    reader2 = PdfReader(merged_path)
    page_indices = list(range(0, len(reader2.pages)))

    for index in page_indices:
        image_page = reader1.pages[index]
        content_page = reader2.pages[index]
        mediabox = content_page.mediabox
        content_page.merge_page(image_page)
        content_page.mediabox = mediabox
        writer.add_page(content_page)

    with open(output_path, "wb") as fp:
        writer.write(fp)

    # delete_file(merged_path)
    # delete_file(pag_path)


def generate_docs(user_input, output_path):
    bundle_path = user_input

    docs = list_doc_paths(bundle_path)

    pdf_merger(docs, output_path)


def get_num_pages(pdf):
    page_num = PyPDF2.PdfFileReader(pdf).numPages
    return page_num


def add_links(pdf, line_objects, output_path):
    file = open(pdf, 'rb')
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(file)

    x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
    print(f'x1, x2: {x1, x2}\ny1, y2: {y1,y2}')

    # add each page in pdf to pdf writer
    num_of_pages = pdf_reader.getNumPages()

    for page in range(num_of_pages):
        current_page = pdf_reader.getPage(page)
        pdf_writer.addPage(current_page)

    for line_object in line_objects:
        pagdest = line_object.page
        text_objects = line_object.text_objects

        for text_object in text_objects:
            pagenum = text_object.page
            x1, y1, x2, y2 = text_object.x1, text_object.y1, text_object.x2, text_object.y2
            print(x1, y1, x2, y2)

            pdf_writer.addLink(
                pagenum=pagenum,  # index of the page on which to place the link
                pagedest=pagdest - 1,  # index of the page to which the link should go
                # clickable area x1, y1, x2, y2 (starts bottom left corner)
                rect=RectangleObject([x1, y1, x2, y2]),
                # border
                # fit
            )
            print(pagenum, pagdest)

    with open(path.abspath(output_path), 'wb') as link_pdf:
        pdf_writer.write(link_pdf)
    file.close()


def get_line_objects(bbox_dict):
    line_objects = []
    for v in bbox_dict:
        line_object = LineObject(v, bbox_dict[v])
        line_objects.append(line_object)

    return line_objects


def is_entry(line_objects, doc_names, pag_nums):
    new_doc_names = doc_names.copy()
    new_line_objects = []
    for line_object in line_objects:
        compiled_text = line_object.compiled_text
        for doc in new_doc_names:
            if doc in compiled_text:
                line_object.page = pag_nums[doc_names.index(doc)]
                new_line_objects.append(line_object)
                new_doc_names.remove(doc)
    return new_line_objects


def get_bbox_dict(index_path):
    index = -1
    text_objects = []
    path = Path(index_path).expanduser()

    def show_ltitem_hierarchy(o: Any, index, depth=0):

        if isinstance(o, Iterable):
            for i in o:
                if isinstance(i, LTPage):
                    index += 1
                    print("page")
                if isinstance(i, LTTextBoxHorizontal):
                    x1, y1, x2, y2 = i.bbox
                    text_object = TextObject(
                        i.get_text().strip(), x1, y1, x2, y2, index)
                    text_objects.append(text_object)
                show_ltitem_hierarchy(i, index, depth=depth + 1)

    def sort_list(list):
        list.sort(key=lambda x: (x.page, 1/x.y1))
        y1_dict = {}
        for li in list:
            y1 = li.y1

            if y1 in y1_dict:
                y1_dict[y1].append(li)
            else:
                y1_dict[y1] = [li]
        return y1_dict

    pages = extract_pages(path)

    show_ltitem_hierarchy(pages, index)

    return sort_list(text_objects)
