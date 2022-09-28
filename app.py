from datetime import date
import os
import tempfile
import tkinter as tk
from tkinter import Label, PhotoImage, ttk
from tkinter import filedialog
import constants as const
from directory import get_dir_dict, join_paths
from doc import gen_table
from dt import date_to_ymd
from pdf import add_links, applyPag, generate_docs, get_line_objects, is_entry, pagGen, pdf_merger
from test2 import get_bbox_dict


class App:
    def __init__(self, master):
        self.input_path = ''
        self.output_path = ''
        self.dir_dict = None
        self.index_path = ''
        self.bundle_name = ''

        self.config(master)
        self.styles(master)
        self.layout()
        self.init_tree()

    def config(self, master):
        self.input_entry_text = tk.StringVar()
        self.output_entry_text = tk.StringVar()
        self.style = ttk.Style()
        self.bg_image = PhotoImage(file=const.BG_IMAGE)
        self.bg_label = Label(master, image=self.bg_image)

        self.title_frame = tk.Frame(master)
        self.path_frame = tk.Frame(master)
        self.tree_frame = tk.Frame(master)
        self.button_frame = tk.Frame(master)
        self.pb_frame = tk.Frame(master)

        # title
        self.title_label = tk.Label(self.title_frame, text=const.TITLE_STR)

        # input path
        self.input_label = tk.Label(self.path_frame, text=const.INPUT_STR)
        self.button = ttk.Button(
            self.path_frame, text="...", style='TButton', command=self.get_input_path)
        self.e0 = ttk.Entry(self.path_frame, width=36,
                            textvariable=self.input_entry_text)

        # output path
        self.output_label = tk.Label(
            self.path_frame, text=const.OUTPUT_STR)
        self.button2 = ttk.Button(
            self.path_frame, text="...", style='TButton', command=self.get_output_path)
        self.e1 = ttk.Entry(self.path_frame, width=36,
                            textvariable=self.output_entry_text)

        # tree view
        self.tree = ttk.Treeview(self.tree_frame)

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

    def start(self):
        self.pb.start(20)

    def layout(self):
        self.bg_label.place(relx=1.0, rely=0.0, anchor='ne')

        self.title_label.pack()
        self.title_frame.pack(pady=(25, 20))

        self.input_label.grid(column=0, row=0, columnspan=2)
        self.button.grid(column=1, row=1)
        self.e0.grid(column=0, row=1)

        self.path_frame.pack(pady=10)

        self.output_label.grid(
            column=0, row=2, columnspan=2, pady=(10, 0))
        self.button2.grid(column=1, row=3)
        self.e1.grid(column=0, row=3)

        self.tree.pack(pady=(10, 10))
        self.tree_frame.pack(pady=20)

        self.button_frame.pack()
        self.btn1.grid(column=0, row=0, padx=(0, 20))
        self.btn2.grid(column=1, row=0, padx=(20, 0))

        self.pb.pack()
        self.pb_frame.pack(pady=20)

    def styles(self, master):
        self.style.theme_use('vista')

        self.style.configure('TButton', background=const.BG_COLOR)

        # master.configure(background=const.BG_COLOR)
        master.configure(bg=const.BG_COLOR)
        self.bg_label.configure(bg=const.BG_COLOR)

        self.title_frame.configure(bg=const.BG_COLOR)
        self.path_frame.configure(bg=const.BG_COLOR)
        self.tree_frame.configure(bg=const.BG_COLOR)
        self.button_frame.configure(bg=const.BG_COLOR)

        self.title_label.configure(
            fg=const.FG_COLOR, bg=const.BG_COLOR, font=const.TITLE_FONT)
        self.input_label.configure(bg=const.BG_COLOR)
        self.output_label.configure(bg=const.BG_COLOR)

        self.btn1.configure(background=const.BUTTON_1_BG_COLOR,
                            foreground=const.FG_COLOR, font=const.H1_FONT, relief='solid', borderwidth=1)
        self.btn2.configure(background=const.FG_COLOR,
                            foreground=const.BUTTON_2_FG_COLOR, font=const.H1_FONT, relief='solid', borderwidth=1)

    def init_tree(self):
        self.tree['columns'] = ("Tab", "Name", "Date")
        self.tree.column("#0", minwidth=25, width=100)
        self.tree.column("Tab", width=50)
        self.tree.column("Name", width=150)
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

        for key in self.dir_dict:
            self.tree.insert('', index='end', iid=index, text=key)

            data = self.dir_dict[key]

            new_index = index + 1

            for i in range(len(data)):
                entry = data[i]
                self.tree.insert(parent=str(index), index='end',
                                 iid=new_index, values=(entry.tab, entry.name, entry.date))
                new_index = new_index + 1

            index = new_index

    def generate(self, master):
        tmpdir = tempfile.TemporaryDirectory()
        index_pdf_path = join_paths(tmpdir.name, "index.pdf")
        index_doc_path = join_paths(tmpdir.name, "index.docx")
        documents_pdf_path = join_paths(tmpdir.name, "documents.pdf")
        bundle_path = join_paths(tmpdir.name, "bundle.pdf")
        pag_path = join_paths(tmpdir.name, "pagination.pdf")
        output_path = join_paths(self.output_path, self.bundle_name)
        if self.dir_dict != None:
            self.doc_names, self.pag_nums = gen_table(self, master,
                                                      self.dir_dict, self.index_path, self.input_path, index_pdf_path, index_doc_path)
            self.gen_bundle(index_pdf_path, documents_pdf_path,
                            bundle_path, pag_path, output_path)

        else:
            print('No Data!')

        print(tmpdir)
        tmpdir.cleanup()
        os.startfile(self.output_path)

    def gen_bundle(self, index_pdf_path, documents_pdf_path, output_path, pag_path, link_path):
        generate_docs(self.input_path, documents_pdf_path)
        self.pb['value'] = 70
        pdf_merger([index_pdf_path, documents_pdf_path], output_path)
        self.pb['value'] = 75
        pagGen(output_path, pag_path)
        self.pb['value'] = 80
        applyPag(output_path, pag_path, output_path)
        self.pb['value'] = 85
        bbox_dict = get_bbox_dict(index_pdf_path)
        line_objects = get_line_objects(bbox_dict)
        new_line_objects = is_entry(
            line_objects, self.doc_names, self.pag_nums)
        add_links(output_path, new_line_objects, link_path)
        self.pb['value'] = 100
