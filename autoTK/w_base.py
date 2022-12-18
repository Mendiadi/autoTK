from enum import Enum

from autoTK.options import Options


class WTypes(Enum):
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
        self.parent = parent.name
        self.supported = None

    def update(self):

        if self.conf._args_supported(self.conf.options):
            self.widget.config(**self.conf.options)


    def set_conf(self, **options):

        self.conf = Options(self.supported,**options)

    def generate_code_for_widget(self):
        ...

    @classmethod
    def create_widget(cls, name, parent, func):
        instance = cls(name, parent)
        instance.widget.bind("<Button-1>", lambda x: func(instance))
        return instance

    def get_place(self):
        return f"self.{self.name}.place(x= {self.widget.winfo_x()}, y= {self.widget.winfo_y()})"
