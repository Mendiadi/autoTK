import tkinter as tk


from placer import Placer
from builder import Builder
from w_base import WTypes

class Screen:
    def __init__(self,win,gui):
        self.win = win
        self.gui = gui

    def destroy(self):
        for child in self.win.winfo_children():
            child.destroy()

class StartScreen(Screen):
    def __init__(self,win,gui):
        super().__init__(win,gui)
        self.headline = tk.Label(self.win,text="WELCOME TO TKINTER DESIGNER",font="none 20 bold")
        self.canvas = tk.Canvas(self.win,width=100,height=100,bg="lightblue",border=0)

        self.canvas.bind("<Enter>",self.canvas_enter)
        self.canvas.bind("<Leave>", self.canvas_leave)
        self.create_btn = tk.Button(self.canvas,text="create",command=self._create)
        self.entry_name = tk.Entry(self.canvas,width=30)
        self.label_on_canvas = tk.Label(self.canvas, text="NEW")
        self.label_info = tk.Label(self.canvas, text="Enter file name:",bg="lightblue")
        self.headline.pack()
        self.canvas.pack(pady=100)
        self.label_on_canvas.pack(pady=5)

    def _create(self):
        self.gui.add_builder(self.entry_name.get())

        self.gui.move_to_editor()


    def canvas_enter(self,e):
        self.canvas.config(width=1000, height=1000,bg="lightblue",border=0)

        self.label_on_canvas.config(bg="lightblue",width=100)
        self.label_info.pack(pady=20)
        self.entry_name.pack(pady=20)
        self.create_btn.pack(pady=20)


    def canvas_leave(self,e):
        self.label_on_canvas.config(bg="white",width=3)
        self.canvas.config(width=100,height=100)

        self.label_info.forget()
        self.create_btn.forget()
        self.entry_name.forget()




class RenderEditor(Screen):
    def __init__(self, win,gui):
        super().__init__(win,gui)
        # master window
        self.win = win

        # actual rendering window
        self.second_win = tk.Frame(self.win, height=500, width=500, bg="grey")

        self.second_win.pack_propagate(False)
        self.placer = Placer(self.second_win)
        # widgets layer
        self.w_canvas = tk.Canvas(self.win, width=50, height=50,bg="red")

        self.w_canvas.bind("<Enter>", self.show_widgets_layer)
        self.w_canvas.bind("<Leave>", self.hide_widgets_layer)
        self.w_label_canvas = tk.Label(self.w_canvas, text="+", font="none 20 bold",width=1, height=1,bg="red")
        self.w_btn = tk.Button(self.w_canvas, text="button",command=lambda:self.add(WTypes.BUTTON))
        self.w_label = tk.Button(self.w_canvas, text="label", command=lambda:self.add(WTypes.LABEL))
        self.w_canvas.pack()
        self.w_label_canvas.pack()

        # top bar
        self.top_bar = tk.Canvas(self.win, height=100, width=400, bg="lightblue")
        self.txt_choosen_name = tk.Label(self.top_bar)
        tk.Button(self.top_bar, text="save",
                  command=self.save).place(x=50, y=30)
        self.txt_choosen_name.place(x=0,y=0)

        # tools
        self.top_bar.pack()
        self.second_win.pack(pady=50)





    def add(self,type_):
        self.placer.add_widget(type_)
        self.txt_choosen_name.config(text=self.placer.choosen_name)


    def show_widgets_layer(self,e):
        self.w_label_canvas.config(width=20,height=2,bg="red")
        self.w_canvas.config(width=500,height=500)
        self.w_btn.place(x=70,y=20)
        self.w_label.place(x=20,y=20)

    def hide_widgets_layer(self,e):
        self.w_label_canvas.config(width=1, height=1)
        self.w_canvas.config(width=1, height=1)
        self.w_btn.forget()

    def save(self):
        self.gui.builder.build(*self.placer.widgets.values())




class GUI:
    def __init__(self,win):
        win.geometry("1000x1000")
        self.temp = None
        self.screen = RenderEditor(win,self)

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