import tkinter as tk


from autoTK.widgets.w_button import WButton
from autoTK.widgets.w_canvas import WCanvas
from autoTK.widgets.w_check_button import WCheckButton
from autoTK.widgets.w_entry import WEntry
from autoTK.widgets.w_label import WLabel
from autoTK.widgets.w_oval import WOval

class WidgetLayer:
    def __init__(self,root,editor):
        self.root = root



        self.editor = editor
        self.w_btns_widgets = []
        self.w_canvas = tk.Canvas(self.root, width=50, height=50, bg="red")

        self.w_canvas.bind("<Enter>", self.show)
        self.w_canvas.bind("<Leave>", self.hide)
        self.w_btn_preview = tk.Button(self.w_canvas,text="sample")
        self.w_entry_preview = tk.Entry(self.w_canvas)
        self.w_label_preview = tk.Label(self.w_canvas,text="sample")
        self.w_check_btn_preview = tk.Checkbutton(self.w_canvas,text="sample")
        self.w_canvas_preview = tk.Canvas(self.w_canvas,height=50,width=50)
        self.w_oval_preview = tk.Canvas(self.w_canvas,height=50,width=50)
        self.w_label_canvas = tk.Label(self.w_canvas, text="+", font="none 20 bold", width=1, height=1, bg="red")
        self.w_entry_name = tk.Entry(self.w_canvas, width=10)
        self.w_entry_set_parent = tk.Entry(self.w_canvas)

        self.w_btn = tk.Button(self.w_canvas, text="button",font="none 9",
                               command=lambda: self.editor.add(WButton),
                               border=0, bg="lightgreen")
        self.w_btn.bind("<Enter>",lambda x:self.enter(self.w_btn,self.w_btn_preview))
        self.w_btn.bind("<Leave>",lambda x: self.leave(self.w_btn))
        self.w_entry = tk.Button(self.w_canvas, text="entry",font="none 9",
                                 command=lambda: self.editor.add(WEntry),
                                 border=0, bg="lightgreen")
        self.w_entry.bind("<Enter>", lambda x: self.enter(self.w_entry,self.w_entry_preview))
        self.w_entry.bind("<Leave>", lambda x: self.leave(self.w_entry))
        self.w_label = tk.Button(self.w_canvas, text="label",font="none 9",
                                 command=lambda: self.editor.add(WLabel),
                                 border=0, bg="lightgreen")
        self.w_label.bind("<Enter>", lambda x: self.enter(self.w_label,self.w_label_preview))
        self.w_label.bind("<Leave>", lambda x: self.leave(self.w_label))
        self.w_canvas_create = tk.Button(self.w_canvas, text="canvas",font="none 9",
                                         command=lambda: self.editor.add(WCanvas),
                                         border=0, bg="lightgreen")
        self.w_canvas_create.bind("<Enter>", lambda x: self.enter(self.w_canvas_create,self.w_canvas_preview))
        self.w_canvas_create.bind("<Leave>", lambda x: self.leave(self.w_canvas_create))
        self.w_oval = tk.Button(self.w_canvas, text="oval",font="none 9",
                                command=lambda: self.editor.add(WOval),
                                border=0, bg="lightgreen")
        self.w_oval.bind("<Enter>", lambda x: self.enter(self.w_oval,self.w_oval_preview,True))
        self.w_oval.bind("<Leave>", lambda x: self.leave(self.w_oval))
        self.w_checkbutton = tk.Button(self.w_canvas, text="check btn",font="none 9",
                                       command=lambda: self.editor.add(WCheckButton),
                                border=0, bg="lightgreen")
        self.w_checkbutton.bind("<Enter>", lambda x: self.enter(self.w_checkbutton,self.w_check_btn_preview))
        self.w_checkbutton.bind("<Leave>", lambda x: self.leave(self.w_checkbutton))
        self.w_name_label = tk.Label(self.w_canvas, text="Variable: ", bg="red", font="none 10 bold")
        self.w_parent_label = tk.Label(self.w_canvas, text="Parent Var: ", bg="red", font="none 10 bold")
        self._preview_widget = None
        self.w_canvas.pack()
        self.w_label_canvas.pack()

    def enter(self,wid,type,oval=False):
        wid.config(font="none 10 bold")

        self._preview_widget = type
        if oval:
            self._preview_widget.create_oval(0,0,50,50,fill="red")


        self._preview_widget.pack()

    def leave(self,wid):
        wid.config(font="none 9")
        self._preview_widget.pack_forget()
        self._preview_widget = None

    def show(self, e):
        self.w_name_label.config(text="Variable:")
        self.w_parent_label.config(text="Parent Var: ")
        self.w_label_canvas.config(width=20, height=2, bg="red")
        self.w_canvas.config(width=500, height=500)
        self.w_label_canvas.config(text="")
        self.w_btn.place(x=10, y=20)
        self.w_label.place(x=70, y=20)
        self.w_entry.place(x=120, y=20)
        self.w_oval.place(x=170, y=20)
        self.w_checkbutton.place(x=210,y=20)
        self.w_canvas_create.place(x=290, y=20)
        self.w_name_label.place(x=0, y=0)
        self.w_entry_name.place(x=70, y=0)
        self.w_entry_set_parent.place(y=0, x=210)
        self.w_parent_label.place(x=150,y=0)

    def hide(self, e):
        self.w_label_canvas.config(width=1, height=1)
        self.w_canvas.config(width=1, height=1)
        self.w_btn.place_forget()
        self.w_entry_name.delete(0, tk.END)
        self.w_entry_name.place_forget()
        self.w_name_label.config(text="")
        self.w_name_label.place_forget()
        self.w_label.place_forget()
        self.w_label_canvas.config(text="+")
        self.w_entry.place_forget()
        self.w_entry_set_parent.place_forget()
        self.w_oval.place_forget()
        self.w_checkbutton.place_forget()
        self.w_parent_label.place_forget()