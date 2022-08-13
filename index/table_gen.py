import os
from dir.directory import delete_file, get_dir, get_documents_path, list_docs
from docx import Document
from docx2pdf import convert
from dir.scraper import scrape_file_names
from pdf.pdf import get_num_pages

from index.tbl import add_text, get_table

# index gen


def gen_table(index, bundle_path, output_path):
    doc = Document(index)

    t = get_table(doc)

    docs = list_docs(bundle_path)
    docs_path = get_documents_path(bundle_path)
    docs_dir = get_dir(docs_path)

    table_data = scrape_file_names(docs)

    num_pages_list = []

    for i in range(len(table_data)):
        (date, name) = table_data[i]
        t.add_row()
        new_row = t.rows[-1]
        cells = new_row.cells
        tab = str(i + 1)

        add_text(cells[0], tab + '.', None)
        add_text(cells[1], name, None)
        add_text(cells[2], date, None)

        num_pages_list.append(get_num_pages(
            os.path.join(docs_path, docs_dir[i])))

    # temp file
    doc.save('output.docx')
    convert('output.docx', 'index.pdf')

    index_pag_num = get_num_pages('index.pdf')

    cumulative_pag_num = index_pag_num

    for i in range(len(table_data)):
        (date, name) = table_data[i]
        my_row = t.rows[i + 1]
        cells = my_row.cells

        old_cumulative_pag_num = cumulative_pag_num
        cumulative_pag_num = cumulative_pag_num + num_pages_list[i]

        if num_pages_list[i] > 1:
            add_text(cells[3], str(old_cumulative_pag_num + 1) +
                     ' - ' + str(cumulative_pag_num), 'centre')
        else:
            add_text(cells[3], str(cumulative_pag_num), 'centre')

    doc.save('output.docx')
    convert('output.docx', output_path)
    delete_file('index.pdf')
    delete_file('output.docx')
