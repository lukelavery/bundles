import tkinter as tk
from app import App

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('700x600')
    root.resizable(False, False)
    app = App(root)
    root.mainloop()
