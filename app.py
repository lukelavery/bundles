from datetime import date
import os
import tempfile

import tkinter as tk
from tkinter import BOTH, RIGHT, Label, PhotoImage, ttk
from tkinter import filedialog

import constants as const
from directory import get_dir_dict, join_paths
from doc import gen_table
from dt import date_to_ymd
from pdf import add_links, applyPag, generate_docs, get_bbox_dict, get_line_objects, is_entry, pagGen, pdf_merger


class App:
    def __init__(self, master):
        self.input_path = ''
        self.output_path = ''
        self.dir_dict = None
        self.index_path = ''
        self.bundle_name = ''

        self.decl(master)
        self.styles(master)
        self.layout()

        self.init_tree()

    def decl(self, master):
        self.input_entry_text = tk.StringVar()
        self.output_entry_text = tk.StringVar()
        self.style = ttk.Style()

        # background
        self.bg_image = PhotoImage(file=const.BG_IMAGE)
        self.bg_label = Label(master, image=self.bg_image)

        # frames
        self.title_frame = tk.Frame(master)
        self.path_frame = tk.Frame(master)
        self.tree_frame = tk.Frame(master)
        self.button_frame = tk.Frame(master)
        self.pb_frame = tk.Frame(master)

        # title
        self.title_label = tk.Label(self.title_frame, text=const.TITLE_STR)

        # paths
        self.input_label = tk.Label(self.path_frame, text=const.INPUT_STR)
        self.input_button = ttk.Button(
            self.path_frame, text="...", style='TButton', command=self.get_input_path)
        self.input_entry = ttk.Entry(self.path_frame, width=36,
                                     textvariable=self.input_entry_text)

        self.output_label = tk.Label(
            self.path_frame, text=const.OUTPUT_STR)
        self.output_button = ttk.Button(
            self.path_frame, text="...", style='TButton', command=self.get_output_path)
        self.output_entry = ttk.Entry(self.path_frame, width=36,
                                      textvariable=self.output_entry_text)

        # tree view
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)

        # buttons
        self.btn1 = tk.Button(self.button_frame,
                              text=const.DATA_BTN_STR,
                              width=20,
                              height=2,
                              command=self.get_data)
        self.btn2 = tk.Button(self.button_frame,
                              text=const.GEN_BTN_STR,
                              width=20,
                              height=2,
                              command=lambda: self.generate(master))

        # progress bar
        self.pb = ttk.Progressbar(
            self.pb_frame,
            orient='horizontal',
            mode='determinate',
            length=280
        )

    def layout(self):
        # background
        self.bg_label.place(relx=1.0, rely=0.0, anchor='ne')

        # title
        self.title_label.pack()
        self.title_frame.pack(pady=(25, 20))

        # paths
        self.input_label.grid(column=0, row=0, columnspan=2)
        self.input_button.grid(column=1, row=1)
        self.input_entry.grid(column=0, row=1)

        self.output_label.grid(
            column=0, row=2, columnspan=2, pady=(10, 0))
        self.output_button.grid(column=1, row=3)
        self.output_entry.grid(column=0, row=3)

        self.path_frame.pack(pady=10)

        # tree view
        self.tree_scroll.pack(side=RIGHT, fill=BOTH)
        self.tree.pack(pady=(00, 10), padx=(15, 0))
        self.tree_frame.pack(pady=20)

        # buttons
        self.btn1.grid(column=0, row=0, padx=(0, 20))
        self.btn2.grid(column=1, row=0, padx=(20, 0))
        self.button_frame.pack()

        # progress bar
        self.pb.pack()
        self.pb_frame.pack(pady=(25, 0))

    def styles(self, master):
        self.style.theme_use('vista')

        # background
        master.configure(bg=const.BG_COLOR)
        self.bg_label.configure(bg=const.BG_COLOR)

        # frames
        self.title_frame.configure(bg=const.BG_COLOR)
        self.path_frame.configure(bg=const.BG_COLOR)
        self.button_frame.configure(bg=const.BG_COLOR)
        self.tree_frame.configure(bg=const.BG_COLOR)

        # title
        self.title_label.configure(
            fg=const.FG_COLOR, bg=const.BG_COLOR, font=const.TITLE_FONT)

        # paths
        self.style.configure('TButton', background=const.BG_COLOR)
        self.input_label.configure(bg=const.BG_COLOR)
        self.output_label.configure(bg=const.BG_COLOR)

        # tree view
        self.tree_scroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # buttons
        self.btn1.configure(background=const.BUTTON_1_BG_COLOR,
                            foreground=const.FG_COLOR, font=const.H1_FONT, relief='solid', borderwidth=1)
        self.btn2.configure(background=const.FG_COLOR,
                            foreground=const.BUTTON_2_FG_COLOR, font=const.H1_FONT, relief='solid', borderwidth=1)

    def init_tree(self):
        self.tree['columns'] = ("Tab", "Name", "Date")
        self.tree.column("#0", minwidth=25, width=125)
        self.tree.column("Tab", width=30)
        self.tree.column("Name", width=200)
        self.tree.column("Date", width=100)

        self.tree.heading("#0", text="Section")
        self.tree.heading("Tab", text="Tab")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date", text="Date")

    def get_input_path(self):
        self.input_path = filedialog.askdirectory()
        self.input_entry_text.set(self.input_path)
        self.bundle_name = date_to_ymd(
            date.today()) + ' ' + os.path.basename(self.input_path) + '.pdf'
        self.index_path = os.path.join(self.input_path, 'index_template.docx')

    def get_output_path(self):
        self.output_path = filedialog.askdirectory()
        self.output_entry_text.set(self.output_path)

    def get_data(self):
        index = 0
        self.dir_dict = get_dir_dict(self.input_path)

        self.tree.delete(*self.tree.get_children())

        for key in self.dir_dict:
            self.tree.insert('', index='end', iid=index, text=key)
            data = self.dir_dict[key]
            parent_index = index
            index = index + 1

            for i in range(len(data)):
                entry = data[i]
                self.tree.insert(parent=str(parent_index), index='end',
                                 iid=index, values=(entry.tab, entry.name, entry.date))
                index = index + 1

        for child in self.tree.get_children():
            self.tree.item(child, open=True)

    def generate(self, master):
        tmpdir = tempfile.TemporaryDirectory()
        index_pdf_path = join_paths(tmpdir.name, "index.pdf")
        index_doc_path = join_paths(tmpdir.name, "index.docx")
        documents_pdf_path = join_paths(tmpdir.name, "documents.pdf")
        bundle_path = join_paths(tmpdir.name, "bundle.pdf")
        pag_path = join_paths(tmpdir.name, "pagination.pdf")
        output_path = join_paths(self.output_path, self.bundle_name)
        if self.dir_dict != None and self.output_path != '':
            self.pb['value'] = 10
            master.update_idletasks()
            self.doc_names, self.pag_nums = gen_table(self, master,
                                                      self.dir_dict, self.index_path, self.input_path, index_pdf_path, index_doc_path)
            self.gen_bundle(master, index_pdf_path, documents_pdf_path,
                            bundle_path, pag_path, output_path)
            tmpdir.cleanup()
            os.startfile(self.output_path)

        else:
            print('No Data!')

    def gen_bundle(self, master, index_pdf_path, documents_pdf_path, output_path, pag_path, link_path):
        generate_docs(self.input_path, documents_pdf_path)
        self.pb['value'] = 70
        master.update_idletasks()
        pdf_merger([index_pdf_path, documents_pdf_path], output_path)
        self.pb['value'] = 75
        master.update_idletasks()
        pagGen(output_path, pag_path)
        self.pb['value'] = 80
        master.update_idletasks()
        applyPag(output_path, pag_path, output_path)
        self.pb['value'] = 85
        master.update_idletasks()
        bbox_dict = get_bbox_dict(index_pdf_path)
        line_objects = get_line_objects(bbox_dict)
        new_line_objects = is_entry(
            line_objects, self.doc_names, self.pag_nums)
        add_links(output_path, new_line_objects, link_path)
        self.pb['value'] = 100
