
class Statements:
    def __init__(self ,*widgets):
        self.widgets = widgets


    def generate_definition(self):
        function_block = []
        for w in self.widgets:
            function_block.append(w.generate_code_for_widget())
        print(function_block)
        return "\n\t\t".join(function_block)


    def generate_placing(self):
        function_block = []
        for w in self.widgets:
            function_block.append(w.get_place())
        print(function_block)
        return "\n\t\t".join(function_block)
