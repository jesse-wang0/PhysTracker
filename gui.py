import tkinter as tk
from tkinter import filedialog
import subprocess
import shlex

global input_path, output_path, force, skip
input_path = ""
output_path = ""
force = False
skip = 1

def get_subprocess_output(cmd):
    args = shlex.split(cmd)

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return exitcode, out, err

def input_dialog():
    global input_path
    path = filedialog.askopenfilename()
    if path:
        selected_input_label.config(text=f"Selected File: {path}")
        label_input_error.config(text="")
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
            result = subprocess.run(["py", "extract_frame.py", "-i", input_path, 
                                    "-o", output_path, "-f"])
        else:
            result = subprocess.run(["py", "extract_frame.py", "-i", input_path, 
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
label = tk.Label(frame_title, text="Image Analysis Tool", font=("Arial", 20), bg="light gray")
label.pack(pady=15)

frame_input = tk.Frame()
input_button = tk.Button(frame_input, text="Open Video File", command=input_dialog)
input_button.pack(padx=20, pady=20)
selected_input_label = tk.Label(frame_input, text="Selected File:")
selected_input_label.pack()

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
frame_output.pack()
frame_process.pack()

root.geometry("600x400")

root.mainloop()