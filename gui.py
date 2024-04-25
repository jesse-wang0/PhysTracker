import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess
import cv2
import os

global input_path, output_path, force, skip
input_path = ""
output_path = ""
force = False
skip = 1

def input_dialog():
    global input_path, image
    path = filedialog.askopenfilename()
    if path:
        selected_input_label.config(text=f"Selected File: {path}")
        label_input_error.config(text="")
        vidcap = cv2.VideoCapture(path)
        success, image = vidcap.read()
        if success:
            cv2.imwrite("first_frame.jpg",image)
            image = Image.open("first_frame.jpg")
            image = image.resize((100, 100), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            image_label.config(image=image)
            os.remove("first_frame.jpg")
        input_path = path

def output_dialog():
    global output_path
    path = filedialog.askdirectory()
    if path:
        selected_output_label.config(text=f"Selected Directory: {path}")
        label_output_error.config(text="")
        output_path = path

def apply_force():
    global force
    force = not force
    print(force)

def skip_frame():
    global skip
    skip = spinbox_skip.get()

def process_file():
    exitcode = 1
    if input_path and output_path:
        if force:
            #call function 
            result = subprocess.Popen(["py", "extract_frame.py", "-i", input_path, 
                                    "-o", output_path, "-f"])
        else:
            result = subprocess.Popen(["py", "extract_frame.py", "-i", input_path, 
                                    "-o", output_path])
        exitcode = result.returncode
        if not exitcode:
            label_success.config(text="Process Successful", fg="green")
        else:
            label_success.config(text="Unsuccessful", fg="red")
    else:
        if not input_path:
            label_input_error.config(text="Please provide input path", fg="red")
        if not output_path:
            label_output_error.config(text="Please provide output path", fg="red")            

root = tk.Tk()
root.title("app test")

frame_title = tk.Frame(relief="groove", bg="light gray")
label = tk.Label(frame_title, text="Frame Extraction Tool", font=("Arial", 20), bg="light gray")
label.pack(pady=15)

frame_input = tk.Frame()
input_button = tk.Button(frame_input, text="Open Video File", command=input_dialog)
input_button.pack(padx=20, pady=20)
frame_image = tk.Frame()
selected_input_label = tk.Label(frame_image, text="Selected File:")
selected_input_label.pack(side=tk.LEFT)
image_label = tk.Label(frame_image)
image_label.pack(side=tk.RIGHT)

frame_output = tk.Frame()
output_button = tk.Button(frame_output, text="Open Output Directory", command=output_dialog)
output_button.pack(padx=20, pady=20)
selected_output_label = tk.Label(frame_output, text="Selected Directory:")
selected_output_label.pack()

frame_process = tk.Frame()
test = tk.Frame(frame_process)
label_options = tk.Label(frame_process, text="OPTIONS:", font=("Arial", 12))
label_options.pack(pady=(20,0))
label_force = tk.Label(test, text="Force:")
label_force.pack(side=tk.LEFT)
check_force = tk.Checkbutton(test, command=apply_force)
check_force.pack(side=tk.LEFT)
label_skip = tk.Label(test, text="Skip frame:")
label_skip.pack(padx=(30,0), side=tk.LEFT)
spinbox_skip = tk.Spinbox(test, from_= 1, to = 10, width=10, command=skip_frame) 
spinbox_skip.pack(side=tk.LEFT)
test.pack()

start_button = tk.Button(frame_process, text="Start Processing", command=process_file)
start_button.pack(padx=20, pady=(10,0))
label_success = tk.Label(frame_process)
label_success.pack()
label_input_error = tk.Label(frame_process)
label_input_error.pack()
label_output_error = tk.Label(frame_process)
label_output_error.pack()

frame_title.pack(fill=tk.BOTH, expand=tk.TRUE)
frame_input.pack(fill=tk.BOTH)
frame_image.pack()
frame_output.pack()
frame_process.pack()

root.geometry("600x400")

root.mainloop()