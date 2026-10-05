from tkinter import Tk


class Window(Tk):
    def __init__(self, name, w, h):
        super().__init__()
        self.title(name)
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{w}x{h}+{int((ws-w)/2)}+{int((hs-h)/2)}')
        self.resizable(False, False)
