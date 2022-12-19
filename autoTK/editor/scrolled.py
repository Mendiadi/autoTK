

import tkinter as tk

class ScrolledWin:
    def __init__(self,win,h,w):

        self.main_frame = tk.Frame(win,height=h,width=w,bg="red")
        self.my_canvas = None
        self.h =h
        self.w = w
        self.my_scrollbar = None


    def update_win(self):

        try:
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        except tk.TclError as e:
            print(e)

    def hook(self):

        self.main_frame.pack()
        # canvas
        self.my_canvas = tk.Canvas(self.main_frame,height=self.h,width=self.w - 10)
        self.my_canvas.pack(side=tk.LEFT)

        # scrollbar
        self.my_scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure the canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.update_win())
        frame = tk.Frame(self.my_canvas,height=self.h,width=self.w-10)
        frame.pack(pady=50)
        return frame
