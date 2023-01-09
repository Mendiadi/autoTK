import tkinter

from autoTK.widgets.w_base import WBase, WTypes


class WTextBox(WBase):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.supported = ("bg", "width", "height", "border", "font style", "font type", "fg", "font size", "font")

    def init(self):
        self.widget = tkinter.Text(self.parent.parent)
        self.set_conf(bg="white", width=10, height=5)
        self.widget.pack()

    def update_widget_option(self, value, supported):
        self.conf.options[supported] = value
        self.conf.update_font()
        self.update()

    @property
    def type(self):
        return WTypes.TEXTBOX

    def generate_code_for_widget(self) -> str:
        self.conf.options.pop("text", 0)
        l = []

        for k, v in self.conf.options.items():

            if k == "font":
                v1 = f"(\"{self.conf._font[0]}\", {self.conf._font[1]},\"{self.conf._font[2]}\")"
                l.append(f' {k}= {v1}')
            else:
                l.append(f' {k}= "{v}"')

        statement = \
            f"""self.{self.name} = tk.Text({self.parent.name},
                   {','.join(l)})"""
        return statement
