import tkinter as tk


from placer import Placer
from builder import Builder
from w_base import WTypes

class Screen:
    def __init__(self,win,gui):
        self.win = win
        self.gui = gui
    def show(self):
        ...

    def destroy(self):
        for child in self.win.winfo_children():
            child.destroy()

class StartScreen(Screen):
    def __init__(self,win,gui):
        super().__init__(win,gui)
        self.headline = tk.Label(self.win,text="WELCOME TO TKINTER DESIGNER",font="none 20 bold")
        self.canvas = tk.Canvas(self.win,width=50,height=50,bg="lightblue",border=0)

        self.canvas.bind("<Enter>",self.canvas_enter)
        self.canvas.bind("<Leave>", self.canvas_leave)
        self.create_btn = tk.Button(self.canvas,text="create",command=self._create)
        self.entry_name = tk.Entry(self.canvas,width=50)
        self.label_on_canvas = tk.Label(self.canvas, text="NEW")
        self.headline.pack()
        self.canvas.pack()
        self.label_on_canvas.pack()

    def _create(self):
        self.gui.add_builder(self.entry_name.get())

        self.gui.move_to_editor()


    def canvas_enter(self,e):
        self.canvas.config(width=500, height=500,bg="lightblue",border=0)
        self.create_btn.pack()
        self.entry_name.pack()

    def canvas_leave(self,e):
        self.canvas.config(width=50,height=50)
        self.create_btn.forget()
        self.entry_name.forget()




class RenderEditor(Screen):
    def __init__(self, win,gui):
        super().__init__(win,gui)
        # master window
        self.win = win


        # top bar
        self.top_bar = tk.Canvas(self.win, height=100, width=400, bg="lightblue")


        # actual rendering window
        self.second_win = tk.Frame(self.win, height=700, width=700, bg="grey")

        self.second_win.pack_propagate(False)
        self.placer = Placer(self.second_win)

        # tools


        self.btn = tk.Button(self.top_bar, text="add",
                             command=lambda: self.placer.add_widget(WTypes.BUTTON))

        self.top_bar.pack()
        self.second_win.pack(pady=50)
        self.btn.place(y=0, x=0)
        tk.Button(self.top_bar, text="add l",
                  command=lambda: self.placer.add_widget(WTypes.LABEL)).place(x=0, y=30)
        tk.Button(self.top_bar, text="save",
                  command=self.save).place(x=50, y=30)

    def save(self):
        self.gui.builder.build(*self.placer.widgets.values())




class GUI:
    def __init__(self,win):
        win.geometry("1000x1000")
        self.temp = None
        self.screen = StartScreen(win,self)

        self.builder =None

    def add_builder(self,name):
        self.builder =  Builder(name)

    def move_to_editor(self):
        self.screen.destroy()
        self.temp = RenderEditor(self.screen.win,self)







if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)

    root.mainloop()