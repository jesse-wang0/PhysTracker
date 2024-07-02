import tkinter as tk
from tkinter import filedialog
import os, subprocess, sys

#DETECT BLOBS AND GENERATE GRAPHS
class Page4(tk.Frame):
    def __init__(self, parent, control_btns, vid_manager, **kwargs):
        super().__init__(parent, **kwargs)
