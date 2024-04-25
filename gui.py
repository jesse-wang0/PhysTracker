import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess
import cv2
import os

global current, input_path, output_path, force, skip
input_path = ""
output_path = ""
force = False
skip = 1

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
    global input_path, image
    path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4')])
    if path:
        selected_input_label.config(text=f"Selected video file: {path}")
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
            help_msg.destroy()
            next_button_p1['state'] = 'active'
        input_path = path

def output_dialog():
    global output_path
    path = filedialog.askdirectory()
    if path:
        selected_output_label.config(text=f"Selected Directory: {path}")
        label_output_error.config(text="")
        output_path = path
        process_button['state'] = 'active'
"""
def apply_force():
    global force
    force = not force
    print(force)

def skip_frame():
    global skip
    skip = spinbox_skip.get()
"""
def process_file():
    exitcode = 1
    if input_path and output_path:
        if force:
            #call function asynchronously
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
            label_success.config(text="Unsuccessful", fg="red")
    else:
        if not input_path:
            label_input_error.config(text="Please provide input path", fg="red")
        if not output_path:
            label_output_error.config(text="Please provide output path", fg="red")            

root = tk.Tk()
root.title("App")

page1 = tk.Frame()
help_msg = tk.Label(page1, text="Welcome to my Tool. \n Please select a video to analyse.")
help_msg.pack()
selected_input_label = tk.Label(page1)
selected_input_label.pack()
label_input_error = tk.Label(page1)
label_input_error.pack()
image_label = tk.Label(page1)
image_label.pack()

buttons = tk.Frame(page1)
back_button_p1 = tk.Button(buttons, text='Previous', command=prev)
back_button_p1['state'] = 'disabled'
back_button_p1.pack(side=tk.LEFT)
next_button_p1 = tk.Button(buttons, text='Next', command=next)
next_button_p1['state'] = 'disabled'
next_button_p1.pack(side=tk.LEFT)
buttons.pack(side=tk.BOTTOM)
page1.pack(side=tk.TOP)


page2 = tk.Frame()
tk.Label(page2, text='Please select an output path').pack()
tk.Button(page2, text="Open Output Directory", command=output_dialog).pack()
selected_output_label = tk.Label(page2)
selected_output_label.pack()
label_output_error = tk.Label(page2)
label_output_error.pack()
label_success = tk.Label(page2)
label_success.pack()

buttons = tk.Frame(page2)
tk.Button(buttons, text='Previous', command=prev).pack(side=tk.LEFT)
process_button = tk.Button(buttons, text='Process', command=process_file)
process_button.pack(side=tk.LEFT)
process_button['state'] = 'disabled'
process_button.pack(side=tk.LEFT)
next_button_p2 = tk.Button(buttons, text='Next', command=next)
next_button_p2['state'] = 'disabled'
next_button_p2.pack(side=tk.LEFT)
buttons.pack(side=tk.BOTTOM)


page3 = tk.Frame()
tk.Label(page3, text='').pack()


pages = [page1, page2, page3]
current = page1

#Menubar initialisation
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

root.geometry("600x400")
root.mainloop()

"""
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
"""