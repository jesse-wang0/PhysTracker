import os
import sys
import multiprocessing
from multiprocessing import Process, Queue
from queue import Empty
import tkinter as tk
from tkinter import filedialog
import cv2
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from pathlib import Path

current_directory = os.path.dirname(sys.path[0])
if current_directory not in sys.path:
    sys.path.append(current_directory)

from extract_frame_cli.extract_frame import extract_frame
from thresholding_cli.thresholding import calculate_threshold

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
        tb.Label(self.extraction_container, 
                 text="1. Frame Extraction").pack(pady=10)
        
        self.select_dir_button = tb.Button(self.extraction_container, 
                                           text="Select Output Directory", 
                                           bootstyle="outline",
                                           command=self.next_step)
        self.select_dir_button.pack(pady=(0,10))
    
        self.extraction_process_flag = False
        self.extraction_error_flag = False
        self.threshold_process_flag = False
        self.threshold_error_flag = False
        self.queue = Queue()

    def next_step(self):
        path = filedialog.askdirectory()
        if path:
            self.vid_manager.set_output_path(path)
            self.output_path = path
            self.directory_label = tk.Label(self.extraction_container, 
                     text=f"Selected Directory: {path}")
            self.directory_label.pack(side=tk.TOP)

            self.process_button = tb.Button(self.extraction_container, 
                                        text='Process', bootstyle="outline",
                                        command=self.extract_frames)
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


    def extract_frames(self):
        input_path = self.vid_manager.get_vid_path()
        output_path = self.output_path
        force = self.force_value.get()
        skip_num = self.vid_manager.get_skip()
        
        if input_path and output_path:
            args = [Path(input_path), Path(output_path), skip_num]
            if force:
                args.append(True)
            args.append(self.queue)
            p1 = Process(target=extract_frame, args=tuple(args)) #multiprocessing
            p1.start()
            self.check_extraction_status()

            roi1 = self.vid_manager.get_roi(1)[0]
            result = cv2.imwrite(f"{self.output_path}{os.sep}roi1.png", roi1)
            print(result)
            roi2 = self.vid_manager.get_roi(2)[0]
            cv2.imwrite(f"{self.output_path}{os.sep}roi2.png", roi2)

    def check_extraction_status(self):
        if self.extraction_process_flag:
            self.calculate_threshold()
            return
        elif self.extraction_error_flag:
            return
        try:
            message = self.queue.get(block=False)
        except Empty:
            pass
        else:
            if message.startswith("Progress"):
                progress = message.split(" ")[1].split("/")
                self.progress_bar['value'] = int(progress[0])/int(progress[1]) * 100
            elif message.startswith("frame_delta_t"):
                f_delta_t = float(message.split("=")[1].strip())
                self.vid_manager.set_frame_duration(f_delta_t)
            elif message == "Process successful":
                self.output_msg.config(text="Process successful", fg="green")
                self.progress_bar['value'] = 100
                self.control_btns.on_next()
                self.extraction_process_flag = True
            elif message.startswith("frame_rate"):
                pass
            else:
                self.output_msg.config(text="Process unsuccessful", fg="red")
                self.extraction_error_flag = True
        finally:
            self.after(20, self.check_extraction_status)

    def calculate_threshold(self):
        self.roi1_path = Path(f"{self.output_path}{os.sep}roi1.png")
        self.roi2_path= Path(f"{self.output_path}{os.sep}roi2.png")
        x = self.vid_manager.get_roi(1)[1][0]
        y = self.vid_manager.get_roi(1)[1][1]
        threshold_process = Process(target=calculate_threshold, args=(self.roi1_path, self.roi2_path, x, y)) #multiprocessing
        threshold_process.start()
        self.check_threshold_status()
    
    def check_threshold_status(self):
        if self.threshold_process_flag:
            os.remove(self.roi1_path)
            os.remove(self.roi2_path)
            return
        elif self.threshold_error_flag:
            return
        try:
            message = self.queue.get(block=False)
        except Empty:
            pass
        else:
            if message.startswith("Threshold Amount"):
                threshold = message.split(" ")[1]
                print(threshold)
                self.vid_manager.set_threshold(int(threshold))
                self.threshold_process_flag = True
            else:
                self.output_msg.config(text="Process unsuccessful", fg="red")
                self.error_flag = True
        finally:
            self.after(100, self.check_threshold_status)

    def can_next(self):
        if self.vid_manager.get_output_path() and self.extraction_process_flag \
            and self.threshold_process_flag:
            return True
        return False