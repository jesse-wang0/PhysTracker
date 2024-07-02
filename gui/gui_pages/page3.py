import tkinter as tk
from tkinter import filedialog
import os, subprocess, sys, cv2
from ttkbootstrap.constants import *
import ttkbootstrap as tb

class Page3(tk.Frame):
    def __init__(self, parent, control_btns, vid_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.control_btns = control_btns
        self.vid_manager = vid_manager
        tk.Label(self, text="Stage 2: Video Processing", 
                 font='TkDefaultFont 14 bold').pack()
        self.style = tb.Style()
        self.mask_container = tk.Frame(self, highlightthickness=1, 
                                                   highlightbackground="black")
        self.mask_container.pack(side=tk.TOP, fill=tk.X) 

        #Title Label
        tb.Label(self.mask_container, 
                 text="2. Mask Processing").pack(pady=10)
        
        self.process_button = tb.Button(self.mask_container, 
                                        text='Process', bootstyle="outline",
                                        command=self.combine_frames)
        self.process_button['state'] = 'active'
        self.process_button.pack(side=tk.TOP, pady=10)
        self.setup_progress_bar()

        os.mkdir(f"{self.vid_manager.get_output_path()}{os.sep}mask")

        self.output_msg = tk.Label(self.mask_container)
        self.output_msg.pack()
    
    def setup_progress_bar(self):
        progress_container = tk.Frame(self.mask_container)
        progress_container.pack(fill=tk.X, pady=10, padx=50)
        tb.Label(progress_container, text="Progress:").pack(side=tk.LEFT)
        self.style.configure('Custom.Horizontal.TProgressbar', 
                             troughcolor='light grey')
        self.progress_bar = tb.Progressbar(progress_container, 
                                      style='Custom.Horizontal.TProgressbar',
                                      bootstyle="success-striped", length=200,
                                      maximum=100, mode="determinate")
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)

    def combine_frames(self):
        input_path = self.vid_manager.get_output_path()
        output_path = f"{input_path}{os.sep}mask"
        threshold = self.vid_manager.get_threshold()

        if input_path and output_path:
            python_executable = sys.executable
            command = [python_executable, "combine_images.py", "-i", input_path,
                       "-o", output_path, "-t", str(threshold)]
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE)
            self.after(500, self.check_process)

    def check_process(self):
        if self.process.poll() is None:
            stdout_line = self.process.stdout.readline().decode().strip()
            if stdout_line.startswith("Processing"):
                progress = stdout_line.split(" ")[1].split("/")
                self.progress_bar['value'] = int(progress[0])/int(progress[1]) * 100
            # Process has not completed yet, check again after 100ms
            self.after(500, self.check_process)
        else:
            exitcode = self.process.returncode
            if exitcode == 0:
                self.output_msg.config(text="Process successful", fg="green")
                self.progress_bar['value'] = 100
                self.control_btns.on_next()
                
            else:
                self.output_msg.config(text="Process unsuccessful", fg="red")
                stdout, stderr = self.process.communicate()
                print(stderr.decode())