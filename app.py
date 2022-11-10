import tkinter as tk
from tkinter import BOTH, RIGHT, Label, PhotoImage, ttk
from tkinter import filedialog
from bundle import Bundle
import constants as const


class App:
    def __init__(self, master):
        self.decl(master)
        self.styles(master)
        self.layout()
        self.init_tree()

    def decl(self, master):
        """Declare all tkinter variables inside the main application."""

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
        """Position all tkinter variables inside the main application."""

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
        """Style all tkinter variables inside the main application."""

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
        """Initialise the columns and headings inside the tree view object."""

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
        """
        Prompt the user to select a directory containing the bundle files.

        The files in the directory must follow the file management and naming conventions outlined in this project's README.md file.
        """

        self.input_path = filedialog.askdirectory()
        self.input_entry_text.set(self.input_path)
        # self.paths['index_path'] = os.path.join(
        #     self.paths['input_path'], 'index_template.docx')

    def get_output_path(self):
        """Prompt the user to select a directory where the completed bundle will be saved."""

        self.output_path = filedialog.askdirectory()
        self.output_entry_text.set(self.output_path)

    def get_data(self):
        """Initialise the Bundle object and dsplay the data in the tree view object."""

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
            self.gen_index(master)
            self.gen_bundle(master)
            tmpdir.cleanup()
            # os.startfile(self.paths['output_path'])

        else:
            print('No Data!')

    def gen_index(self, master):
        """
        This function inputs the Tab, Document Name, and Date fields into the template word document and then converts the document to pdf in order to determine the number of pages of the index.

        The sequential Page Number field is then input into the word document which is again converted to the final pdf which fill form part of the bundle.
        """

        self.bundle.index.input_table_data(self.bundle.data)
        self.bundle.index.save(
            'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test.docx')
        self.bundle.index.convert(
            'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test.pdf')
        self.update_pb(master, 33)

        self.bundle.index.input_pag_nums(
            self.bundle, self.bundle.index.get_pag_num())
        self.bundle.index.save(
            'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test.docx')
        self.bundle.index.convert(
            'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test.pdf')
        self.update_pb(master, 66)

    def gen_bundle(self, master):
        """
        Generate the bundle.

        This function merges the generated index and the individual documents from the input directory into a single file.

        Page numbering is then added to the document. 

        Hyperlinking is then applied which links the entries in the index to the respective page numbers within the document.
        """

        self.bundle.documents.merge_documents(
            'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test2.pdf')
        self.update_pb(master, 80)
        self.bundle.documents.paginate('C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test3.pdf',
                                       'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test4.pdf')
        self.update_pb(master, 90)
        self.bundle.documents.hyperlink('C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test.pdf',
                                        'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test4.pdf', 'C:/Users/lukel/Desktop/900000/900000/Completed Bundles/test5.pdf')
        self.update_pb(master, 100)

    def update_pb(self, master, v):
        """Set the value of the progress bar and update the gui."""

        self.pb['value'] = v
        master.update_idletasks()
