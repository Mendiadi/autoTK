from autoTK.w_base import WBase, WTypes


class WEntry(WBase):
    def __init__(self, name, parent, widget):
        super().__init__(name, parent, widget)
        self.conf = None

    @property
    def type(self):
        return WTypes.ENTRY

    def generate_code_for_widget(self) -> str:
        self.conf.options.pop("text", 0)
        statement = \
            f"""self.{self.name} = tk.Entry({self.parent},
            {','.join([f' {k}= "{v}"' for k, v in self.conf.options.items()])})"""
        return statement
