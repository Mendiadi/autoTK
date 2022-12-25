import copy
import tkinter
from enum import Enum

from typing_extensions import overload

from autoTK.utils.options import Options


class WTypes(Enum):
    CHECKBUTTON = 5
    OVAL = 4
    CANVAS = 3
    ENTRY = 2
    BUTTON = 1
    LABEL = 0


class WBase:
    def __init__(self, name, parent):
        self.conf = None
        self.name = name
        self.widget = None
        self.parent = parent
        self.supported = None
        self.index = 0

    def init(self): ...

    def update_widget_option(self,value,supported):
        ...


    def update(self):
        if self.conf._args_supported(self.conf.options):
            print(self.conf.options)

            self.widget.config(**self.conf.options)

    def set_conf(self, **options):

        if not self.conf:
            self.conf = Options(self.supported, **options)
        else:

            self.conf.options.update(**options)

    def generate_code_for_widget(self):
        ...





    @classmethod
    def create_widget(cls, name, parent, func):
        instance = cls(name, parent)
        instance.init()
        instance.widget.bind("<Button-1>", lambda x: func(instance))
        return instance

    def get_place(self):
        return f"self.{self.name}.place(x= {self.widget.winfo_x()}, y= {self.widget.winfo_y()})"
