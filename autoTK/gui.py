import threading
import time
import tkinter as tk

from autoTK.options import Options
from autoTK.w_button import WButton
from autoTK.w_entry import WEntry
from autoTK.w_label import WLabel
from placer import Placer
from builder import Builder
from w_base import WTypes


class Screen:
    def __init__(self, win, gui):
        self.win = win
        self.gui = gui

    def destroy(self):
        for child in self.win.winfo_children():
            child.destroy()


class StartScreen(Screen):

    content = """
    autoTK is new Live Editor Tool for building and Design GUI
    Applications Fast and Easy.
     its Allowed you to create the template design for your project.
    autoTK Generating the Code for you!
     you can after modify the code to your own idea
    and fit the code for your purpose.
     the code only provide the window template.
    somthing that will save your time and helps to design better!
    """

    def __init__(self, win, gui):
        super().__init__(win, gui)
        self.headline = tk.Label(self.win, text="WELCOME TO TKINTER DESIGNER", font="none 20 bold",bg="lightblue")
        self.canvas = tk.Canvas(self.win, width=100, height=100, bg="lightblue", border=0)
        self.content_label = tk.Label(self.win,text=self.content,bg="lightblue",font="none 10 bold")
        self.canvas.bind("<Enter>", self.canvas_enter)
        self.canvas.bind("<Leave>", self.canvas_leave)
        self.create_btn = tk.Button(self.canvas, text="Create New Window", command=self._create,
                                    border=0,font="none 10 bold",bg="deepskyblue2")
        self.entry_name = tk.Entry(self.canvas, width=15,border=0,bg="deepskyblue2",font="none 10 bold")


        self.label_on_canvas = tk.Label(self.canvas, text="NEW",bg="lightblue")
        self.label_info = tk.Label(self.canvas, text="Enter Project name:", bg="lightblue")
        self.entry_width = tk.Entry(self.canvas, width=10,border=0,bg="deepskyblue2",font="none 10 bold")
        self.label_info_width = tk.Label(self.canvas, text="WIDTH: ", bg="lightblue")
        self.entry_height = tk.Entry(self.canvas, width=10,border=0,bg="deepskyblue2",font="none 10 bold")
        self.label_info_height = tk.Label(self.canvas, text="HEIGHT: ", bg="lightblue")
        self.headline.pack()
        self.canvas.pack(pady=100)
        self.label_on_canvas.pack(pady=5)
        self.content_label.pack(pady=5)
        self.entry_height.insert(0,"500")
        self.entry_width.insert(0,"500")



    def _create(self):
        height, width = self.entry_height.get(), self.entry_width.get()
        self.gui.add_builder(self.entry_name.get(), f"{width}x{height}")
        self.gui.move_to_editor(w=width, h=height)

    def canvas_enter(self, e):
        self.canvas.config(width=1000, height=1000, bg="lightblue", border=0)

        self.label_on_canvas.config(bg="lightblue", width=100,text="")
        self.label_info.pack()
        self.entry_name.pack(pady=5)

        self.label_info_width.pack(pady=5)
        self.entry_width.pack(pady=5)
        self.label_info_height.pack(pady=5)
        self.entry_height.pack(pady=5)
        self.create_btn.pack(pady=5)


    def canvas_leave(self, e):
        self.label_on_canvas.config(bg="lightblue", width=3,text="NEW")
        self.canvas.config(width=100, height=100)
        self.label_info_width.forget()
        self.entry_width.forget()
        self.label_info_height.forget()
        self.entry_height.forget()
        self.label_info.forget()
        self.create_btn.forget()
        self.entry_name.pack_forget()
        self.entry_name.pack_forget()


class RenderEditor(Screen):
    def __init__(self, win, gui, height, width):
        super().__init__(win, gui)
        # master window
        self.win = win

        # actual rendering window

        self.second_win = tk.Frame(self.win, height=height, width=width, bg="white")


        self.second_win.pack_propagate(False)
        self.placer = Placer(self.second_win)
        # widgets layer

        self.w_btns_widgets = []
        self.w_canvas = tk.Canvas(self.win, width=50, height=50, bg="red")

        self.w_canvas.bind("<Enter>", self.show_widgets_layer)
        self.w_canvas.bind("<Leave>", self.hide_widgets_layer)
        self.w_label_canvas = tk.Label(self.w_canvas, text="+", font="none 20 bold", width=1, height=1, bg="red")
        self.w_entry_name = tk.Entry(self.w_canvas, width=20)
        self.w_entry_set_parent = tk.Entry(self.w_canvas)

        self.w_btn = tk.Button(self.w_canvas, text="button", command=lambda: self.add(WTypes.BUTTON),
                               border=0,bg="lightgreen")
        self.w_entry = tk.Button(self.w_canvas, text="entry", command=lambda: self.add(WTypes.ENTRY),
                               border=0,bg="lightgreen")
        self.w_label = tk.Button(self.w_canvas, text="label", command=lambda: self.add(WTypes.LABEL),
                               border=0,bg="lightgreen")
        self.w_name_label = tk.Label(self.w_canvas, text="Variable: ", bg="red",font="none 10 bold")
        self.w_canvas.pack()
        self.w_label_canvas.pack()

        tk.Button(self.win, text="save",
                  command=self.save).place(x=50, y=30)
        self.bg_entry = tk.Entry(self.win)
        self.bg_entry.place(x=50, y=70)
        self.bg_entry.insert(0,"white")
        self.bg_entry.bind("<Leave>",lambda e:self.second_win.config(bg=self.bg_entry.get()))
        # top bar
        self.top_bar = tk.Canvas(self.win, height=150, width=600, bg="lightblue")
        self.txt_choosen_name = tk.Label(self.top_bar)
        self.options_entries = {}
        self.set_x_entry = tk.Entry(self.top_bar, width=8, bg="green")
        self.set_y_entry = tk.Entry(self.top_bar, width=8, bg="red")
        self.set_y_entry.bind("<Leave>",lambda x:self.placer.choosen.place(y=int(self.set_y_entry.get())))
        self.set_x_entry.bind("<Leave>", lambda x: self.placer.choosen.place(x=int(self.set_y_entry.get())))
        import functools

        for i, supported in enumerate(Options().supported):
            tk.Label(self.top_bar, text=supported, bg="lightblue",font="none 12 bold").place(x=(i * 100) + 5, y=15)

            e = tk.Entry(self.top_bar, width=10,bg="deepskyblue",border=0,font="none 10 bold")
            update_fn = functools.partial(self.update_widget_options, supported=supported, entry=e)
            e.bind("<Leave>", update_fn)
            print("%" * 50, supported)

            e.place(x=(i * 100) + 5, y=50)
            self.options_entries[supported] = e
        self.txt_choosen_name.place(x=200, y=120)
        self.duplicate_btn = tk.Button(self.top_bar, text="clone", command=self.duplicate_widget)
        self.duplicate_btn.place(x=450, y=80)
        self.multi_selected_var = tk.IntVar()
        self.multi_selected_check_btn = tk.Checkbutton(self.top_bar,
                                                       text="multiple",
                                                       variable=self.multi_selected_var,
                                                       offvalue=0, onvalue=1,
                                                       bg="lightblue", border=0, activebackground="lightblue",
                                                       selectcolor="grey")
        self.enable_auto_correct_check_var = tk.IntVar()
        self.enable_auto_correct_check_btn = tk.Checkbutton(self.top_bar,
                                                            text="enable auto correct",
                                                            variable=self.enable_auto_correct_check_var,
                                                            offvalue=0, onvalue=1,
                                                            bg="lightblue", border=0, activebackground="lightblue",
                                                            selectcolor="grey")
        self.add_onclick_template_var = tk.IntVar()
        self.add_onclick_template_btn = tk.Checkbutton(self.top_bar,
                                                       text="add onclick template",
                                                       variable=self.add_onclick_template_var,
                                                       offvalue=0, onvalue=1,
                                                       bg="lightblue", border=0, activebackground="lightblue",
                                                       selectcolor="grey")
        self.multi_selected_check_btn.place(x=500, y=90)
        self.enable_auto_correct_check_btn.place(x=50, y=90)


        self.set_y_entry.place(x=400,y=130)
        self.set_x_entry.place(x=500, y=130)
        # list box
        self.list_box = tk.Listbox(self.win)
        self.list_box.place(x=10, y=300)
        self.list_box_multi = tk.Listbox(self.win,bg="lightblue",height=9,font="none 10 bold")
        self.button_del_wid = tk.Button(self.win, text="delete",
                                        command=lambda: self.placer.delete_selected(self.list_box, self.list_box_multi))
        self.button_del_wid.place(x=10, y=700)
        # tools
        self.top_bar.pack()
        self.second_win.pack(pady=50)
        self.active = True
        threading.Thread(target=self._thread_update_chosen, daemon=True).start()
        self.in_updating_options = False
        self.temp_values = None
        print(self.w_btns_widgets)
        self.temp_multi_selection = list(self.placer.selected_multi_list)


    def update_widget_options(self, e, entry, supported):
        print("moshe")
        if self.placer.amounts < 1:
            return
        self.in_updating_options = True
        wid = self.placer.get_widget(self.placer.choosen_name)
        wid.conf.options[supported] = entry.get()
        print(wid.conf.options, supported)
        wid.update()
        self.in_updating_options = False

    def update_top_bar(self):
        if self.in_updating_options:
            return
        op = self.placer.get_widget(self.placer.choosen_name)
        temp = dict(op.conf.options)
        for entry in self.options_entries.values():
            entry.delete(0, tk.END)
        for option, value in temp.items():
            e = self.options_entries[option]
            e.insert(0, value)

        if type(op) == WEntry:
            self.options_entries["height"].config(state="disabled")
        else:
            self.options_entries["height"].config(state="normal")

        if type(op) == WButton:
            self.add_onclick_template_btn.place(x=10, y=70)
            self.add_onclick_template_var.set(op.onclick_template)
        else:
            self.add_onclick_template_btn.place_forget()

    def select_widget(self, wid):
        if not wid:
            return

        self.list_box.selection_clear(0, tk.END)
        self.list_box.select_set(wid.index)
        self.list_box.select_anchor(wid.index)
        self.update_top_bar()

    def auto_fill_x_y_entries(self):
        if self.set_y_entry.get() != str(self.placer.choosen.winfo_y()) or \
                self.set_x_entry.get() != str(self.placer.choosen.winfo_x()):
            self.set_y_entry.delete(0, tk.END)
            self.set_x_entry.delete(0, tk.END)
            self.set_y_entry.insert(0, str(self.placer.choosen.winfo_y()))
            self.set_x_entry.insert(0, str(self.placer.choosen.winfo_x()))

    def _thread_update_chosen(self):
        pos = ""
        while self.active:
            time.sleep(0.5)
            if type(self.placer.choosen) == tk.Button:
                if self.add_onclick_template_var.get() == 1:
                    print("yes")
                    self.placer.get_widget(self.placer.choosen_name).onclick_template = True
                else:
                    print("no")
                    self.placer.get_widget(self.placer.choosen_name).onclick_template = False
            if self.enable_auto_correct_check_var.get() == 1:
                self.placer.is_auto_correct_enabled = True
            else:
                self.placer.is_auto_correct_enabled = False
            if self.multi_selected_var.get() == 1:
                self.placer.in_multiple_selection = True
                self.list_box_multi.place(x=500 + (self.second_win.winfo_width()//2), y=38)

                if len(self.temp_multi_selection) != len(self.placer.selected_multi_list):
                    print(self.placer.selected_multi_list,"***",self.temp_multi_selection)
                    self.temp_multi_selection = list(self.placer.selected_multi_list)

                    self.list_box_multi.delete(0, tk.END)
                    for i, w in enumerate(self.temp_multi_selection):
                        content=f"\n{w.name} type {type(w.widget).__name__}"
                        self.list_box_multi.insert(i,content)
            else:

                self.list_box_multi.place_forget()
                self.placer.in_multiple_selection = False

                selected = self.list_box.get(tk.ANCHOR)
                wid = self.placer.get_widget(self.placer.choosen_name)
                if self.placer.choosen is None and self.placer.choosen_name is None:
                    continue
                if not selected:
                    if not wid:
                        continue
                    self.select_widget(wid)
                    continue

                if self.placer.choosen_name != selected:
                    if not self.placer.force_select:
                        print("moshe")
                        self.placer.choosen_name = selected
                        self.placer.choosen = self.placer.get_widget(selected).widget

                        self.update_top_bar()
                        pos = f"   (x = {self.placer.choosen.winfo_x()},y = {self.placer.choosen.winfo_y()})"

                    else:
                        self.select_widget(wid)

                if pos:
                    pos = f"   (x = {self.placer.choosen.winfo_x()},y = {self.placer.choosen.winfo_y()})"

                self.txt_choosen_name.config(text=f"Var Name: {self.placer.choosen_name} "
                                                  f" type: {type(self.placer.choosen).__name__}  position: {pos}")

    def duplicate_widget(self):
        self.placer.duplicate()
        self.list_box.insert(tk.END, self.placer.choosen_name)

    def add(self, type_):
        name = self.w_entry_name.get()
        if not name:
            name = f"_{self.placer.amounts}"
        p = self.w_entry_set_parent.get()
        self.placer.add_widget(type_, name,parent=p if p else None)
        self.list_box.insert(tk.END, self.placer.choosen_name)

    def show_widgets_layer(self, e):
        self.w_name_label.config(text="Variable:")
        self.w_label_canvas.config(width=20, height=2, bg="red")
        self.w_canvas.config(width=500, height=500)
        self.w_label_canvas.config(text="")
        self.w_btn.place(x=70, y=20)
        self.w_label.place(x=20, y=20)
        self.w_entry.place(x=120, y=20)
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


    def save(self):
        self.gui.builder.bg = self.bg_entry.get()
        self.gui.builder.build(*self.placer.widgets.values())


class GUI:
    def __init__(self, win):
        win.geometry("500x500")
        self.temp = None
        self.img = tk.PhotoImage(file="bg.png")
        self.bg_image = tk.Label(win, image=self.img)
        self.bg_image.image = self.img
        self.bg_image.place(x=0, y=0)
        self.screen = StartScreen(win, self)
        win.resizable(False,False)
        self.builder = None

    def add_builder(self, name, size):
        self.builder = Builder(name, size)

    def move_to_editor(self, h, w):
        self.screen.destroy()
        self.bg_image = tk.Label(self.screen.win, image=self.img)
        self.bg_image.image = self.img
        self.bg_image.place(x=0, y=0)
        if int(h) + 450 < 500:
            h = 500
        if int(w) + 400 < 800:
            w = 800
        self.screen.win.geometry(f"{int(w) + 400}x{int(h) + 450}")
        self.temp = RenderEditor(self.screen.win, self, int(h), int(w))


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
