import tkinter

from autoTK.widgets.w_base import WBase, WTypes


class WCanvas(WBase):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.supported = ("bg", "width", "height", "border")

    def init(self):
        self.widget = tkinter.Canvas(self.parent.parent)
        self.widget.pack_propagate(False)
        self.widget.pack()
        self.set_conf(height=50,width=50,bg="white",border=1)

    def update_widget_option(self,value,supported):
        self.conf.options[supported] = value

        self.update()

    @property
    def type(self):
        return WTypes.CANVAS

    def generate_code_for_widget(self) -> str:
        self.conf.options.pop("text", 0)
        statement = \
            f"""self.{self.name} = tk.Canvas({self.parent.name},
            {','.join([f' {k}= "{v}"' for k, v in self.conf.options.items()])})"""
        return statement
