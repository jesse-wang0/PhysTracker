import tkinter as tk
from tkinter import filedialog



class BottomButtons(tk.Frame):
    def __init__(self, parent, prev, next):
        super().__init__(parent)
        self.parent = parent

        self.next_button = tk.Button(self, text='Next', command=next)
        self.next_button['state'] = 'disabled'
        self.next_button.pack(side=tk.RIGHT)

        self.back_button = tk.Button(self, text='Previous', command=prev)
        self.back_button['state'] = 'disabled'
        self.back_button.pack(side=tk.RIGHT)

    def off_next(self):
        self.next_button['state'] = 'disabled'

    def on_next(self):
        self.next_button['state'] = 'active'

    def off_back(self):
        self.back_button['state'] = 'disabled'
        
    def on_back(self):
        self.back_button['state'] = 'active'

class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="New File")
        self.filemenu.add_command(label="Open Video File", command=self.input_dialog)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=parent.quit)
        self.add_cascade(label="File", menu=self.filemenu)

    def input_dialog(self):
        pass

class MainApplication(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.menubar = MenuBar(self)
        self.bottom_buttons = BottomButtons(self, self.prev, self.next)
        self.page1 = Page1(self)
        self.page2 = Page2(self)
        self.page3 = Page3(self)
        self.page4 = Page4(self)
        
        self.pages = [self.page1, self.page2, self.page3, self.page4]
        self.current = self.page1

        self.bottom_buttons.pack(side=tk.BOTTOM)
        root.configure(menu=self.menubar)
    
    def move(self, direction):
        index = self.pages.index(current) + direction
        if 0 <= index < len(self.pages):
            current.pack_forget()
            current = self.pages[index]
            current.pack(self, side=tk.TOP)

    def next(self):
        self.move(1)

    def prev(self):
        self.move(-1)

class Page1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent


class Page2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

class Page3(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

class Page4(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

class Page5(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

if __name__ == "__main__":
    root = tk.Tk()
    root.title("App")
    root.geometry("800x500")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()