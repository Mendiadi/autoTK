
import tkinter as tk

class ScrolledWin:
    def __init__(self ,win ,h ,w):
        self.win = win
        self.main_frame = tk.Frame(win ,bg="red")
        self.my_canvas = None
        self.h =h
        self.w = w
        self.my_scrollbar = None

    def update_win(self, e):
        self.win.update()
        try:
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        except tk.TclError as e:
            print(e)

    def hook(self):

        self.main_frame.pack(expand=1, fill=tk.BOTH)
        # canvas
        self.my_canvas = tk.Canvas(self.main_frame)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # scrollbar
        self.my_scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure the canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.update_win(e))

        self.second_frame = tk.Frame(self.my_canvas)

        self.my_canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        return self.second_frame
