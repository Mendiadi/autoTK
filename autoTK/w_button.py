from autoTK.w_base import WBase, WTypes



class WButton(WBase):
    def __init__(self, name, parent, widget):
        super().__init__(name, parent, widget)
        self.conf = None
        self.onclick_template = False

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
