import os
import sys
from multiprocessing import Process, Queue
from queue import Empty
import tkinter as tk
import cv2
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from pathlib import Path

current_directory = os.path.dirname(sys.path[0])
if current_directory not in sys.path:
    sys.path.append(current_directory)

from combine_images_cli.combine_images import combine_images

class Page3(tk.Frame):
    def __init__(self, parent, control_btns, vid_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.control_btns = control_btns
        self.vid_manager = vid_manager
        self.combine_process_flag = False
        self.combine_error_flag = False
        self.queue = Queue()
        
        tk.Label(self, text="Stage 2: Video Processing", 
                 font='TkDefaultFont 14 bold').pack()
        self.style = tb.Style()
        self.mask_container = tk.Frame(self, highlightthickness=1, 
                                       highlightbackground="black")
        self.mask_container.pack(side=tk.TOP, fill=tk.X) 

        #Title Label
        tb.Label(self.mask_container, text="2. Mask Processing").pack(pady=10)
        
        self.process_button = tb.Button(self.mask_container, 
                                        text='Process', bootstyle="outline",
                                        command=self.combine_frames)
        self.process_button['state'] = 'active'
        self.process_button.pack(side=tk.TOP, pady=10)
        self.setup_progress_bar()

        self.output_msg = tk.Label(self.mask_container)
        self.output_msg.pack()
    
    def setup_prereq(self):
        self.output_path = f"{self.vid_manager.get_output_path()}{os.sep}mask"
        if os.path.exists(self.output_path):
            if os.path.isdir(self.output_path):
                with os.scandir(self.output_path) as entries:
                    for entry in entries:
                        if entry.is_file():
                            os.unlink(entry.path)
            elif not os.path.isdir(self.output_path):
                os.mkdir(self.output_path)

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
        self.setup_prereq()

        threshold = self.vid_manager.get_threshold()
        if input_path and self.output_path:
            p1 = Process(target=combine_images, 
                         args=(Path(input_path), Path(self.output_path), 
                               threshold, False, self.queue)
                        )
            p1.start()
            self.process_button['state'] = 'disabled'
            self.process_button.config(text='Processing')
            self.check_combine_status()

    def check_combine_status(self):
        if self.combine_process_flag or self.combine_error_flag:
            return
        try:
            message = self.queue.get(block=False)
        except Empty:
            pass
        else:
            if message.startswith("Progress"):
                progress = message.split(" ")[1].split("/")
                self.progress_bar['value'] = int(progress[0])/int(progress[1]) * 100
            elif message == "Process successful":
                self.output_msg.config(text="Process successful", fg="green")
                self.progress_bar['value'] = 100
                self.control_btns.on_next()
                self.setup_image()
                self.process_button['state'] = 'active'
                self.process_button.config(text='Process')
                self.combine_process_flag = True
                self.combine_error_flag = False
            else:
                self.output_msg.config(text="Process unsuccessful", fg="red")
                self.combine_error_flag = True
                self.combine_process_flag = False
        finally:
            self.after(100, self.check_combine_status)

    def setup_image(self):
        self.img_container = tk.Frame(self, highlightthickness=1, 
                                      highlightbackground="black")
        self.img_container.pack(side=tk.TOP, fill=tk.X)

        self.mask_path = f"{self.output_path}{os.sep}mask.png"
        self.mask_img = self.vid_manager.render_image(cv2.imread(self.mask_path), 1.75)
        self.image_label = tb.Label(self.img_container, image=self.mask_img)
        self.image_label.pack(side=tk.LEFT)
        
        crop_container = tk.Frame(self.img_container)
        crop_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        
        # Centering text and button inside crop_container
        crop_label = tb.Label(crop_container, text="Crop unnecessary parts", anchor="center")
        crop_label.pack(side=tk.TOP, pady=(50, 10))
        
        crop_button = tb.Button(crop_container, text='Crop', bootstyle="outline", command=self.crop_image)
        crop_button.pack(side=tk.TOP)
        
    def crop_image(self):
        raw_img = cv2.imread(self.mask_path)
        x, y, w, h = cv2.selectROI("Crop Mask", raw_img)
        cv2.destroyAllWindows()
        roi_cropped = raw_img[int(y):int(y + h), int(x):int(x + w)]

        self.mask_img = self.vid_manager.render_image(roi_cropped, 1.75)
        self.image_label.config(image=self.mask_img)
        self.vid_manager.set_region((x,y,w,h))

    def can_next(self):
        if self.combine_process_flag:
            return True
        return False