import tkinter as tk
from app import App

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('400x400')
    app = App(root)
    root.mainloop()
