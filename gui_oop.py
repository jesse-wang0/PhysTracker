import tkinter as tk
import cv2, os, subprocess
from tkinter import filedialog

class BottomButtons(tk.Frame):
    def __init__(self, parent, prev, next):
        super().__init__(parent)
        self.next_button = tk.Button(self, text='Next', command=next)
        self.next_button['state'] = 'disabled'
        self.next_button.pack(side=tk.RIGHT, padx=(0, 20), pady=(0, 10))

        self.back_button = tk.Button(self, text='Previous', command=prev)
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

class MainApplication(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.menubar = MenuBar(self)
        self.buttons = BottomButtons(self, self.prev, self.next)

        self.page1 = Page1(self, self.buttons)
        self.page2 = Page2(self)
        self.page3 = Page3(self)
        self.page4 = Page4(self)
        self.pages = [self.page1, self.page2, self.page3, self.page4]
        self.current = self.page1

        root.configure(menu=self.menubar)
        self.buttons.pack(side=tk.BOTTOM, anchor='ne')
        self.page1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def move(self, direction):
        index = self.pages.index(self.current) + direction
        if 0 <= index < len(self.pages):
            self.current.pack_forget()
            self.current = self.pages[index]
            self.current.pack(side=tk.TOP)
            print(self.current)

    def next(self):
        self.move(1)

    def prev(self):
        self.move(-1)

    def setup_page1(self, path):
        self.page1.setup_page(path)

    def frame_extraction(self):
        exitcode = 1
        input_path = self.page1.get_input_path()
        output_path = self.page2.get_output_path()
        force = self.page2.get_force()
        skip_num = self.page1.get_skip()

        if input_path and output_path:
            if force:
                #popen to call function asynchronously
                result = subprocess.Popen(["py", "extract_frame.py", 
                                            "-i", input_path, "-o", output_path, 
                                            "-f", f"-s {skip_num}"])
            else:
                result = subprocess.Popen(["py", "extract_frame.py", 
                                            "-i", input_path, "-o", output_path,
                                            f"-s {skip_num}"])
            exitcode = result.returncode
            if not exitcode:
                self.page2.handle_success()
            else:
                self.page2.handle_fail()
        elif not output_path:
                self.page2.handle_empty_output_path()

class Page2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        tk.Label(self, text='Please select an output path').pack()
        tk.Button(self, text="Open Output Directory", 
                    command=self.output_dialog).pack()
        self.process_button = tk.Button(self, text='Process', 
                                        command=parent.frame_extraction)
        self.process_button.pack(side=tk.TOP)
        self.process_button['state'] = 'disabled'
        self.output_msg = tk.Label(self)
        self.output_label = tk.Label(self)

    def get_output_path(self):
        return self.output_path
    
    def get_force(self):
        pass #TODO

    def output_dialog(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path = path
            self.output_label.config(text=f"Selected Directory: {path}")
            self.output_label.pack(side=tk.TOP)
            if len(os.listdir(path)) == 0:
                self.process_button['state'] = 'active'
                self.output_msg.config(text="Output directory is empty. You can process video without concerns", fg="green")
            else:
                self.output_msg.config(text=("Output directory is NOT empty."
                                             "If you want to process the video you must activate force"
                                             "WARNING: The force option will remove all pre-existing files"
                                             "in the directory before the frame extraction"
                                            ), fg="red")
            self.output_msg.pack(side=tk.TOP)
            self.force_checkbox = tk.Checkbutton(self, text=" Activate force", onvalue=1, offvalue=0)
            self.force_checkbox.pack()

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