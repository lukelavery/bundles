import tkinter as tk
from tkinter import Label, PhotoImage, ttk
from tkinter import filedialog
from turtle import begin_fill
from webbrowser import BackgroundBrowser

from dir.directory import get_dir_dict


class App:
    def __init__(self, master):
        self.path = ''
        self.entry_text = tk.StringVar()

        self.bg_color = '#edeff2'
        master.configure(background=self.bg_color)

        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.style.configure('TButton', background=self.bg_color)
        # self.style.map('TButton', background=[
        #                ('active', 'red')], foreground=[('active', 'red')])

        self.bg = PhotoImage(file='image52.png')
        self.bg_label = Label(master, image=self.bg)
        self.bg_label.place(relx=1.0,
                            rely=0.0,
                            anchor='ne')

        # title
        self.title = tk.Frame(master)
        self.title_label = tk.Label(self.title, text="AG BUNDLE TOOL", font=(
            "Arial", 18, "bold"), fg='#405569', bg=self.bg_color)
        self.title_label.pack()
        self.title.pack(pady=10)

        # input path
        self.path_frame = tk.Frame(master, bg=self.bg_color)
        self.input_path_label = tk.Label(self.path_frame, text='Please select the directory containing your bundle files.', bg=self.bg_color).grid(
            column=0, row=0, columnspan=2)
        self.button = ttk.Button(
            self.path_frame, text="...", style='TButton', command=self.get_path).grid(column=1, row=1)
        self.e0 = ttk.Entry(self.path_frame, width=36, textvariable=self.entry_text).grid(
            column=0, row=1)

        # output path
        self.output_path_label = tk.Label(self.path_frame, text='Please select the directory to save your completed bundle.', bg=self.bg_color).grid(
            column=0, row=2, columnspan=2, pady=(10, 0))
        self.button = ttk.Button(
            self.path_frame, text="...", style='TButton').grid(column=1, row=3)
        self.e0 = ttk.Entry(self.path_frame, width=36, textvariable='').grid(
            column=0, row=3)
        self.path_frame.pack(pady=5)

        # tree view
        self.tree_frame = tk.Frame(master)
        self.tree = ttk.Treeview(self.tree_frame)

        self.tree['columns'] = ("Tab", "Name", "Date")
        self.tree.column("#0", minwidth=25, width=100)
        self.tree.column("Tab", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Date", width=100)

        self.tree.heading("#0", text="Section")
        self.tree.heading("Tab", text="Tab")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date", text="Date")

        self.tree.pack()
        self.tree_frame.pack(pady=20)

        self.pb = ttk.Progressbar(
            master,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
# "raised", "sunken", "flat", "ridge", "solid", "groove"
        # buttons
        self.button_frame = tk.Frame(master, bg=self.bg_color, pady=10)
        # self.get_data_button = ttk.Button(
        #     self.button_frame, text="1. GET DATA", command=self.get_data, style='TButton').grid(column=0, row=0, padx=(0, 20))
        # self.generate_button = ttk.Button(
        #     self.button_frame, text="2. GENERATE", command=self.pb.start, style='1.TButton').grid(column=1, row=0, padx=(20, 0))
        # self.btn1 = tk.Button(self.button_frame,
        #                       bg='#DCDCDC',
        #                       fg='#405569',
        #                       relief='flat',
        #                       text='hello button',
        #                       font=('Arial', 12, 'bold'),
        #                       width=20).grid(
        #     column=0, row=0, padx=(20, 0))
        self.btn1 = tk.Button(self.button_frame,
                              bg='#DCDCDC',
                              fg='#405569',
                              relief='solid',
                              borderwidth=1,
                              text='1. GET DATA',
                              font=('Arial', 12, 'bold'),
                              width=20,
                              height=2,
                              command=self.get_data).grid(
            column=0, row=0, padx=(0, 20))
        self.btn2 = tk.Button(self.button_frame,
                              bg='#405569',
                              fg='white',
                              relief='solid',
                              borderwidth=1,
                              text='2. GENERATE BUNDLE',
                              font=('Arial', 12, 'bold'),
                              width=20,
                              height=2).grid(column=1, row=0, padx=(20, 0))
        self.button_frame.pack()

        self.pb.pack(pady=20)

    def decl(self):

    def styles(self):

    def layout(self):

    def get_path(self):
        self.path = filedialog.askdirectory()
        self.entry_text.set(self.path)
        print(self.path)

    def get_data(self):
        index = 0
        dir_dict = get_dir_dict(self.path)

        for key in dir_dict:
            self.tree.insert('', index='end', iid=index, text=key)

            data = dir_dict[key]

            new_index = index + 1

            for i in range(len(data)):
                (tab, date, name) = data[i]
                self.tree.insert(parent=str(index), index='end',
                                 iid=new_index, values=(tab, name, date))
                new_index = new_index + 1

            index = new_index

    def generate(self):


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('700x600')
    root.resizable(False, False)
    app = App(root)
    root.mainloop()
