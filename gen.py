from dir.directory import join_paths
from index.gen_index import gen_index
from pdf.pdf import applyPag, generate_docs, pagGen, pdf_merger


def gen(path, context, index, bundle):
    index_path = join_paths(path, 'index.docx')
    index_pdf_path = join_paths(path, "index.pdf")
    documents_pdf_path = join_paths(path, "documents.pdf")
    output_path = join_paths(path, "bundle.pdf")
    pag_path = join_paths(path, "pagination.pdf")

    if index:
        gen_index(path, context, index_path, index_pdf_path)
    if bundle:
        gen_bundle(path, index_pdf_path, documents_pdf_path,
                   output_path, pag_path)


def gen_bundle(path, index_pdf_path, documents_pdf_path, output_path, pag_path):
    generate_docs(path, documents_pdf_path)
    pdf_merger([index_pdf_path, documents_pdf_path], output_path)
    pagGen(output_path, pag_path)
    applyPag(output_path, pag_path, output_path)
    # print('Done')
