'''customized widgets'''
from tkinter import ttk
import tkinter as tk


class LabeledInfo(ttk.Frame):
    def __init__(self, master, label_text: str, textvariable, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.label = ttk.Label(self, text=label_text)
        self.info = ttk.Label(self, textvariable=textvariable)
        self.label.grid(row=0, column=0)
        self.info.grid(row=0, column=1)
