import os
import sys
import tkinter as tk
import cv2
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from multiprocessing import Process, Queue
from queue import Empty
from pathlib import Path

current_directory = os.path.dirname(sys.path[0])
if current_directory not in sys.path:
    sys.path.append(current_directory)
from blob_detection_cli.blob_detection import detect_blobs
from get_positions_cli.get_positions import get_positions

#blob detection and getting path positions
class Page4(tk.Frame):
    def __init__(self, parent, control_btns, vid_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.control_btns = control_btns
        self.vid_manager = vid_manager
        self.blob_process_flag = False
        self.blob_error_flag = False
        self.position_process_flag = False
        self.position_error_flag = False
        self.queue = Queue()

        tk.Label(self, text="Stage 2: Video Processing", 
                 font='TkDefaultFont 14 bold').pack()
        self.style = tb.Style()
        self.mask_container = tk.Frame(self, highlightthickness=1, 
                                       highlightbackground="black")
        self.mask_container.pack(side=tk.TOP, fill=tk.X) 
        tb.Label(self.mask_container, text="3. Path Detection").pack(pady=10)
        
        self.process_button = tb.Button(self.mask_container, 
                                        text='Process', bootstyle="outline",
                                        command=self.get_positions)
        self.process_button['state'] = 'active'
        self.process_button.pack(side=tk.TOP, pady=10)
        self.setup_progress_bar()

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

    def get_positions(self):
        input_path = self.vid_manager.get_output_path()
        frame_duration = self.vid_manager.get_frame_duration()
        roi = self.vid_manager.get_region()
        scale = self.vid_manager.get_scale()

        if input_path and frame_duration and roi and scale:
            p1 = Process(target=get_positions, 
                         args=(Path(input_path), frame_duration, roi, scale, 
                               "average.jpg", self.queue)
                        )
            p1.start()
            self.check_position_status()
            self.process_button['state'] = 'disabled'
            self.process_button.config(text='Processing')
            self.vid_manager.set_csv_path(f"{input_path}{os.sep}data{os.sep}position_data.csv")
    
    def check_position_status(self):
        if self.position_process_flag:
            self.blob_detection()
            return
        elif self.position_error_flag:
            return
        try:
            message = self.queue.get(block=False)
        except Empty:
            pass
        else:
            if message.startswith("Progress"):
                progress = message.split(" ")[1].split("/")
                progress_percent = int(progress[0])/int(progress[1]) * 100
                if progress_percent > 95: #Need to wait until thresholding also finishes. Simulate measuring both processes
                    progress_percent = 95
                self.progress_bar['value'] = progress_percent
            elif message == "Process successful":
                self.position_process_flag = True
                self.position_error_flag = False
            else:
                self.output_msg.config(text="Process unsuccessful", fg="red")
                self.position_error_flag = True
                self.position_process_flag = False
        finally:
            self.after(20, self.check_position_status)

    def blob_detection(self):
        input_path = self.vid_manager.get_output_path()
        roi = self.vid_manager.get_region()
        input_image = f"{input_path}{os.sep}mask{os.sep}mask.png"
        output_path = f"{input_path}{os.sep}mask"
        if input_image:
            p2 = Process(target=detect_blobs, 
                         args=(Path(input_image), Path(output_path), 
                               roi, self.queue)
                        )
            p2.start()
            #TODO: ALso handle the errors even tho user cant see
            self.check_blob_status()

    def check_blob_status(self):
        if self.blob_process_flag or self.blob_error_flag:
            return
        try:
            message = self.queue.get(block=False)
        except Empty:
            pass
        else:
            if message == "Process successful":
                self.output_msg.config(text="Process successful", fg="green")
                self.progress_bar['value'] = 100
                self.control_btns.on_next()
                self.process_button['state'] = 'active'
                self.process_button.config(text='Process')
                self.setup_path_img()
                self.blob_process_flag = True
                self.blob_error_flag = False
            else:
                self.output_msg.config(text="Process unsuccessful", fg="red")
                self.blob_error_flag = True
                self.blob_process_flag = False
        finally:
            self.after(100, self.check_blob_status)

    def setup_path_img(self):
        path_container = tk.Frame(self)
        path_container.pack(side=tk.TOP)
        img_path = f"{self.vid_manager.get_output_path()}{os.sep}mask{os.sep}path.png"
        self.path_img = self.vid_manager.render_image(cv2.imread(img_path), 1.75)
        img_label = tk.Label(path_container, image=self.path_img)
        img_label.pack()

    def can_next(self):
        if self.position_process_flag and self.blob_process_flag:
            return True
        return False