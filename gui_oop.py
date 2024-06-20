import tkinter as tk
from tkinter import filedialog

class Page1(tk.Frame):
    def __init__(self, parent):
        super().__init__(self, parent)
        self.parent = parent


if __name__ == "__main__":
    root = tk.Tk()
    root.title("App")
    root.geometry("800x500")
    Page1(root).pack(side="top", fill="both", expand=True)
    root.mainloop()