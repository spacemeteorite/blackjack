import tkinter as tk
from tkinter import ttk
from typing import Protocol



class Presenter(Protocol):
    def handle_click(self, event: tk.Event) -> None:
        ...


class App(tk.Tk):
    def __init__(self):
        super().__init__()


        self.title('dude')


if __name__ == "__main__":
    app = App()
    app.mainloop()