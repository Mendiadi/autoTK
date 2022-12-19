import tkinter as tk


from autoTK.widgets.w_button import WButton
from autoTK.widgets.w_canvas import WCanvas
from autoTK.widgets.w_entry import WEntry
from autoTK.widgets.w_label import WLabel
from autoTK.widgets.w_oval import WOval
from autoTK.editor.renderwindow import RenderWindow
from autoTK.utils.common_types import Screen
from autoTK.editor.top_bar import TopBar

class RenderEditor(Screen):
    def __init__(self, win, gui, height, width):
        super().__init__(win, gui)
        # master window
        self.win = win
        self.top_bar = TopBar(self.win, self)
        # actual rendering window

        self.second_win = tk.Frame(self.win, height=height, width=width, bg="white")

        self.second_win.pack_propagate(False)
        self.placer = RenderWindow(self.second_win)
        self.placer.add_handler("update", self.top_bar.update)
        self.placer.add_handler("select", self.select_widget)
        self.placer.add_handler("top_bar", self.handle_top_bar)

        # widgets layer

        self.w_btns_widgets = []
        self.w_canvas = tk.Canvas(self.win, width=50, height=50, bg="red")

        self.w_canvas.bind("<Enter>", self.show_widgets_layer)
        self.w_canvas.bind("<Leave>", self.hide_widgets_layer)
        self.w_label_canvas = tk.Label(self.w_canvas, text="+", font="none 20 bold", width=1, height=1, bg="red")
        self.w_entry_name = tk.Entry(self.w_canvas, width=20)
        self.w_entry_set_parent = tk.Entry(self.w_canvas)

        self.w_btn = tk.Button(self.w_canvas, text="button", command=lambda: self.add(WButton),
                               border=0, bg="lightgreen")
        self.w_entry = tk.Button(self.w_canvas, text="entry", command=lambda: self.add(WEntry),
                                 border=0, bg="lightgreen")
        self.w_label = tk.Button(self.w_canvas, text="label", command=lambda: self.add(WLabel),
                                 border=0, bg="lightgreen")
        self.w_canvas_create = tk.Button(self.w_canvas, text="canvas", command=lambda: self.add(WCanvas),
                                         border=0, bg="lightgreen")
        self.w_oval = tk.Button(self.w_canvas, text="oval", command=lambda: self.add(WOval),
                                border=0, bg="lightgreen")
        self.w_name_label = tk.Label(self.w_canvas, text="Variable: ", bg="red", font="none 10 bold")
        self.w_canvas.pack()
        self.w_label_canvas.pack()

        tk.Button(self.win, text="save",
                  command=self.save).place(x=50, y=30)
        self.bg_entry = tk.Entry(self.win)
        self.bg_entry.place(x=50, y=70)
        self.bg_entry.insert(0, "white")
        self.bg_entry.bind("<Leave>", lambda e: self.second_win.config(bg=self.bg_entry.get()))
        # top bar

        # list box
        self.list_box = tk.Listbox(self.win)
        self.list_box.place(x=10, y=300)
        self.list_box_multi = tk.Listbox(self.win, bg="lightblue", height=9, font="none 10 bold")
        self.button_del_wid = tk.Button(self.win, text="delete",
                                        command=lambda: self.placer.delete_selected(self.list_box))
        self.button_del_wid.place(x=10, y=700)
        # tools

        self.second_win.pack(pady=50)
        self.active = True
        self.list_box.bind("<Motion>", lambda x: self.handle_choose_from_list_box())
        self.in_updating_options = False
        self.temp_values = None

    def handle_top_bar(self):
        if self.placer.choosen_name:
            self.top_bar.show()
        else:

            self.top_bar.hide()

    def handle_choose_from_list_box(self):

        if self.list_box.size():
            name = self.list_box.get(tk.ANCHOR)
            if self.placer.choosen_name != name:
                wid = self.placer.get_widget(name)
                self.placer.set_choosen(wid)
                self.top_bar.generate_content(wid)
                self.top_bar.update(wid)

    def select_widget(self, wid):
        if not wid:
            return
        self.list_box.selection_clear(0, tk.END)
        self.list_box.select_set(wid.index)
        self.list_box.select_anchor(wid.index)
        self.top_bar.generate_content(wid)
        self.top_bar.update(wid)

    def duplicate_widget(self):
        self.placer.duplicate()
        self.list_box.insert(tk.END, self.placer.choosen_name)

    def add(self, type_):
        name = self.w_entry_name.get()
        if not name or name in self.placer.widgets:
            name = f"var_{self.placer.amounts}"

        p = self.w_entry_set_parent.get()
        if p not in self.placer.widgets:
            p = None
        self.placer.add_widget(type_, name, parent=p if p else None)
        self.list_box.insert(tk.END, self.placer.choosen_name)

    def show_widgets_layer(self, e):
        self.w_name_label.config(text="Variable:")
        self.w_label_canvas.config(width=20, height=2, bg="red")
        self.w_canvas.config(width=500, height=500)
        self.w_label_canvas.config(text="")
        self.w_btn.place(x=70, y=20)
        self.w_label.place(x=20, y=20)
        self.w_entry.place(x=120, y=20)
        self.w_oval.place(x=220, y=20)
        self.w_canvas_create.place(x=160, y=20)
        self.w_name_label.place(x=0, y=0)
        self.w_entry_name.place(x=70, y=0)
        self.w_entry_set_parent.place(y=0, x=210)

    def hide_widgets_layer(self, e):
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

    def save(self):
        self.gui.builder.bg = self.bg_entry.get()
        self.gui.builder.build(*self.placer.widgets.values())


