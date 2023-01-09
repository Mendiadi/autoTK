import tkinter as tk

from autoTK.widgets.w_button import WButton
from autoTK.widgets.w_canvas import WCanvas
from autoTK.widgets.w_check_button import WCheckButton
from autoTK.widgets.w_entry import WEntry
from autoTK.widgets.w_label import WLabel
from autoTK.widgets.w_oval import WOval
from autoTK.widgets.w_text_box import WTextBox


class WidgetLayer:
    def __init__(self, root, editor):
        self.root = root

        self.editor = editor
        self.w_btns_widgets = []
        self.w_canvas = tk.Canvas(self.root, width=50, height=50, bg="red")

        self.w_canvas.bind("<Enter>", self.show)
        self.w_canvas.bind("<Leave>", self.hide)
        self.w_btn_preview = tk.Button(self.w_canvas, text="sample")
        self.w_entry_preview = tk.Entry(self.w_canvas)
        self.w_label_preview = tk.Label(self.w_canvas, text="sample")
        self.w_text_box_preview = tk.Text(self.w_canvas, width=10, height=5)
        self.w_check_btn_preview = tk.Checkbutton(self.w_canvas, text="sample")
        self.w_canvas_preview = tk.Canvas(self.w_canvas, height=50, width=50)
        self.w_oval_preview = tk.Canvas(self.w_canvas, height=50, width=50)
        self.w_label_canvas = tk.Label(self.w_canvas, text="+", font="none 20 bold", width=1, height=1, bg="red")
        self.w_entry_name = tk.Entry(self.w_canvas, width=10)
        self.w_entry_set_parent = tk.Entry(self.w_canvas, width=8)

        self.w_btn = self.editor.components.create_button(self.w_canvas,
                                                          lambda: self.enter(self.w_btn_preview), self.leave,
                                                          text="button", command=lambda: self.editor.add(WButton))
        self.w_entry = self.editor.components.create_button(self.w_canvas,
                                                            lambda: self.enter(self.w_entry_preview), self.leave,
                                                            text="entry", command=lambda: self.editor.add(WEntry))

        self.w_label = self.editor.components.create_button(self.w_canvas,
                                                            lambda: self.enter(self.w_label_preview), self.leave,
                                                            text="label", command=lambda: self.editor.add(WLabel))

        self.w_canvas_create = self.editor.components.create_button(self.w_canvas,
                                                                    lambda: self.enter(self.w_canvas_preview),
                                                                    self.leave,
                                                                    text="canvas",
                                                                    command=lambda: self.editor.add(WCanvas))

        self.w_oval = self.editor.components.create_button(self.w_canvas,
                                                           lambda: self.enter(self.w_oval_preview, True), self.leave,
                                                           text="oval", command=lambda: self.editor.add(WOval))

        self.w_checkbutton = self.editor.components.create_button(self.w_canvas,
                                                                  lambda: self.enter(self.w_check_btn_preview),
                                                                  self.leave,
                                                                  text="check btn",
                                                                  command=lambda: self.editor.add(WCheckButton))

        self.w_text_box = self.editor.components.create_button(self.w_canvas,
                                                               lambda: self.enter(self.w_text_box_preview), self.leave,
                                                               text="textbox",
                                                               command=lambda: self.editor.add(WTextBox))

        self.w_name_label = tk.Label(self.w_canvas, text="Variable: ", bg="red", font="none 10 bold")
        self.w_parent_label = tk.Label(self.w_canvas, text="Parent Var:", bg="red", font="none 10 bold")
        self._preview_widget = None
        self.w_canvas.pack()
        self.w_label_canvas.pack()

    def enter(self, type, oval=False):
        self._preview_widget = type
        if oval:
            self._preview_widget.create_oval(0, 0, 50, 50, fill="red")
        self._preview_widget.pack()

    def leave(self):
        if self._preview_widget:
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
        self.w_checkbutton.place(x=210, y=20)
        self.w_canvas_create.place(x=290, y=20)
        self.w_text_box.place(x=10, y=45)
        self.w_name_label.place(x=0, y=0)
        self.w_entry_name.place(x=70, y=0)
        self.w_entry_set_parent.place(y=0, x=250)
        self.w_parent_label.place(x=150, y=0)

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
        self.w_text_box.place_forget()
