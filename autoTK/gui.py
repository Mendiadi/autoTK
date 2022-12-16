import threading
import time
import tkinter as tk

from autoTK.options import Options
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
    def __init__(self, win, gui):
        super().__init__(win, gui)
        self.headline = tk.Label(self.win, text="WELCOME TO TKINTER DESIGNER", font="none 20 bold")
        self.canvas = tk.Canvas(self.win, width=100, height=100, bg="lightblue", border=0)

        self.canvas.bind("<Enter>", self.canvas_enter)
        self.canvas.bind("<Leave>", self.canvas_leave)
        self.create_btn = tk.Button(self.canvas, text="create", command=self._create)
        self.entry_name = tk.Entry(self.canvas, width=30)
        self.label_on_canvas = tk.Label(self.canvas, text="NEW")
        self.label_info = tk.Label(self.canvas, text="Enter file name:", bg="lightblue")
        self.headline.pack()
        self.canvas.pack(pady=100)
        self.label_on_canvas.pack(pady=5)

    def _create(self):
        self.gui.add_builder(self.entry_name.get())

        self.gui.move_to_editor()

    def canvas_enter(self, e):
        self.canvas.config(width=1000, height=1000, bg="lightblue", border=0)

        self.label_on_canvas.config(bg="lightblue", width=100)
        self.label_info.pack(pady=20)
        self.entry_name.pack(pady=20)
        self.create_btn.pack(pady=20)

    def canvas_leave(self, e):
        self.label_on_canvas.config(bg="white", width=3)
        self.canvas.config(width=100, height=100)

        self.label_info.forget()
        self.create_btn.forget()
        self.entry_name.forget()


class RenderEditor(Screen):
    def __init__(self, win, gui):
        super().__init__(win, gui)
        # master window
        self.win = win

        # actual rendering window
        self.second_win = tk.Frame(self.win, height=500, width=500, bg="grey")

        self.second_win.pack_propagate(False)
        self.placer = Placer(self.second_win)
        # widgets layer
        self.w_canvas = tk.Canvas(self.win, width=50, height=50, bg="red")

        self.w_canvas.bind("<Enter>", self.show_widgets_layer)
        self.w_canvas.bind("<Leave>", self.hide_widgets_layer)
        self.w_label_canvas = tk.Label(self.w_canvas, text="+", font="none 20 bold", width=1, height=1, bg="red")
        self.w_entry_name = tk.Entry(self.w_canvas, width=20)
        self.w_btn = tk.Button(self.w_canvas, text="button", command=lambda: self.add(WTypes.BUTTON))
        self.w_label = tk.Button(self.w_canvas, text="label", command=lambda: self.add(WTypes.LABEL))
        self.w_canvas.pack()
        self.w_label_canvas.pack()

        tk.Button(self.win, text="save",
                  command=self.save).place(x=50, y=30)

        # top bar
        self.top_bar = tk.Canvas(self.win, height=150, width=600, bg="lightblue")
        self.txt_choosen_name = tk.Label(self.top_bar)
        self.options_entries = {}
        import functools

        for i, supported in enumerate(Options().supported):
            tk.Label(self.top_bar, text=supported, bg="lightblue").place(x=i * 100, y=15)

            e = tk.Entry(self.top_bar, width=10)
            update_fn = functools.partial(self.update_widget_options, supported=supported,entry=e)
            e.bind("<Leave>", update_fn)
            print("%" * 50, supported)

            e.place(x=i * 100, y=30)
            self.options_entries[supported] = e
        self.txt_choosen_name.place(x=300, y=0)

        # list box
        self.list_box = tk.Listbox(self.win)
        self.list_box.place(x=10, y=300)

        # tools
        self.top_bar.pack()
        self.second_win.pack(pady=50)
        self.active = True
        threading.Thread(target=self._thread_update_chosen, daemon=True).start()
        self.in_updating_options = False
        self.temp_values = None

    def update_widget_options(self,e,entry,supported):
        print("moshe")
        if self.placer.amounts < 1:
            return
        self.in_updating_options = True
        wid = self.placer.get_widget(self.placer.choosen_name)
        wid.conf.options[supported] = entry.get()
        print(wid.conf.options,supported)
        wid.update()
        self.in_updating_options = False

    def update_top_bar(self):
        if self.in_updating_options:
            return
        op = self.placer.get_widget(self.placer.choosen_name).conf.options
        temp = dict(op)
        for entry in self.options_entries.values():
            entry.delete(0,tk.END)
        for option,value in temp.items():

            e = self.options_entries[option]
            e.insert(0,value)


    def select_widget(self,wid):
        self.list_box.selection_clear(0, tk.END)
        self.list_box.select_set(wid.index)
        self.list_box.select_anchor(wid.index)
        self.update_top_bar()

    def _thread_update_chosen(self):
        while self.active:
            time.sleep(0.5)
            selected = self.list_box.get(tk.ANCHOR)
            wid = self.placer.get_widget(self.placer.choosen_name)
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
                else:
                    self.select_widget(wid)

            self.txt_choosen_name.config(text=self.placer.choosen_name)





    def add(self, type_):
        self.placer.add_widget(type_, self.w_entry_name.get())
        self.list_box.insert(tk.END, self.placer.choosen_name)

    def show_widgets_layer(self, e):
        self.w_label_canvas.config(width=20, height=2, bg="red")
        self.w_canvas.config(width=500, height=500)
        self.w_btn.place(x=70, y=20)
        self.w_label.place(x=20, y=20)
        self.w_entry_name.place(x=70, y=0)

    def hide_widgets_layer(self, e):
        self.w_label_canvas.config(width=1, height=1)
        self.w_canvas.config(width=1, height=1)
        self.w_btn.forget()
        self.w_entry_name.delete(0,tk.END)
        self.w_entry_name.forget()


    def save(self):
        self.gui.builder.build(*self.placer.widgets.values())


class GUI:
    def __init__(self, win):
        win.geometry("1000x1000")
        self.temp = None
        self.screen = StartScreen(win, self)

        self.builder = None

    def add_builder(self, name):
        self.builder = Builder(name)

    def move_to_editor(self):
        self.screen.destroy()
        self.temp = RenderEditor(self.screen.win, self)


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)

    root.mainloop()
