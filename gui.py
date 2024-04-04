import tkinter as tk
from tkinter import filedialog

global input_path
global output_path
input_path = ""
output_path = ""

def input_dialog():
    global input_path
    path = filedialog.askopenfilename()
    selected_input_label.config(text=f"Selected File: {path}")
    if path:
        label_input_error.config(text="")
        input_path = path

def output_dialog():
    global output_path
    path = filedialog.askdirectory()
    selected_output_label.config(text=f"Selected Directory: {path}")
    if path:
        label_output_error.config(text="")
        output_path = path

def process_file():
    if input_path and output_path:
        print("nice")
    else:
        if not input_path:
            label_input_error.config(text="Please provide input path", fg="red")
        if not output_path:
            label_output_error.config(text="Please provide output path", fg="red")            

root = tk.Tk()
root.title("app test")

label = tk.Label(text="Image Analysis")
label.pack()

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
start_button = tk.Button(frame_process, text="Start Processing", command=process_file)
start_button.pack(padx=20, pady=(20,0))
label_input_error = tk.Label(frame_process)
label_input_error.pack()
label_output_error = tk.Label(frame_process)
label_output_error.pack()

frame_input.pack()
frame_output.pack()
frame_process.pack()

root.geometry("400x300")

root.mainloop()