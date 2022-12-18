from autoTK.w_canvas import WCanvas, WTypes


class WOval(WCanvas):
    def __init__(self, name, parent, widget):
        super().__init__(name, parent, widget)
        self.conf = None
        self.bg = None
    @property
    def type(self):
        return WTypes.OVAL

    def update(self):
        if not self.bg:
            self.bg = self.conf.options.pop("bg", 0)
        super().update()


    def generate_code_for_widget(self) -> str:
        self.conf.options.pop("text", 0)

        statement = \
            f"""self.{self.name} = tk.Canvas({self.parent},
            {','.join([f' {k}= "{v}"' for k, v in self.conf.options.items()])})
            \n\t\tself.{self.name}.create_oval(0,0,{self.conf.options['width']},{self.conf.options['height']},fill=\"{self.bg}\")"""
        return statement