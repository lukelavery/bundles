from cgitb import text
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from dir.scraper import scrape_file_names

from test import get_dir_dict


class App:
    def __init__(self, master):
        self.path = ''
        self.entry_text = tk.StringVar()

        # title
        self.title = tk.Frame(master)
        self.title_label = tk.Label(self.title, text="AG BUNDLE TOOL", font=(
            "Arial", 18, "bold"), fg='#405569')
        self.title_label.pack()
        self.title.pack(pady=10)

        # input path
        self.input_path = tk.Frame(master)
        self.input_path_label = tk.Label(self.input_path, text='Please select the directory containing your bundle files.').grid(
            column=0, row=0, columnspan=2)
        self.button = tk.Button(
            self.input_path, text="...", command=self.get_path).grid(column=1, row=1)
        self.e0 = tk.Entry(self.input_path, width=36, textvariable=self.entry_text).grid(
            column=0, row=1)
        self.input_path.pack()

        # output path
        self.output_path = tk.Frame(master)
        self.output_path_label = tk.Label(self.output_path, text='Please select the directory to save your completed bundle.').grid(
            column=0, row=0, columnspan=2)
        self.button = tk.Button(
            self.output_path, text="...").grid(column=1, row=1)
        self.e0 = tk.Entry(self.output_path, width=36, textvariable='').grid(
            column=0, row=1)
        self.output_path.pack()

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
        self.tree_frame.pack()

        self.pb = ttk.Progressbar(
            master,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )

        # buttons
        self.button_frame = tk.Frame(master)
        self.get_data_button = tk.Button(
            self.button_frame, text="1. GET DATA", command=self.get_data).grid(column=0, row=0)
        self.generate_button = tk.Button(
            self.button_frame, text="2. GENERATE", command=self.pb.start).grid(column=1, row=0)
        self.button_frame.pack()

        self.pb.pack()

    def get_path(self):
        self.path = filedialog.askdirectory()
        self.entry_text.set(self.path)
        print(self.path)

    def get_data(self):
        index = 0
        tab = 0
        dir_dict = get_dir_dict(self.path)

        for key in dir_dict:
            self.tree.insert('', index='end', iid=index, text=key)

            data = dir_dict[key]

            new_index = index + 1

            for i in range(len(data)):
                tab = tab + 1
                (date, name) = data[i]
                self.tree.insert(parent=str(index), index='end',
                                 iid=new_index, values=(tab, name, date))
                new_index = new_index + 1

            index = new_index


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('550x550')
    root.resizable(False, False)
    app = App(root)
    root.mainloop()
