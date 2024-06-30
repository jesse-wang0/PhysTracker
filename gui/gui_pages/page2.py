import tkinter as tk
from tkinter import filedialog
import os, subprocess, sys
from ttkbootstrap.constants import *
import ttkbootstrap as tb

class Page2(tk.Frame):
    def __init__(self, parent, control_btns, vid_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.control_btns = control_btns
        self.vid_manager = vid_manager
        tk.Label(self, text="Stage 2: Video Processing", 
                 font='TkDefaultFont 14 bold').pack()
        self.style = tb.Style()
        self.force_value = tk.BooleanVar(value=False)

        self.extraction_container = tk.Frame(self, highlightthickness=1, 
                                                   highlightbackground="black")
        self.extraction_container.pack(side=tk.TOP, fill=tk.X) 

        #Title Label
        tb.Label(self.extraction_container, 
                 text="1. Frame Extraction").pack(pady=10)
        
        self.select_dir_button = tb.Button(self.extraction_container, 
                                           text="Select Output Directory", 
                                           bootstyle="outline",
                                           command=self.next_step)
        self.select_dir_button.pack(pady=(0,10))
        
    def next_step(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path = path
            self.directory_label = tk.Label(self.extraction_container, 
                     text=f"Selected Directory: {path}")
            self.directory_label.pack(side=tk.TOP)

            self.process_button = tb.Button(self.extraction_container, 
                                        text='Process', bootstyle="outline",
                                        command=self.extract_and_threshold)
            self.process_button['state'] = 'disabled'
            self.process_button.pack(side=tk.TOP, pady=10)

            self.setup_progress_bar()

            self.warning_msg = tk.Label(self.extraction_container)
            if len(os.listdir(path)) == 0:
                self.process_button['state'] = 'active'
                self.warning_msg.config(text="Output directory is empty. You can process video without concerns", fg="green")
            else:
                self.warning_msg.config(text=("Output directory is NOT empty. "
                                             "If you want to process the video you must activate force"
                                             "\n WARNING: The force option will remove all pre-existing files"
                                             " in the directory before the frame extraction"
                                            ), fg="red")
                self.force_value = tk.BooleanVar(value=False)
                self.force_checkbox = tk.Checkbutton(self.extraction_container, 
                                                     text=" Activate force", 
                                                     onvalue=1, offvalue=0, 
                                                     variable=self.force_value, 
                                                     command=self.apply_force)
                self.force_checkbox.pack(before=self.process_button)
            self.warning_msg.pack(after=self.directory_label)
            self.output_msg = tk.Label(self.extraction_container)
            self.output_msg.pack()
    
    def setup_progress_bar(self):
        progress_container = tk.Frame(self.extraction_container)
        progress_container.pack(fill=tk.X, pady=10, padx=50)
        tb.Label(progress_container, text="Progress:").pack(side=tk.LEFT)
        self.style.configure('Custom.Horizontal.TProgressbar', 
                             troughcolor='light grey')
        self.progress_bar = tb.Progressbar(progress_container, 
                                      style='Custom.Horizontal.TProgressbar',
                                      bootstyle="success-striped", length=200,
                                      maximum=100, mode="determinate")
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)

    def apply_force(self):
        if self.force_value.get():
            self.process_button['state'] = 'active'
        else:
            self.process_button['state'] = 'disabled'

    def extract_and_threshold(self):
        exitcode_extract = self.frame_extraction()
        threshold, exitcode_threshold = self.get_threshold()
        self.threshold = threshold
        if not exitcode_extract:
            self.output_msg.config(text="Process successful", fg="green")
        else:
            self.output_msg.config(text="Process unsuccessful", fg="red")

    def frame_extraction(self):
        exitcode = 1
        input_path = self.vid_manager.get_vid_path()
        output_path = self.vid_manager.get_output_path()
        force = self.force_value.get()
        skip_num = self.vid_manager.get_skip()
        print(skip_num)

        if input_path and output_path:
            python_executable = sys.executable
            command = [python_executable, "extract_frame.py", "-i", input_path,
                       "-o", output_path, "-s", str(skip_num)]
            if force:
                command.append("-f")
            result = subprocess.Popen(command)
            exitcode = result.returncode
            return exitcode
        elif not output_path:
                self.output_msg.config(text="Output path invalid", fg="red")

    def get_threshold(self):
        python_executable = sys.executable
        img1, dimension1 = self.vid_manager.get_roi(1)
        img2, dimension2 = self.vid_manager.get_roi(2)
        result = subprocess.Popen([python_executable, "thresholding.py", 
                                   "-i", img1, "-j", img2, 
                                   "-x", dimension1, "-y", dimension2])
        return result, result.returncode