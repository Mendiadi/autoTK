from enum import Enum

from autoTK.options import Options


class WTypes(Enum):
    CANVAS = 3
    ENTRY = 2
    BUTTON = 1
    LABEL = 0


class WBase:
    def __init__(self, name, parent, widget):
        self.conf = None
        self.name = name
        self.widget = widget
        self.parent = parent


    def update(self):
        print(self.conf.options)
        if self.conf._args_supported(self.conf.options):
            self.widget.config(**self.conf.options)


    def set_conf(self, **options):
        self.conf = Options(**options)

    def generate_code_for_widget(self):
        ...

    @classmethod
    def create_widget(cls, name, parent, widget, func):
        instance = cls(name, parent, widget)
        widget.bind("<Button-1>", lambda x: func(instance))
        return instance

    def get_place(self):
        return f"self.{self.name}.place(x= {self.widget.winfo_x()}, y= {self.widget.winfo_y()})"
