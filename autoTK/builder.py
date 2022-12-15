import os

from converter import Converter
from analizer import Analizer

class Builder:
    def __init__(self,name):
        self.scanner = None
        self.converter = Converter(name)

    def build(self,*widgets):
        self.scanner = Analizer(*widgets)
        self._prepare_file()

    def _prepare_file(self):
        if self.converter.name not in os.listdir():
            with open(self.converter.name + "_" +".py","w") as f:
                attrs = self.scanner.generate_definition()
                states = self.scanner.generate_placing()
                content = self.converter.create_structure(attrs,states)
                f.write(content)
                print(content)

