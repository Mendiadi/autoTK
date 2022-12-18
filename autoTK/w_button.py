import tkinter

from autoTK.w_base import WBase, WTypes



class WButton(WBase):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.onclick_template = False
        self.supported = ("text", "bg", "width", "height", "border", "font")
        self.widget = tkinter.Button(parent.parent)
        self.widget.pack()
        self.set_conf(text="sample")
    @property
    def type(self):
        return WTypes.BUTTON

    def generate_code_for_widget(self) -> str:
        if self.onclick_template:
            self.conf.options["command"] = f"self.{self.name}_onclick"
        statement = \
            f"""self.{self.name} = tk.Button({self.parent},
            {','.join([f' {k}= "{v}"' if k != "command" else f' {k}= {v}' for k, v in self.conf.options.items()])})"""
        return statement
