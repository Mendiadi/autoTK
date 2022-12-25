import functools
import tkinter as tk
from typing import Callable, Sequence


class WAutoTK:
    def __init__(self,**theme):
        self.sub = theme.get("sub","lightgreen")
        self.theme = theme.get("theme","lightblue")
        self.font = theme.get("font","none 9")
        self.sub_font = theme.get("sub_font","none 10")

        self.components = []



    def _enter(self,wid,func:Callable):
        wid.config(font=self.sub_font,bg=self.sub)

        if func:
            func()


    def _leave(self,wid,func:Callable):
        wid.config(font=self.font,bg=self.theme)
        if func:
            func()

    def create_button(self,master_,*register_funcs:[Callable],**kwargs):
        btn = tk.Button(master_, text="button", font=self.font,
                               border=0, bg=self.theme)
        btn.config(**kwargs)
        print(register_funcs)
        f_enter , f_leav = None,None
        if len(register_funcs) == 2:
             f_enter,f_leav = register_funcs[0],register_funcs[1]
        btn.bind("<Enter>",lambda x: self._enter(btn,f_enter))
        btn.bind("<Leave>",lambda x: self._leave(btn,f_leav))
        self.components.append(btn)
        return btn

    def update_theme(self,**theme):
        self.sub = theme.get("sub", "lightgreen")
        self.theme = theme.get("theme", "lightblue")
        self.font = theme.get("font", "none 9")
        self.sub_font = theme.get("sub_font", "none 10")
        for c in self.components:
            c.config(bg=self.theme,font=self.font)


    def create_radio_buttons(self,master,modes:Sequence,**kwargs):
        if not modes:
            return
        if type(modes[0]) == str:
            var = tk.StringVar()
        else:
            var = tk.IntVar()
        can = tk.Canvas(master,bg=self.theme)
        command = kwargs.pop("command", None)

        for mode in modes:
            if command:

                f=functools.partial(command,value=mode)
            else:
                f= None
            a = tk.Radiobutton(can,text=mode,value=mode,variable=var,command=f)
            a.config(**kwargs)
            a.pack()
        var.set(modes[0])
        return var, can

def click(value):
    print(value)

if __name__ == '__main__':
    a = WAutoTK()
    win = tk.Tk()
    win.geometry("500x500")
    l = ["option1","option2","option3"]
    var , can =a.create_radio_buttons(win,l,command=click)
    can.pack()
    print(var.get())
    win.mainloop()