import tkinter

from autoTK.w_canvas import WCanvas, WTypes


class WOval(WCanvas):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.conf = None
        self.bg = None
        self.supported = (*self.supported, "inner color")

    def init(self):
        self.widget = tkinter.Canvas(self.parent.parent)
        self.set_conf(width=100, height=100, bg="red")
        self.widget.create_oval(0, 0, self.conf.options['width'], self.conf.options['height'],
                                fill=self.conf.options['bg'])
        self.widget.pack()

    @property
    def type(self):
        return WTypes.OVAL

    def update(self):
        if not self.bg:
            self.bg = self.conf.options.pop("bg", 0)
        super().update()

    def generate_code_for_widget(self) -> str:
        statement = \
            f"""self.{self.name} = tk.Canvas({self.parent.name},
            {','.join([f' {k}= "{v}"' for k, v in self.conf.options.items()])})
            \n\t\tself.{self.name}.create_oval(0,0,{self.conf.options['width']},{self.conf.options['height']},fill=\"{self.bg}\")"""
        return statement
