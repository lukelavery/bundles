import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import src.views.constants as const
from src.controller.controller import Controller


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.create_widgets(parent)
        self.style_widgets(parent)
        self.layout_widgets()

        self.controller = None

    def create_widgets(self, parent):
        """Declare all tkinter variables inside the main application."""
        
        self.input_entry_text = tk.StringVar()
        self.output_entry_text = tk.StringVar()
        self.style = ttk.Style()

        # background
        self.bg_image = tk.PhotoImage(file=const.BG_IMAGE)
        self.bg_label = tk.Label(parent, image=self.bg_image)

        # frames
        self.title_frame = tk.Frame(parent)
        self.path_frame = tk.Frame(parent)
        self.tree_frame = tk.Frame(parent)
        self.button_frame = tk.Frame(parent)
        self.progress_bar_frame = tk.Frame(parent)

        # title
        self.title_label = tk.Label(self.title_frame, text=const.TITLE_STR)

        # paths
        self.input_label = tk.Label(self.path_frame, text=const.INPUT_STR)
        self.input_button = ttk.Button(
            self.path_frame, text="...",
            style='TButton',
            command=self.input_entry_button_clicked
        )
        self.input_entry = ttk.Entry(self.path_frame, width=36,
                                     textvariable=self.input_entry_text)
        self.input_error_message_label = ttk.Label(
            self.path_frame, text='', foreground='red')

        self.output_label = tk.Label(
            self.path_frame, text=const.OUTPUT_STR)
        self.output_button = ttk.Button(
            self.path_frame,
            text="...",
            style='TButton',
            command=self.output_entry_button_clicked
        )
        self.output_entry = ttk.Entry(self.path_frame, width=36,
                                      textvariable=self.output_entry_text)
        self.output_error_message_label = ttk.Label(
            self.path_frame, text='')

        # tree view
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.init_tree()

        # buttons
        self.btn1 = tk.Button(self.button_frame,
                              text=const.DATA_BTN_STR,
                              width=20,
                              height=2,
                              command=self.get_data_button_clicked
                              )
        self.btn2 = tk.Button(self.button_frame,
                              text=const.GEN_BTN_STR,
                              width=20,
                              height=2,
                              command=self.generate_button_clicked,
                              )

        # progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_bar_frame,
            orient='horizontal',
            mode='determinate',
            length=280
        )

    def style_widgets(self, parent):
        """Style all tkinter variables inside the main application."""
        
        self.style.theme_use('vista')

        # background
        parent.configure(bg=const.BG_COLOR)
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
        self.input_error_message_label.configure(foreground='red')
        self.output_label.configure(bg=const.BG_COLOR)
        self.output_error_message_label.configure(foreground='red')

        # tree view
        self.tree_scroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # buttons
        self.btn1.configure(background=const.BUTTON_1_BG_COLOR, foreground=const.FG_COLOR,
                            font=const.H1_FONT, relief='solid', borderwidth=1)
        self.btn2.configure(background=const.FG_COLOR, foreground=const.BUTTON_2_FG_COLOR,
                            font=const.H1_FONT, relief='solid', borderwidth=1)

    def layout_widgets(self):
        """Position all tkinter variables inside the main application."""
        
        # background
        self.bg_label.place(relx=1.0, rely=0.0, anchor='ne')

        # title
        self.title_label.pack()
        self.title_frame.pack(pady=(20, 20))

        # paths
        self.input_label.grid(column=0, row=0, columnspan=2)
        self.input_button.grid(column=1, row=1)
        self.input_entry.grid(column=0, row=1)
        self.input_error_message_label.grid(row=2, column=0, sticky=tk.W)

        self.output_label.grid(
            column=0, row=3, columnspan=2, pady=(10, 0))
        self.output_button.grid(column=1, row=4)
        self.output_entry.grid(column=0, row=4)
        self.output_error_message_label.grid(row=5, column=0, sticky=tk.W)

        self.path_frame.pack(pady=10)

        # tree view
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.tree.pack(padx=(15, 0))
        self.tree_frame.pack(pady=(5, 30))

        # buttons
        self.btn1.grid(column=0, row=0, padx=(0, 20))
        self.btn2.grid(column=1, row=0, padx=(20, 0))
        self.button_frame.pack()

        # progress bar
        self.progress_bar.pack()
        self.progress_bar_frame.pack(pady=(25, 0))

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

    def set_controller(self, controller: Controller):
        """Set the controller"""
        
        self.controller = controller

    def input_entry_button_clicked(self):
        """Handle button click event."""
        
        self.input_entry_text.set(filedialog.askdirectory())
        # if self.controller:
        #     self.controller.set_input_path(self.input_entry_text.get())

    def output_entry_button_clicked(self):
        """Handle button click event."""
        
        self.output_entry_text.set(filedialog.askdirectory())

    def get_data_button_clicked(self):
        if self.controller:
            self.controller.set_input_path(self.input_entry_text.get())

    def generate_button_clicked(self):
        """Handle button click event."""
        
        if self.controller:
            self.controller.set_output_path(self.output_entry_text.get())

    def show_input_error(self, message):
        """Show an error message for the input entry field."""
        
        self.input_error_message_label['text'] = message
        self.input_error_message_label['foreground'] = 'red'
        self.input_error_message_label.after(
            3000, self.hide_input_error_message)

    def show_output_error(self, message):
        """Show an error message for the output entry field."""
        
        self.output_error_message_label['text'] = message
        self.output_error_message_label['foreground'] = 'red'
        self.output_error_message_label.after(
            3000, self.hide_output_error_message)

    def hide_input_error_message(self):
        """Hide error message for the input entry field."""
        
        self.input_error_message_label['text'] = ''

    def hide_output_error_message(self):
        """Hide error message for the output entry field."""
        
        self.output_error_message_label['text'] = ''

    def update_tree_view(self, bundle_data):
        """Update the tree view with the bundle data."""
        
        index = 0
        self.tree.delete(*self.tree.get_children())

        for key in bundle_data:
            self.tree.insert('', index='end', iid=index,
                             values=(key.section, key.name))
            parent_index = index
            index += 1

            for entry in bundle_data[key]:
                self.tree.insert(parent=str(parent_index), index='end',
                                 iid=index, values=(entry.tab, entry.name, entry.date))
                index += 1

        for child in self.tree.get_children():
            self.tree.item(child, open=True)

    def show_error(self, message):
        """Show a general error as a popup."
        
        messagebox.showerror('error', message)

    def update_pb(self, value):
        """Set the value of the progress bar and update the gui."""

        self.progress_bar['value'] = value
        self.parent.update_idletasks()
