import tkinter as tk


from placer import Placer
from builder import Builder
from w_base import WTypes

class GUI:
    def __init__(self,win):
        # master window
        self.win = win
        self.win.geometry("1000x1000")

        # top bar
        self.top_bar = tk.Canvas(self.win, height=100, width=400, bg="lightblue")
        self.top_bar.pack()

        # actual rendering window
        self.second_win = tk.Frame(self.win,height=700,width=700,bg="grey")
        self.second_win.pack(pady=50)
        self.second_win.pack_propagate(False)
        self.placer = Placer(self.second_win)

        # tools
        self.builder = Builder("my_window")


        self.btn = tk.Button(self.top_bar, text="add",
                             command=lambda: self.placer.add_widget(WTypes.BUTTON))
        self.btn.place(y=0, x=0)
        tk.Button(self.top_bar, text="add l",
                  command=lambda: self.placer.add_widget(WTypes.LABEL)).place(x=0, y=30)
        tk.Button(self.top_bar, text="save",
                  command=self.save).place(x=50, y=30)


    def save(self):
        self.builder.build(*self.placer.widgets.values())


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()