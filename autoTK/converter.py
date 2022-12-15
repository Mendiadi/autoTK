

class Converter:
    def __init__(self,classname):
        self.structure = {"size":"700x700"}
        self.name = classname


    def _get_main_template(self):
        return f"if __name__ == '__main__':\n\t" \
               f"root = tk.Tk()\n\t" \
               f"gui = {self.name}(root)\n\t" \
               f"root.geometry('{self.structure['size']}')" \
               f"\n\tgui.load()\n\troot.mainloop()"

    def _get_base_template(self):
        return "import tkinter as tk" \
               f"\n\nclass {self.name}:\n" \
               f"\tdef __init__(self,win):\n" \
               f"\t\tself.win = win\n\t\t"

    def create_structure(self,attributes,statements):
        print("*"*100,attributes)
        top_template = self._get_base_template()
        top_template += "".join(attributes)

        load_func = "\n\tdef load(self):\n\t\t"
        load_func += "".join(statements)
        return f"{top_template}\n{load_func}\n{self._get_main_template()}"