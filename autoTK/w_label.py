from autoTK.options import Options
from autoTK.w_base import WBase


class WLabel(WBase):
    def __init__(self, name, parent, widget):
        super().__init__(name, parent, widget)
        self.conf = None



    def generate_code_for_widget(self) -> str:
        statement = \
            f"""self.{self.name} = tk.Label({self.parent},
            {','.join([f'{k}="{v}"' for k, v in self.conf.options.items()])})"""
        return statement



