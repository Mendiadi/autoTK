import tkinter as tk


from autoTK.providers.provider import Provider
from autoTK.editor.start_screen import StartScreen
from autoTK.editor.editor_tool import RenderEditor


class GUI:
    def __init__(self, win):
        win.geometry("500x500")
        self.temp = None
        self.img = tk.PhotoImage(file="resources/bg.png")
        self.bg_image = tk.Label(win, image=self.img)
        self.bg_image.image = self.img
        self.bg_image.place(x=0, y=0)
        self.screen = StartScreen(win, self)
        win.resizable(False, False)
        self.builder = None

    def add_provider(self, name, size):
        if not name:
            name = "samplePage"
        self.builder = Provider(name, size)

    def move_to_editor(self, h, w):
        self.screen.destroy()
        self.bg_image = tk.Label(self.screen.win, image=self.img)
        self.bg_image.image = self.img
        self.bg_image.place(x=0, y=0)
        if int(h) + 450 < 500:
            h = 500
        if int(w) + 400 < 800:
            w = 800
        self.screen.win.geometry(f"{int(w) + 400}x{int(h) + 450}")
        self.temp = RenderEditor(self.screen.win, self, int(h), int(w))




