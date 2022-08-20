from dir.directory import join_paths
from index.gen_index import gen_index
from pdf.pdf import add_links, applyPag, generate_docs, pagGen, pdf_merger
from test2 import get_bbox_dict
from text_model import LineObject


def gen(path, context, index, bundle):
    index_path = join_paths(path, 'index.docx')
    index_pdf_path = join_paths(path, "index.pdf")
    documents_pdf_path = join_paths(path, "documents.pdf")
    output_path = join_paths(path, "bundle.pdf")
    pag_path = join_paths(path, "pagination.pdf")
    link_path = join_paths(path, "links.pdf")

    doc_names, page_nums = gen_index(path, context, index_path)
    if bundle:
        gen_bundle(path, index_pdf_path, documents_pdf_path,
                   output_path, pag_path, doc_names, page_nums, link_path)


def gen_bundle(path, index_pdf_path, documents_pdf_path, output_path, pag_path, doc_names, pag_nums, link_path):
    generate_docs(path, documents_pdf_path)
    pdf_merger([index_pdf_path, documents_pdf_path], output_path)
    pagGen(output_path, pag_path)
    applyPag(output_path, pag_path, output_path)
    bbox_dict = get_bbox_dict(index_pdf_path)
    line_objects = get_line_objects(bbox_dict)
    new_line_objects = is_entry(line_objects, doc_names, pag_nums)
    add_links(output_path, new_line_objects, link_path)


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
