from autoTK.w_base import WBase


class WButton(WBase):
    def __init__(self,name,parent,widget):
        super().__init__(name,parent,widget)
        self.conf = self._get_conf()



    def _get_conf(self):
        return {"text": "hello", "bg": "black", "font": "none 12 bold"}



    def generate_code_for_widget(self) -> str:

        statement = \
            f"""self.{self.name} = tk.Button({self.parent},
            {','.join([f'{k}="{v}"' for k, v in self.conf.items()])})"""
        return statement



