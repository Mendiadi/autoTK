import tkinter

from autoTK.widgets.w_base import WBase, WTypes


class WEntry(WBase):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.supported = ("bg", "width", "border","fg","font style","font size", "font type","font")

    def init(self):
        self.widget = tkinter.Entry(self.parent.parent)
        self.set_conf()
        self.widget.pack()

    @property
    def type(self):
        return WTypes.ENTRY

    def generate_code_for_widget(self) -> str:
        self.conf.options.pop("text", 0)
        l = []
        f_style = self.conf.options.pop("font style", 0)
        f_size = self.conf.options.pop("font size", 0)
        for k, v in self.conf.options.items():

            if k == "font":
                v1 = f"(\"{v}\", {f_size},\"{f_style}\")"
                l.append(f' {k}= {v1}')
            else:
                l.append(f' {k}= "{v}"')

        statement = \
            f"""self.{self.name} = tk.Entry({self.parent.name},
                   {','.join(l)})"""
        return statement
