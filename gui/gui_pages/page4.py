import tkinter as tk
import os, subprocess, sys, cv2
from ttkbootstrap.constants import *
import ttkbootstrap as tb

#blob detection and getting path positions
class Page4(tk.Frame):
    def __init__(self, parent, control_btns, vid_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.control_btns = control_btns
        self.vid_manager = vid_manager
        self.process1_flag = False
        self.process2_flag = False
        tk.Label(self, text="Stage 2: Video Processing", 
                 font='TkDefaultFont 14 bold').pack()
        self.style = tb.Style()
        self.mask_container = tk.Frame(self, highlightthickness=1, 
                                       highlightbackground="black")
        self.mask_container.pack(side=tk.TOP, fill=tk.X) 

        #Title Label
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

    def blob_detection(self):
        input_path = self.vid_manager.get_output_path()
        roi = self.vid_manager.get_region()
        input_image = f"{input_path}{os.sep}mask{os.sep}mask.png"
        output_path = f"{input_path}{os.sep}mask"
        if input_image:
            python_executable = sys.executable
            command = [python_executable, "blob_detection.py", 
                       "-i", input_image, "-o", output_path, "-r", str(roi)]
            self.process2 = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE)
            #TODO: ALso handle the errors even tho user cant see

    def get_positions(self):
        input_path = self.vid_manager.get_output_path()
        frame_duration = self.vid_manager.get_frame_duration()
        roi = self.vid_manager.get_region()
        scale = self.vid_manager.get_scale()
        
        if input_path and frame_duration and roi and scale:
            python_executable = sys.executable
            command = [python_executable, "get_positions.py", "-i", input_path,
                       "-d", str(frame_duration), "-r", str(roi), "-m", str(scale)]
            self.process1 = subprocess.Popen(command, stdout=subprocess.DEVNULL, 
                                            stderr=subprocess.PIPE)
            self.after(20, self.check_process)
        self.blob_detection()
        self.vid_manager.set_csv_path(f"{input_path}{os.sep}data{os.sep}position_data.csv")

    def check_process(self):
        if self.process1.poll() is None:
            stderr_line = self.process1.stderr.readline().decode().strip()
            if stderr_line.startswith("Processing"):
                progress = stderr_line.split(" ")[1].split("/")
                self.progress_bar['value'] = int(progress[0])/int(progress[1]) * 100
            # Process has not completed yet, check again after 20ms
            self.after(20, self.check_process)
        else:
            exitcode = self.process1.returncode
            if exitcode == 0:
                self.output_msg.config(text="Process successful", fg="green")
                self.progress_bar['value'] = 100
                self.control_btns.on_next()
                self.process_button['state'] = 'active'
                self.setup_path_img()
                self.process1_flag = True
                self.process2_flag = True
            else:
                self.output_msg.config(text="Process unsuccessful", fg="red")
                stdout, stderr = self.process1.communicate()
                print(stderr.decode())

    def setup_path_img(self):
        path_container = tk.Frame(self)
        path_container.pack(side=tk.LEFT)
        img_path = f"{self.vid_manager.get_output_path()}{os.sep}mask{os.sep}path.png"
        self.path_img = self.vid_manager.render_image(cv2.imread(img_path), 1.75)
        img_label = tk.Label(path_container, image=self.path_img)
        img_label.pack()

    def can_next(self):
        if self.process1_flag and self.process2_flag:
            return True
        return False