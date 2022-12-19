import tkinter

from autoTK.widgets.w_base import WBase, WTypes


class WLabel(WBase):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.supported = (
            "text", "bg", "width",
            "height", "border", "font",
            "fg"
        )

    def init(self):
        self.widget = tkinter.Label(self.parent.parent)
        self.widget.pack()
        self.set_conf(text="sample")

    @property
    def type(self):
        return WTypes.LABEL

    def generate_code_for_widget(self) -> str:
        statement = \
            f"""self.{self.name} = tk.Label({self.parent.name},
            {','.join([f' {k}= "{v}"' for k, v in self.conf.options.items()])})"""
        return statement
