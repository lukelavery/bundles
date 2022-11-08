import os
import tempfile
import tkinter as tk
from tkinter import BOTH, RIGHT, Label, PhotoImage, ttk
from tkinter import filedialog
import constants as const
from directory import join_paths
from models import Bundle
from pdf import add_links, applyPag, generate_docs, get_bbox_dict, get_line_objects, is_entry, pagGen, pdf_merger


class App:
    def __init__(self, master):
        self.paths = {}

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
        self.tree.column("#0", width=0)
        self.tree.column("Tab", width=30)
        self.tree.column("Name", width=300)
        self.tree.column("Date", width=150)

        self.tree.heading("#0")
        self.tree.heading("Tab", text="Tab")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date", text="Date")

    def get_input_path(self):
        self.paths['input_path'] = filedialog.askdirectory()
        self.input_entry_text.set(self.paths['input_path'])
        self.paths['index_path'] = os.path.join(
            self.paths['input_path'], 'index_template.docx')

    def get_output_path(self):
        self.paths['output_path'] = filedialog.askdirectory()
        self.output_entry_text.set(self.paths['output_path'])

    def get_data(self):
        index = 0
        self.bundle = Bundle(
            self.paths['input_path'], self.paths['index_path'])

        self.tree.delete(*self.tree.get_children())

        for key in self.bundle.get_sections():
            self.tree.insert('', index='end', iid=index,
                             values=(key.section, key.name))
            data = self.bundle.get_entries(key)
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
        tmpdir = self.get_tmpdir()

        if self.bundle != None and self.paths['output_path'] != '':
            self.pb['value'] = 10
            master.update_idletasks()
            self.gen_table(master)
            self.gen_bundle()
            tmpdir.cleanup()
            # os.startfile(self.paths['output_path'])

        else:
            print('No Data!')

    def gen_table(self, master):
        self.bundle.index.input_table_data(self.bundle.data)
        self.bundle.index.input_pag_nums(self.bundle, 1)
        self.bundle.index.save(
            'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test.docx')
        self.bundle.index.convert(
            'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test.pdf')

    def gen_bundle(self):
        # self.bundle.documents.merge_documents(self.paths['documents_pdf_path'])
        self.bundle.documents.merge_documents(
            'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test2.pdf')
        self.bundle.documents.paginate('C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test3.pdf',
                                       'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test4.pdf')
        self.bundle.documents.hyperlink('C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test.pdf',
                                        'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test4.pdf', 'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test5.pdf')

    def update_pb(self, master, v):
        self.pb['value'] = v
        master.update_idletasks()

    def get_tmpdir(self):
        tmpdir = tempfile.TemporaryDirectory()

        self.paths.update({
            'index_pdf_path': join_paths(tmpdir.name, "index.pdf"),
            'index_doc_path': join_paths(tmpdir.name, "index.docx"),
            'documents_pdf_path': join_paths(
                tmpdir.name, "documents.pdf"),
            'bundle_path': join_paths(tmpdir.name, "bundle.pdf"),
            'pag_path': join_paths(tmpdir.name, "pagination.pdf"),
            'output_path': join_paths(
                self.paths['output_path'], self.bundle.name)
        })

        return tmpdir
