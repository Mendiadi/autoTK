from autoTK.w_base import WBase
from options import Options

class WButton(WBase):
    def __init__(self,name,parent,widget):
        super().__init__(name,parent,widget)
        self.conf = None





    def generate_code_for_widget(self) -> str:

        statement = \
            f"""self.{self.name} = tk.Button({self.parent},
            {','.join([f'{k}="{v}"' for k, v in self.conf.options.items()])})"""
        return statement



