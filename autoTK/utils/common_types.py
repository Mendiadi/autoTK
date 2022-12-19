
class Parent:
    def __init__(self, p, n):
        self.parent = p
        self.name = n

class Screen:
    def __init__(self, win, gui):
        self.win = win
        self.gui = gui

    def destroy(self):
        for child in self.win.winfo_children():
            child.destroy()