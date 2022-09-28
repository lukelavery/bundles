from directory import get_dir_dict
from test import gen_table


def gen_index(path, index_path):

    # gen_title('template_index.docx', context, index_path)
    dir_dict = get_dir_dict(path)
    doc_names, page_nums = gen_table(dir_dict, index_path, path)
    return doc_names, page_nums
