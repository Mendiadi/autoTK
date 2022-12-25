import tkinter

from autoTK.widgets.w_base import WBase, WTypes


class WCheckButton(WBase):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.onclick_template = False
        self.supported = (
            "text", "bg", "width",
            "height", "border","font size",
            "fg","state","onvalue","font style","offvalue","font type","font"
        )

    def init(self):
        self.widget = tkinter.Checkbutton(self.parent.parent)
        self.widget.pack()
        self.set_conf(text="sample",bg="white",onvalue=1,offvalue=0,border=1,fg="black")

    @property
    def type(self):
        return WTypes.CHECKBUTTON

    def update_widget_option(self,value,supported):
        self.conf.options[supported] = value
        self.conf.update_font()
        self.update()

    def generate_code_for_widget(self) -> str:

        if self.onclick_template:
            self.conf.options["command"] = f"self.{self.name}_onclick"

        l = []
        for k, v in self.conf.options.items():
            if k != "command":
                if k == "font":
                    v1 = f"(\"{self.conf._font[0]}\", {self.conf._font[1]},\"{self.conf._font[2]}\")"
                    l.append(f' {k}= {v1}')
                else:
                    l.append(f' {k}= "{v}"')
            else:

                l.append(f' {k}= {v}')

        statement = \
            f"""self.{self.name} = tk.Checkbutton({self.parent.name},
                   {','.join(l)})"""
        return statement
