import os

from autoTK.w_button import WButton
from converter import Converter
from analizer import Analizer


class Builder:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.scanner = None
        self.converter = None
        self.bg="white"
    def build(self, *widgets):
        self.converter = Converter(self.name, self.size, [
            w for w in widgets if type(w) == WButton and w.onclick_template
        ],self.bg)
        self.scanner = Analizer(*widgets)
        self._prepare_file()

    def _prepare_file(self):
        if self.converter.name not in os.listdir():
            with open(self.converter.name + "_" + ".py", "w") as f:
                attrs = self.scanner.generate_definition()
                states = self.scanner.generate_placing()
                content = self.converter.create_structure(attrs, states)
                f.write(content)
                print(content)
