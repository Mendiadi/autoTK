import os

from autoTK.widgets.w_button import WButton
from autoTK.providers.structure import Structure
from autoTK.providers.statements import Statements


class Provider:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.w_statements = None
        self.structure = None
        self.bg="white"
        self.dir = None


    def build(self,dir, *widgets):
        self.dir = dir
        self.structure = Structure(self.name, self.size, [
            w for w in widgets if type(w) == WButton and w.onclick_template
        ], self.bg)
        self.w_statements = Statements(*widgets)
        self._prepare_file()

    def _prepare_file(self):

        if self.structure.name not in os.listdir():
            path = os.path.join(self.dir,self.structure.name + "_" + ".py")
            with open(path, "w") as f:
                attrs = self.w_statements.generate_definition()
                states = self.w_statements.generate_placing()
                content = self.structure.create_structure(attrs, states)
                f.write(content)

