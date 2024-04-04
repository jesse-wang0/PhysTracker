import tkinter as tk
from tkinter import filedialog

def input_dialog():
    global INPUT_PATH
    path = filedialog.askopenfilename()
    selected_input_label.config(text=f"Selected File: {path}")
    INPUT_PATH = path

def output_dialog():
    global OUTPUT_PATH
    path = filedialog.askdirectory()
    selected_output_label.config(text=f"Selected File: {path}")
    OUTPUT_PATH = path

def process_file(file_path): 
    pass

root = tk.Tk()
root.title("app test")

label = tk.Label(text="Image Analysis")
label.pack()

frame_i = tk.Frame()
input_button = tk.Button(frame_i, text="Open Video File", command=input_dialog)
input_button.pack(padx=20, pady=20)
selected_input_label = tk.Label(frame_i, text="Selected File:")
selected_input_label.pack()

frame_o = tk.Frame()
output_button = tk.Button(frame_o, text="Open Output Directory", command=output_dialog)
output_button.pack(padx=20, pady=20)
selected_output_label = tk.Label(frame_o, text="Selected Directory:")
selected_output_label.pack()

start_button = tk.Button(root, text="Start Processing", command=process_file)

frame_i.pack()
frame_o.pack()
start_button.pack(padx=20, pady=40)
root.geometry("400x300")

root.mainloop()