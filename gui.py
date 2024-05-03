import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess
import cv2
import os

global current, input_path, output_path, force, skip_amount, video, frame_count, current_frame
input_path = ""
output_path = ""
force = False
skip = 1
current_frame = 1

def move(direction):
    global current
    idx = pages.index(current) + direction
    if 0 <= idx < len(pages):
        current.pack_forget()
        current = pages[idx]
        current.pack(side=tk.TOP)

def next():
    move(+1)

def prev():
    move(-1)

def input_dialog():
    global input_path, image, video, frame_count
    path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4')])
    if path:
        selected_input_label.config(text=f"Selected video file: {path}")
        label_input_error.config(text="")
        video = cv2.VideoCapture(path)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        res, initial_frame = video.read()
        image = cv2.resize(initial_frame, (500,300), interpolation = cv2.INTER_LINEAR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        tk_img = ImageTk.PhotoImage(image=image) 
        image_label.image = tk_img
        image_label.config(image=tk_img)
        frame_count_label.config(text=f"Selected frame: {current_frame}/{frame_count}")
        next_button_p1['state'] = 'active'
        add_skip_buttons()
        input_path = path
        help_msg.destroy()
        spinbox_skip.pack(pady=10)
        spinbox_text.config(text="Choose frequency of frames to skip: ")

def output_dialog():
    global output_path
    path = filedialog.askdirectory()
    if path:
        selected_output_label.config(text=f"Selected Directory: {path}")
        label_output_error.config(text="")
        output_path = path
        if len(os.listdir(path)) == 0:
            empty_dir_label.config(text="Output directory is empty. You can process video without concerns", fg="green")
            process_button['state'] = 'active'
        else:
            empty_dir_label.config(text="""Output directory is NOT empty. 
If you want to process the video you must 
activate force
WARNING: The force option will remove all pre-existing files in the directory 
before the frame extraction""", fg="red")
            force_checkbox.pack()


def apply_force():
    global force
    force = not force

    if current == page2:
        if force:
            process_button['state'] = 'active'
        else:
            process_button['state'] = 'disabled'

def skip_frame(num):
    global current_frame

    cap = cv2.VideoCapture(input_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + num - 1)
    res, frame = cap.read()
    image = cv2.resize(frame, (500,300), interpolation = cv2.INTER_LINEAR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    tk_img = ImageTk.PhotoImage(image=image) 
    image_label.image = tk_img
    image_label.configure(image=tk_img)
    frame_count_label.config(text=f"Selected frame: {current_frame+num}/{frame_count}")
    current_frame += num

def add_skip_buttons(): 
    back5_button = tk.Button(skip_frames_frame, text='<<<<<', 
                            command=lambda: skip_frame(-5))
    back5_button.pack(side=tk.LEFT)
    back3_button = tk.Button(skip_frames_frame, text='<<<', 
                            command=lambda: skip_frame(-3))
    back3_button.pack(side=tk.LEFT)
    back1_button = tk.Button(skip_frames_frame, text='<', 
                            command=lambda: skip_frame(-1))
    back1_button.pack(side=tk.LEFT)
    skip1_button = tk.Button(skip_frames_frame, text='>', 
                            command=lambda: skip_frame(1))
    skip1_button.pack(side=tk.LEFT)
    skip3_button = tk.Button(skip_frames_frame, text='>>>', 
                            command=lambda: skip_frame(3))
    skip3_button.pack(side=tk.LEFT)
    skip5_button = tk.Button(skip_frames_frame, text='>>>>>', 
                            command=lambda: skip_frame(5))
    skip5_button.pack(side=tk.LEFT)

def choose_skip():
    global skip_amount
    skip_amount = spinbox_skip.get()

def frame_extraction():
    exitcode = 1
    if input_path and output_path:
        if force:
            #popen to call function asynchronously
            result = subprocess.Popen(["py", "extract_frame.py", "-i", input_path, 
                                    "-o", output_path, "-f", f"-s {skip}"])
        else:
            result = subprocess.Popen(["py", "extract_frame.py", "-i", input_path, 
                                    "-o", output_path, f"-s {skip}"])
        exitcode = result.returncode
        if not exitcode:
            label_success.config(text="Process Successful", fg="green")
            next_button_p2['state'] = 'active'
        else:
            label_success.config(text="Process Unsuccessful", fg="red")
    else:
        if not input_path:
            label_input_error.config(text="Please provide input path", fg="red")
        if not output_path:
            label_output_error.config(text="Please provide output path", fg="red")

"""
def combine_frames():
    exitcode = 1
    if output_path:
        if force:
            #popen to call function asynchronously
            result = subprocess.Popen(["py", "combine_images.py", "-i", input_path, 
                                    "-o", output_path, "-f"])
        else:
            result = subprocess.Popen(["py", "combine_images.py", "-i", input_path, 
                                    "-o", output_path])
        exitcode = result.returncode
        if not exitcode:
            label_success.config(text="Process Successful", fg="green")
            next_button_p2['state'] = 'active'
        else:
            label_success.config(text="Process Unsuccessful", fg="red")
    else:
        if not input_path:
            label_input_error.config(text="Please provide input path", fg="red")
        if not output_path:
            label_output_error.config(text="Please provide output path", fg="red")

def detect_blob():
    exitcode = 1
    if input_path and output_path:
        if force:
            #popen to call function asynchronously
            result = subprocess.Popen(["py", "extract_frame.py", "-i", input_path, 
                                    "-o", output_path, "-f"])
        else:
            result = subprocess.Popen(["py", "extract_frame.py", "-i", input_path, 
                                    "-o", output_path])
        exitcode = result.returncode
        if not exitcode:
            label_success.config(text="Process Successful", fg="green")
            next_button_p2['state'] = 'active'
        else:
            label_success.config(text="Process Unsuccessful", fg="red")
    else:
        if not input_path:
            label_input_error.config(text="Please provide input path", fg="red")
        if not output_path:
            label_output_error.config(text="Please provide output path", fg="red")
"""

root = tk.Tk()
root.title("App")

# Page 1: Video input (Main frames)
page1 = tk.Frame()
help_msg = tk.Label(page1, text="""Welcome to my Tool. 
                    \n Please select a video to analyse.""")
help_msg.pack()
selected_input_label = tk.Label(page1)
selected_input_label.pack()
label_input_error = tk.Label(page1)
label_input_error.pack()
frame_count_label = tk.Label(page1)
frame_count_label.pack()
skip_frames_frame = tk.Frame(page1)
skip_frames_frame.pack()
image_label = tk.Label(page1)
image_label.pack()
spinbox_text = tk.Label(page1)
spinbox_text.pack()
spinbox_skip = tk.Spinbox(page1, from_= 1, to = 10, width=10, command=choose_skip)

# Page 1 (Buttons) 
buttons_frame = tk.Frame(page1)
back_button_p1 = tk.Button(buttons_frame, text='Previous', command=prev)
back_button_p1['state'] = 'disabled'
back_button_p1.pack(side=tk.LEFT)
next_button_p1 = tk.Button(buttons_frame, text='Next', command=next)
next_button_p1['state'] = 'disabled'
next_button_p1.pack(side=tk.LEFT)
buttons_frame.pack(side=tk.BOTTOM)
page1.pack(side=tk.TOP)

# Page 2: Frame processing (Main frames)
page2 = tk.Frame()
tk.Label(page2, text='Please select an output path').pack()
tk.Button(page2, text="Open Output Directory", command=output_dialog).pack()
selected_output_label = tk.Label(page2)
selected_output_label.pack()
empty_dir_label = tk.Label(page2)
empty_dir_label.pack()
force_checkbox = tk.Checkbutton(page2, text=" Activate force", onvalue=1, offvalue=0, command=apply_force)
label_output_error = tk.Label(page2)
label_output_error.pack()
label_success = tk.Label(page2)
label_success.pack()

# Page 2 (Buttons)
buttons = tk.Frame(page2)
tk.Button(buttons, text='Previous', command=prev).pack(side=tk.LEFT)
process_button = tk.Button(buttons, text='Process', command=frame_extraction)
process_button.pack(side=tk.LEFT)
process_button['state'] = 'disabled'
process_button.pack(side=tk.LEFT)
next_button_p2 = tk.Button(buttons, text='Next', command=next)
next_button_p2['state'] = 'disabled'
next_button_p2.pack(side=tk.LEFT)
buttons.pack(side=tk.BOTTOM)

# Page 3: Display mask (Main frames)
page3 = tk.Frame()
tk.Label(page3, text='Please select an output path').pack()

pages = [page1, page2, page3]
current = page1

# Menubar initialisation
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New File")
filemenu.add_command(label="Open Video File", command=input_dialog)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About")
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

root.geometry("800x500")
root.mainloop()