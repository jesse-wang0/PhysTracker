from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter as tk
import cv2, os

class VideoProcessor:
    def __init__(self, video_path):
        self.path = video_path
        
        self.video = cv2.VideoCapture(video_path)
        self.total_frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        self.current_frame_count = 0
        if not self.video.isOpened():
            raise ValueError("Error opening video file")

    def get_current_frame_count(self):
        return self.current_frame_count
    
    def get_total_frame_count(self):
        return self.total_frame_count
    
    def get_current_image(self):
        return self.current_image
    
    def get_next_frame(self, num):
        new_frame = self.current_frame_count + num
        if new_frame < 0:
            new_frame = 0
        elif new_frame > self.total_frame_count:
            new_frame = self.total_frame_count

        cap = cv2.VideoCapture(self.path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        res, frame = cap.read()
        if res:
            self.current_image = frame
            #keep reference to avoid garbage collection
            self.frame_image = self.render_image(frame)
            self.current_frame_count = new_frame
            return self.frame_image

    def render_image(self, image):
        image = cv2.resize(image, (500,300), interpolation = cv2.INTER_LINEAR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image=image) 
    
class BottomButtons(tk.Frame):
    def __init__(self, parent, prev, next):
        super().__init__(parent)
        self.parent = parent

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
            self.parent.set_selected_path(path)

class MainApplication(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.menubar = MenuBar(self)
        self.buttons = BottomButtons(self, self.prev, self.next)

        self.page1 = Page1(self)
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

    def set_selected_path(self, path):
        self.page1.setup_page(path)
        self.buttons.on_next()

    def frame_extraction(self):
        exitcode = 1
        if input_path and output_path:
            if force:
                #popen to call function asynchronously
                result = subprocess.Popen(["py", "extract_frame.py", 
                                            "-i", input_path, "-o", output_path, 
                                            "-f", f"-s {skip}"])
            else:
                result = subprocess.Popen(["py", "extract_frame.py", 
                                            "-i", input_path, "-o", output_path,
                                            f"-s {skip}"])
            exitcode = result.returncode
            if not exitcode:
                self.page2.handle_success()
            else:
                self.page2.handle_fail()
        elif not output_path:
                self.page2.handle_empty_output_path()

class Page1(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.help_msg = tk.Label(self, text="""Welcome to my Tool. 
                                    \n Please select a video to analyse.""")
        self.help_msg.pack()
        self.content_container = tk.Frame(self, highlightbackground="black", 
                                            highlightthickness=1)

    def setup_page(self, path):
        self.vid_manager = VideoProcessor(path)
        self.setup_video_preview()
        self.setup_spinbox()
        self.setup_skip_buttons()
        self.help_msg.config(text="""Stage 1: Setup
                            \n Choose a suitable amount of frames to skip
                            \n Choose two clear frames to select the object of interest
                            """)
        self.roi_button = tk.Button(self.content_container, text="Select ROI", 
                                    command=self.select_roi)
        self.roi_button.pack(side=tk.TOP, anchor="n", pady=10)
        self.content_container.pack(fill=tk.BOTH)

    def setup_video_preview(self):
        self.image_container = tk.Frame(self.content_container, 
                                        highlightbackground="black", 
                                        highlightthickness=1)
        self.image_label = tk.Label(self.image_container)
        self.image_label.config(image=self.vid_manager.get_next_frame(0))
        self.image_label.pack()
        self.frame_count_label = tk.Label(self.image_container, text=f"Selected frame: {self.vid_manager.get_current_frame_count()} / {self.vid_manager.get_total_frame_count()}")
        self.frame_count_label.pack(side=tk.TOP)
        self.image_container.pack(anchor="nw", side=tk.LEFT)

    def setup_spinbox(self):
        self.spinbox_container = tk.Frame(self.content_container, 
                                        highlightbackground="black", 
                                        highlightthickness=1)
        self.spinbox_text = tk.Label(self.spinbox_container)
        self.spinbox_text.config(text="Choose frequency of frames to skip: ")
        self.spinbox_text.pack()
        self.spinbox_skip = tk.Spinbox(self.spinbox_container, from_= 1, 
                                        to = 10, width=10)
        self.spinbox_skip.pack(pady=10)
        self.spinbox_container.pack(fill=tk.BOTH, side=tk.TOP,
                                    anchor="n", pady=(0,10))

    def get_skip(self):
        return self.spinbox_skip.get()

    def setup_skip_buttons(self):
        skip_frames_frame = tk.Frame(self.image_container)
        skip_frames_frame.pack(before=self.frame_count_label, fill=tk.X)
        self.back5_button = tk.Button(skip_frames_frame, text='<<<<<', 
                                command=lambda: self.skip_frame(-5))
        self.back5_button.pack(side=tk.LEFT, anchor="w")
        self.back3_button = tk.Button(skip_frames_frame, text='<<<', 
                                command=lambda: self.skip_frame(-3))
        self.back3_button.pack(side=tk.LEFT, anchor="w")
        self.back1_button = tk.Button(skip_frames_frame, text='<', 
                                command=lambda: self.skip_frame(-1))
        self.back1_button.pack(side=tk.LEFT, anchor="w")

        self.skip5_button = tk.Button(skip_frames_frame, text='>>>>>', 
                                command=lambda: self.skip_frame(5))
        self.skip5_button.pack(side=tk.RIGHT, anchor="e")
        self.skip3_button = tk.Button(skip_frames_frame, text='>>>', 
                                command=lambda: self.skip_frame(3))
        self.skip3_button.pack(side=tk.RIGHT, anchor="e")
        self.skip1_button = tk.Button(skip_frames_frame, text='>', 
                                command=lambda: self.skip_frame(1))
        self.skip1_button.pack(side=tk.RIGHT, anchor="e")
    
    def skip_frame(self, num):
        self.image_label.config(image=self.vid_manager.get_next_frame(num))
        self.frame_count_label.config(text=f"Selected frame: {self.vid_manager.get_current_frame_count()} / {self.vid_manager.get_total_frame_count()}")

    def select_roi(self):
        img = self.vid_manager.get_current_image()
        x, y , w, h = cv2.selectROI(img)
        cv2.destroyAllWindows()
        rect = (x, y , w, h)

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

    def output_dialog(self):
        path = filedialog.askdirectory()
        if path:
            print(path)
            self.output_path = path
            self.output_label.config(text=f"Selected Directory: {path}")
            self.output_label.pack(side=tk.TOP)
            if len(os.listdir(path)) == 0:
                self.process_button['state'] = 'active'
                self.output_msg.config(text="Output directory is empty. You can process video without concerns", fg="green")
            else:
                self.output_msg.config(text="""Output directory is NOT empty. 
                    If you want to process the video you must activate force
                    WARNING: The force option will remove all pre-existing files 
                    in the directory before the frame extraction""", fg="red")
            self.output_msg.pack(side=tk.TOP)

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