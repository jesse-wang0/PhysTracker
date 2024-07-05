import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from tkinter import filedialog

from video_manager import VideoProcessor
from gui_pages.page1 import Page1
from gui_pages.page2 import Page2
from gui_pages.page3 import Page3
from gui_pages.page4 import Page4
from gui_pages.page5 import Page5

class MainApplication(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.update()
        width = parent.winfo_width()
        height = parent.winfo_height()
        self.menubar = MenuBar(self)
        self.buttons = BottomButtons(self, self.prev, self.next)
        self.vid_manager = VideoProcessor((width, height))

        self.page1 = Page1(self, self.buttons, self.vid_manager)
        self.page2 = Page2(self, self.buttons, self.vid_manager)
        self.page3 = Page3(self, self.buttons, self.vid_manager)
        self.page4 = Page4(self, self.buttons, self.vid_manager)
        self.page5 = Page5(self, self.buttons, self.vid_manager)
        self.pages = [self.page1, self.page2, self.page3, 
                      self.page4, self.page5]
        self.current = self.page1

        root.configure(menu=self.menubar)
        self.buttons.pack(side=tk.BOTTOM, anchor='ne')
        self.page1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def move(self, direction):
        index = self.pages.index(self.current) + direction
        if 0 <= index < len(self.pages):
            self.current.pack_forget()
            self.current = self.pages[index]
            self.current.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.buttons.off_next()
            self.buttons.off_back()

        if self.current == self.page1:
            if self.page1.can_next():
                self.buttons.on_next()
        else:
            self.buttons.on_back()
            if self.current.can_next():
                self.buttons.on_next()
            if self.current == self.page5:
                self.page5.add_table_values(self.vid_manager.get_csv_path())
            elif self.current == self.page3:
                 self.page3.setup_prereq()

    def next(self):
        self.move(1)

    def prev(self):
        self.move(-1)

    def setup_page1(self, path):
        self.page1.setup_page(path)

class BottomButtons(tb.Frame):
    def __init__(self, parent, prev, next):
        super().__init__(parent)
        self.next_button = tb.Button(self, text='Next', command=next)
        self.next_button['state'] = 'disabled'
        self.next_button.pack(side=tk.RIGHT, padx=(0, 20), pady=(0, 10))

        self.back_button = tb.Button(self, text='Previous', command=prev)
        self.back_button['state'] = 'disabled'
        self.back_button.pack(side=tk.RIGHT, pady=(0, 10))

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
        self.parent = parent
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="New File")
        self.filemenu.add_command(label="Open Video File", 
                                  command=self.input_dialog)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=parent.quit)
        self.add_cascade(label="File", menu=self.filemenu)

    def input_dialog(self):
        path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4')])
        if path:
            self.parent.setup_page1(path)

if __name__ == "__main__":
    root = tb.Window(themename="litera")
    root.title("App")
    root.geometry("1000x600")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()