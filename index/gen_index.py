import os
from index.table_gen import gen_table

from index.title_gen import gen_title


def gen_index(path, context, index_path, index_pdf_path):

    gen_title('template_index.docx', context, index_path)
    gen_table(index_path, path, index_pdf_path)
