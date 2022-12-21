import tkinter

from autoTK.widgets.w_base import WBase, WTypes


class WLabel(WBase):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.supported = (
            "text", "bg", "width",
            "height", "border",
            "fg","font style","font size","font type","font"
        )

    def init(self):
        self.widget = tkinter.Label(self.parent.parent)
        self.widget.pack()
        self.set_conf(text="sample")

    @property
    def type(self):
        return WTypes.LABEL

    def generate_code_for_widget(self) -> str:
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
            f"""self.{self.name} = tk.Label({self.parent.name},
            {','.join(l)})"""
        return statement
