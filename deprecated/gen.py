from directory import join_paths
from deprecated.gen_index import gen_index
from pdf import add_links, applyPag, generate_docs, get_line_objects, is_entry, pagGen, pdf_merger
from test2 import get_bbox_dict


def gen(path, bundle):
    index_path = join_paths(path, 'index_template.docx')
    index_pdf_path = join_paths(path, "index.pdf")
    documents_pdf_path = join_paths(path, "documents.pdf")
    output_path = join_paths(path, "bundle.pdf")
    pag_path = join_paths(path, "pagination.pdf")
    link_path = join_paths(path, "links.pdf")

    doc_names, page_nums = gen_index(path, index_path)
    if bundle:
        gen_bundle(path, index_pdf_path, documents_pdf_path,
                   output_path, pag_path, doc_names, page_nums, link_path)
