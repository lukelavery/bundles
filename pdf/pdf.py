from os import path
from PyPDF2 import PdfMerger, PdfWriter, PdfReader, PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
import PyPDF2
from reportlab.pdfgen import canvas
from text_model import LineObject

from dir.directory import list_doc_paths


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
        c.drawString(x2 - 30, y1 + 30, text)
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
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open(pdf, 'rb'))

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


def get_line_objects(bbox_dict):
    line_objects = []
    for v in bbox_dict:
        line_object = LineObject(v, bbox_dict[v])
        line_objects.append(line_object)

    return line_objects


def is_entry(line_objects, doc_names, pag_nums):
    print(pag_nums)
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
