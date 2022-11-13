
from os import path
from pathlib import Path
from typing import Any, Iterable

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTPage, LTTextBoxHorizontal
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject
from reportlab.pdfgen import canvas


class Documents:
    def __init__(self, bundle):
        self.bundle = bundle
        self.writer = PdfWriter()
        self.reader = None

    def merge_documents(self, output_path: str):
        """Merge the index and documents in the bundle and into a single file."""

        paths = [self.bundle.index.pdf_path]
        paths += self.bundle.get_paths()
        self._pdf_merger(
            paths, output_path)
        self.reader = PdfReader(output_path)

    def _pdf_merger(self, pdf_paths: list[str], output_path: str):
        """Merge the index and documents in the bundle and into a single file."""
        merger = PdfMerger()

        for pdf in pdf_paths:
            merger.append(pdf)

        merger.write(output_path)
        merger.close()

    def paginate(
        self,
        pag_path: str,
        output_path: str
    ):
        """Paginate the bundle."""

        self._pagGen(pag_path)
        self._applyPag(pag_path, output_path)

    def _pagGen(
        self,
        output_path: str
    ):
        """Generate a pdf document with the same page dimensions as the collated bundle."""
        c = canvas.Canvas(output_path)
        pages = len(self.reader.pages)

        for i in range(pages):
            _, y1, x2, y2 = self.reader.getPage(i).mediaBox

            page_num = c.getPageNumber()
            text = str(page_num)
            c.setFont('Helvetica-Bold', 15)
            c.drawString(x2 - 30, y1 + 20, text)
            c.setPageSize((x2, y2))
            c.showPage()
        c.save()

    def _applyPag(
        self,
        pag_path: str,
        output_path: str
    ):
        """Overlay the collated bundle with the generate page numbers."""
        pag_reader = PdfReader(pag_path)
        page_indices = list(range(0, len(self.reader.pages)))

        for index in page_indices:
            image_page = pag_reader.pages[index]
            content_page = self.reader.pages[index]
            mediabox = content_page.mediabox
            content_page.merge_page(image_page)
            content_page.mediabox = mediabox
            self.writer.add_page(content_page)

        with open(output_path, "wb") as fp:
            self.writer.write(fp)

    def hyperlink(
        self,
        index_path: str,
        bundle_path: str,
        output_path: str
    ):
        bbox_dict = self._get_bbox_dict(index_path)
        line_objects = self._get_line_objects(bbox_dict)
        new_line_objects = self._is_entry(
            line_objects, self.bundle.get_entries())
        self._add_links(bundle_path, output_path,
                        line_objects=new_line_objects)

    def _get_bbox_dict(self, index_path: str):
        index = -1
        text_objects = []
        path = Path(index_path).expanduser()

        def show_ltitem_hierarchy(o: Any, index, depth=0):

            if isinstance(o, Iterable):
                for i in o:
                    if isinstance(i, LTPage):
                        index += 1
                    if isinstance(i, LTTextBoxHorizontal):
                        x1, y1, x2, y2 = i.bbox
                        text_object = TextObject(
                            i.get_text().strip(), x1, y1, x2, y2, index)
                        text_objects.append(text_object)
                    show_ltitem_hierarchy(i, index, depth=depth + 1)

        def sort_list(text_objects):
            text_objects.sort(key=lambda x: (x.page, 1/x.y1))
            y1_dict = {}
            for li in text_objects:
                y1 = li.y1

                if y1 in y1_dict:
                    y1_dict[y1].append(li)
                else:
                    y1_dict[y1] = [li]
            return y1_dict

        pages = extract_pages(path)

        show_ltitem_hierarchy(pages, index)

        return sort_list(text_objects)

    def _get_line_objects(self, bbox_dict):
        line_objects = []
        for v in bbox_dict:
            line_object = LineObject(v, bbox_dict[v])
            line_objects.append(line_object)

        return line_objects

    def _is_entry(self, line_objects, bundle_entries):
        new_bundle_entries = bundle_entries.copy()
        new_line_objects = []

        for lo in line_objects:
            compiled_text = lo.compiled_text

            for be in bundle_entries:
                if be.name in compiled_text:
                    lo.page = be.pag_num
                    new_line_objects.append(lo)
                    new_bundle_entries.remove(be)
                    print(lo.page)

        return new_line_objects

    def _add_links(self, bundle_path, output_path, line_objects):
        file = open(bundle_path, 'rb')
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(file)
        pagdest = self.bundle.index.get_pag_num() + 1

        x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
        # print(f'x1, x2: {x1, x2}\ny1, y2: {y1,y2}')

        # add each page in pdf to pdf writer
        num_of_pages = pdf_reader.getNumPages()

        for page in range(num_of_pages):
            current_page = pdf_reader.getPage(page)
            pdf_writer.addPage(current_page)

        for line_object in line_objects:

            text_objects = line_object.text_objects

            for text_object in text_objects:
                pagenum = text_object.page
                x1, y1, x2, y2 = text_object.x1, text_object.y1, text_object.x2, text_object.y2
                # print(x1, y1, x2, y2)

                pdf_writer.addLink(
                    pagenum=pagenum,  # index of the page on which to place the link
                    pagedest=pagdest - 1,  # index of the page to which the link should go
                    # clickable area x1, y1, x2, y2 (starts bottom left corner)
                    rect=RectangleObject([x1, y1, x2, y2]),
                    # border
                    # fit
                )
            print(pagenum, pagdest)
            pagdest += line_object.page

        with open(path.abspath(output_path), 'wb') as link_pdf:
            pdf_writer.write(link_pdf)
        file.close()


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
