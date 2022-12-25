import tkinter

import tkinter as tk

from autoTK.widgets.w_base import WBase, WTypes


class WLabel(WBase):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.supported = (
            "text", "bg", "width",
            "height", "border",
            "fg","image","font size","font type","font style","font"
        )


    def update_widget_option(self,value,supported):
        self.conf.options[supported] = value
        if supported == "image":
            img = tk.PhotoImage(file=value(), name=value())
            self.set_conf(image=img)
        self.conf.update_font()
        self.update()

    def init(self):
        self.widget = tkinter.Label(self.parent.parent)
        self.widget.pack()
        self.set_conf(text="sample",fg="black",border=1,bg="white")

    @property
    def type(self):
        return WTypes.LABEL

    def generate_code_for_widget(self) -> str:
        l = []
        image_statement = ""
        for k, v in self.conf.options.items():
            if k == "image":
                l.append(f' {k}= self.{self.name + "_image"}')
                image_statement = f"self.{self.name + '_image'} = tk.PhotoImage(file=r\"{v}\")\n\t\t"
                continue
            if k == "font":
                v1 = f"(\"{self.conf._font[0]}\", {self.conf._font[1]},\"{self.conf._font[2]}\")"
                l.append(f' {k}= {v1}')
            else:
                l.append(f' {k}= "{v}"')

        statement = \
            f"""{image_statement}self.{self.name} = tk.Label({self.parent.name},
            {','.join(l)})"""
        return statement
