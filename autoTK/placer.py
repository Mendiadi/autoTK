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


    def get_widget(self,name):
        wid = self.widgets.get(name,None)
        return wid

    def add_widget(self,type_,name):
        if type_.value == WTypes.LABEL.value:
            wid = tk.Label(self.root, text="test")
            wid.pack()
            w = WLabel.create_widget(name,
                                      "self.win", wid, self.set_choosen)
        elif type_.value == WTypes.BUTTON.value:
            wid = tk.Button(self.root,text="test")
            wid.pack()
            w = WButton.create_widget(name,
                                  "self.win",wid,self.set_choosen)

        self.choosen_name = w.name
        self.widgets[w.name] = w
        w.index = self.amounts
        self.amounts += 1

    def set_choosen(self,wid):
        self.force_select = True
        self.choosen = wid.widget
        self.choosen_name = wid.name

    def motion(self,event):
        if self.do_capture and self.choosen:
            x, y = event.x, event.y
            self.choosen.place_configure(x=x, y=y)


    def capture(self,flag):
        self.do_capture = flag
        if not flag:
            self.force_select = False

