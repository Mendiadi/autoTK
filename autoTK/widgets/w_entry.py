import tkinter

from autoTK.widgets.w_base import WBase, WTypes


class WEntry(WBase):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.supported = ("bg", "width", "border", "font")

    def init(self):
        self.widget = tkinter.Entry(self.parent.parent)
        self.set_conf()
        self.widget.pack()

    @property
    def type(self):
        return WTypes.ENTRY

    def generate_code_for_widget(self) -> str:
        self.conf.options.pop("text", 0)
        statement = \
            f"""self.{self.name} = tk.Entry({self.parent.name},
            {','.join([f' {k}= "{v}"' for k, v in self.conf.options.items()])})"""
        return statement
