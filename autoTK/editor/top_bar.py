import tkinter as tk
import functools


from autoTK.widgets.w_base import WTypes, WBase


class TopBar:
    def __init__(self, root, editor):
        self.labels_supported = {}
        self.editor = editor
        self.root = root
        self.top_bar = tk.Canvas(self.root, height=170, width=600, bg="lightblue")
        self.txt_choosen_name = tk.Label(self.top_bar, font="none 15 bold", bg="lightblue")
        self.txt_choosen_pos = tk.Label(self.top_bar, font="none 15 bold", bg="lightblue")
        self.options_entries = {}
        self.set_x_entry = tk.Entry(self.top_bar, width=4, bg="lightblue", font="none 8 bold")
        self.set_y_entry = tk.Entry(self.top_bar, width=4, bg="lightblue", font="none 8 bold")
        self.set_y_entry.bind("<Leave>", lambda x: self.editor.placer.choosen.place(y=int(self.set_y_entry.get())))
        self.set_x_entry.bind("<Leave>", lambda x: self.editor.placer.choosen.place(x=int(self.set_x_entry.get())))
        self.duplicate_btn = tk.Button(self.top_bar, text="clone", command=self.editor.duplicate_widget)
        self.duplicate_btn.place(x=450, y=80)

        self.enable_auto_correct_check_var = tk.IntVar()
        self.enable_auto_correct_check_btn = tk.Checkbutton(self.top_bar,
                                                            text="enable auto correct",
                                                            variable=self.enable_auto_correct_check_var,
                                                            offvalue=0, onvalue=1,
                                                            bg="lightblue", border=0, activebackground="lightblue",
                                                            command=self.enable_auto_correct)
        self.add_onclick_template_var = tk.IntVar()
        self.add_onclick_template_btn = tk.Checkbutton(self.top_bar,
                                                       text="add onclick template",
                                                       variable=self.add_onclick_template_var,
                                                       offvalue=0, onvalue=1,
                                                       bg="lightblue", border=0, activebackground="lightblue",
                                                       command=self.onclick_check_button)

        self.change_name_var_entry = tk.Entry(self.top_bar, width=10, bg="lightblue", font="none 8 bold")
        self.change_name_var_entry.bind("<Leave>", lambda x: self.change_var_name())
        self.top_bar.pack()
        self.hide()

    def change_var_name(self):
        name = self.editor.placer.choosen_name
        txt = self.change_name_var_entry.get().replace(" ", "_")

        if txt and txt != " " and txt[0].isalpha() and txt not in self.editor.placer.widgets:

            wid = self.editor.placer.widgets.pop(name, None)
            if not wid:
                return

            wid.name = txt
            self.editor.placer.widgets[txt] = wid
            self.editor.list_box.delete(wid.index, wid.index)
            self.editor.list_box.insert(wid.index, txt)
            self.change_name_var_entry.delete(0, tk.END)
            self.change_name_var_entry.insert(0, wid.name)
            self.editor.placer.set_choosen(wid)

    def generate_content(self, options):
        if self.options_entries:
            [e.destroy() for e in self.options_entries.values()]
            [e.destroy() for e in self.labels_supported.values()]
            self.options_entries.clear()
        for i, supported in enumerate(options.supported):
            l = tk.Label(self.top_bar, text=supported, bg="lightblue", font="none 12 bold")

            e = tk.Entry(self.top_bar, width=10, bg="deepskyblue", border=0, font="none 10 bold")
            if options.type.value == WTypes.OVAL.value:

                update_fn = lambda x: self.editor.placer.update_widget(e.get())
            else:
                update_fn = functools.partial(self.update_widget_options, supported=supported, entry=e)
            if options.type.value == WTypes.BUTTON.value:

                if options.onclick_template:
                    self.add_onclick_template_btn.select()
                else:
                    self.add_onclick_template_btn.deselect()
                self.add_onclick_template_btn.place(x=10, y=130)
            else:
                self.add_onclick_template_btn.place_forget()
            e.bind("<Leave>", update_fn)

            l.place(x=(i * 100) + 5, y=15)
            e.place(x=(i * 100) + 5, y=50)
            self.options_entries[supported] = e
            self.labels_supported[supported] = l

    def show(self):
        self.top_bar.config(height=170)
        self.txt_choosen_pos.place(x=440, y=150)
        self.txt_choosen_name.place(x=0, y=150)
        self.set_x_entry.place(x=490, y=155)
        self.set_y_entry.place(x=567, y=155)
        self.enable_auto_correct_check_btn.place(x=50, y=90)
        self.change_name_var_entry.place(x=88, y=155)

    def hide(self):
        self.txt_choosen_pos.place_forget()
        self.txt_choosen_name.place_forget()
        self.set_x_entry.place_forget()
        self.set_y_entry.place_forget()
        self.enable_auto_correct_check_btn.place_forget()
        self.change_name_var_entry.place_forget()

        self.top_bar.config(height=10)

    def update(self, widget: WBase):
        if self.editor.in_updating_options:
            return

        temp = dict(widget.conf.options)
        for option, value in temp.items():
            e = self.options_entries[option]
            e.delete(0, tk.END)
            e.insert(0, value)
        x, y = widget.widget.winfo_x(), widget.widget.winfo_y()
        self.set_x_entry.delete(0, tk.END)
        self.set_y_entry.delete(0, tk.END)
        self.set_x_entry.insert(0, x)
        self.set_y_entry.insert(0, y)
        self.change_name_var_entry.delete(0, tk.END)
        self.change_name_var_entry.insert(0, self.editor.placer.choosen_name)
        self.txt_choosen_name.config(text=f"Variable:            "
                                          f"Type: {type(self.editor.placer.choosen).__name__}")
        self.txt_choosen_pos.config(text="( X =     ,  Y =     )")

    def update_widget_options(self, e, entry, supported):
        if self.editor.placer.amounts < 1:
            return
        self.editor.in_updating_options = True
        wid = self.editor.placer.get_widget(self.editor.placer.choosen_name)
        wid.conf.options[supported] = entry.get()
        wid.update()
        self.editor.in_updating_options = False

    def onclick_check_button(self):
        w = self.editor.placer.get_widget(self.editor.placer.choosen_name)
        w.onclick_template = bool(self.add_onclick_template_var.get())

    def enable_auto_correct(self):

        self.editor.placer.is_auto_correct_enabled = bool(self.enable_auto_correct_check_var.get())



