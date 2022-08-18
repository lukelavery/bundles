from index.title_gen import gen_title
from test import get_dir_dict, gen_table


def gen_index(path, context, index_path, index_pdf_path):

    gen_title('template_index.docx', context, index_path)
    dir_dict = get_dir_dict(path)
    doc_names = gen_table(dir_dict, index_path, path)
    return doc_names
