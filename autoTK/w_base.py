from enum import Enum

class WTypes(Enum):
    BUTTON = 1
    LABEL = 0


class WBase:
    def __init__(self,name,parent,widget):
        self.name = name
        self.widget = widget
        self.parent = parent

    def generate_code_for_widget(self):
        ...

    @classmethod
    def create_widget(cls,name,parent,widget,func):

        widget.bind("<Button-1>",lambda x: func(widget))
        return cls(name,parent,widget)

    def get_place(self):
        return f"self.{self.name}.place(x={self.widget.winfo_x()},y={self.widget.winfo_y()})"