import time
import tkinter as tk
from tkinter import ttk
import threading

from autoTK.w_base import WTypes
from autoTK.w_button import WButton
from autoTK.w_label import WLabel


class Placer:
    def __init__(self,root):
        self.root = root
        self.root.bind('<Motion>', self.motion)
        self.root.bind("<ButtonPress-1>", lambda event:  self.capture(True))
        self.root.bind("<ButtonRelease-1>", lambda event:  self.capture(False))
        self.capture(False)
        self.do_capture = False
        self.choosen = None
        self.choosen_name = None
        self.widgets = {}
        self.force_select = False
        self.amounts = 0
        self.memorize_detect = set()
        self.in_motion = False

    def get_widget(self,name):
        wid = self.widgets.get(name,None)
        return wid

    def add_widget(self,type_,name):
        if name in self.widgets:
            name = f"{name}_{self.amounts}"
        if type_.value == WTypes.LABEL.value:
            wid = tk.Label(self.root)
            wid.pack()
            w = WLabel.create_widget(name,
                                      "self.win", wid, self.set_choosen)
        elif type_.value == WTypes.BUTTON.value:
            wid = tk.Button(self.root)
            wid.pack()
            w = WButton.create_widget(name,
                                  "self.win",wid,self.set_choosen)
        w.set_conf(text="sample")
        w.update()

        self.choosen_name = w.name
        self.widgets[w.name] = w
        w.index = self.amounts
        self.amounts += 1

    def set_choosen(self,wid):
        self.force_select = True
        self.choosen = wid.widget
        self.choosen_name = wid.name
        self.memorize_detect.clear()

    def motion(self,event):
        if self.do_capture and self.choosen:
            self.in_motion = True
            x, y = event.x, event.y
            self.choosen.place_configure(x=x, y=y)
            self.detect_horizontal_points()
            self.detect_vertical_points()
        print(threading.activeCount())

    def detect_vertical_points(self):
        canvases = []
        def clear():
            [c_.destroy() for c_ in canvases]
            self.choosen.place_configure(y=w.widget.winfo_y())
            canvases.clear()
        src_ = self.choosen.winfo_y()
        if not self.choosen:
            return
        for name, w in self.widgets.items():
            if len(canvases) > 1:
                break

            if self.choosen_name != name:

                if (src_ == w.widget.winfo_y() or src_ - 1 == w.widget.winfo_y() - 1
                    or src_ + 1 == w.widget.winfo_y() + 1
                )and (self.choosen, w) not in self.memorize_detect:

                    c = tk.Canvas(self.root, width=abs(w.widget.winfo_x() - self.choosen.winfo_x()) + 5, height=0.1)

                    canvases.append(c)
                    print("&" * 500)
                    if w.widget.winfo_x() < self.choosen.winfo_x():
                        c.place(x=w.widget.winfo_x(), y=w.widget.winfo_y())
                    else:
                        c.place(y=src_, x=self.choosen.winfo_x())
                    self.memorize_detect.add((self.choosen, w))
                    threading.Timer(0.5, clear).start()
                    # self.choosen.place_configure(y=w.widget.winfo_y())
                    break

    def detect_horizontal_points(self):

        canvases = []
        def clear():
            [c_.destroy() for c_ in canvases]
            if not self.in_motion:
                self.choosen.place_configure(x=w.widget.winfo_x())

            canvases.clear()
        src_ = self.choosen.winfo_x()
        if not self.choosen:
            return
        for name,w in self.widgets.items():
            if len(canvases) > 1:
                break

            if self.choosen_name != name:

                if (src_ == w.widget.winfo_x() or src_ - 1 == w.widget.winfo_x() - 1
                    or src_ + 1 == w.widget.winfo_x() + 1
                )and (self.choosen, w) not in self.memorize_detect:


                    c = tk.Canvas(self.root,width=0.1,height=abs(w.widget.winfo_y() - self.choosen.winfo_y())+5)

                    canvases.append(c)
                    print("&"*500)
                    if w.widget.winfo_y() < self.choosen.winfo_y():
                        c.place(x=w.widget.winfo_x(),y=w.widget.winfo_y())
                    else:
                        c.place(x=src_, y=self.choosen.winfo_y())
                    self.memorize_detect.add((self.choosen,w))
                    threading.Timer(0.2,clear).start()
                    # self.choosen.place_configure(x=w.widget.winfo_x())
                    break



    def capture(self,flag):
        self.do_capture = flag
        if not flag:
            self.force_select = False

        self.in_motion = False
