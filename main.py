import os
import tkinter as tk
from dir.directory import delete_file, list_docs
from gui.gui import Gui
from index.table_gen import gen_table
from pdf.pdf import applyPag, generate_docs, pagGen, pdf_merger
from docx import Document

template_index = 'template_index.docx'

if __name__ == "__main__":
    # index_path = os.path.join(input_path, "index.docx")
    # index_pdf_path = os.path.join(input_path, "index.pdf")
    # documents_pdf_path = os.path.join(input_path, "documents.pdf")
    # output_path = os.path.join(input_path, "bundle.pdf")

    # generate_docs(input_path)
    # gen_index(template_index, context, index_path)
    # gen_table(index_path, input_path, index_pdf_path)
    # pdf_merger([index_pdf_path, documents_pdf_path], "bundle.pdf")
    # pagGen("bundle.pdf", "pagination.pdf")
    # applyPag("bundle.pdf", "pagination.pdf", "bundle.pdf")
    root = tk.Tk()
    root.geometry('400x400')
    gui = Gui(root)
    root.mainloop()
