import os
from PyPDF2 import PdfMerger, PdfWriter, PdfReader
import PyPDF2
from reportlab.pdfgen import canvas

from dir.directory import delete_file, list_docs


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
        page_num = c.getPageNumber()
        text = str(page_num)
        c.drawString(550, 30, text)
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
    document_paths = []

    docs = list_docs(bundle_path)

    for doc in docs:
        doc_path = os.path.join(bundle_path, "Documents", doc)
        document_paths.append(doc_path)

    pdf_merger(document_paths, output_path)


def get_num_pages(pdf):
    page_num = PyPDF2.PdfFileReader(pdf).numPages
    return page_num
