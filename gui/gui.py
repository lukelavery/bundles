import tkinter as tk
from tkinter import filedialog
from gen import gen

from index.gen_index import gen_index


class Gui:
    def __init__(self, master):

        # frm = ttk.Frame(root, padding=10)
        # frm.grid()
        self.path = ''
        self.entry_text = tk.StringVar()

        self.button = tk.Button(master, text="...",
                                command=self.get_path).grid(column=2, row=0)

        tk.Label(master, text="Tribunal Location").grid(row=1)
        tk.Label(master, text="Case Number").grid(row=2)
        tk.Label(master, text="Claimant").grid(row=3)
        tk.Label(master, text="Respondent").grid(row=4)
        tk.Label(master, text="Bundle Title").grid(row=5)

        self.e0 = tk.Entry(master, width=36, textvariable=self.entry_text)
        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)
        self.e4 = tk.Entry(master)
        self.e5 = tk.Entry(master)

        self.e0.grid(row=0, column=0, columnspan=2)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        self.e4.grid(row=4, column=1)
        self.e5.grid(row=5, column=1)

        tk.Button(master,
                  text='Generate',
                  command=self.get_inputs).grid(row=6,
                                                column=0,
                                                sticky=tk.W,
                                                pady=4)

    def get_path(self):
        self.path = filedialog.askdirectory()
        self.entry_text.set(self.path)

    def get_inputs(self):
        context = {
            'location': self.e1.get(),
            'case_num': self.e2.get(),
            'claimant': self.e3.get(),
            'respondent': self.e4.get(),
            'title': self.e5.get(),
        }
        gen(self.path, context, True, True)
