import tkinter
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



        self.add_onclick_template_var = tk.IntVar()
        self.add_onclick_template_btn = tk.Checkbutton(self.top_bar,font="none 10 bold",
                                                       text="Add onclick Template",
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
        from tkinter import font
        if self.options_entries:
            [e.destroy() for e in self.options_entries.values()]
            [e.destroy() for e in self.labels_supported.values()]
            self.options_entries.clear()
        i2 = 0
        for i, supported in enumerate(options.supported):
            if supported == "font":
                continue
            l = tk.Label(self.top_bar, text=supported, bg="lightblue", font="none 12 bold")
            if supported == "font type":
                e = tk.Listbox(self.top_bar,height=4,bd=1,bg="lightblue")
                for i, f in enumerate(font.families()):
                    e.insert(i, f)


                # e.bind("<Enter>", lambda x: print(e.selection_get()))

            else:
                e = tk.Entry(self.top_bar, width=10, bg="deepskyblue", border=0, font="none 10 bold")
            if options.type.value == WTypes.OVAL.value and supported == "inner color":

                update_fn = lambda x: self.editor.placer.update_widget(x,e.get)

            else:
                if supported == "image":
                    update_fn = functools.partial(self.editor.placer.update_widget,value=e.get)
                else:
                    update_fn = functools.partial(self.update_widget_options, supported=supported, entry=e,
                                              key="font type" if supported == "font type" else None)

            print(supported)
            if options.type.value == WTypes.BUTTON.value or options.type.value == WTypes.CHECKBUTTON.value:

                if options.onclick_template:
                    self.add_onclick_template_btn.select()
                else:
                    self.add_onclick_template_btn.deselect()
                self.add_onclick_template_btn.place(x=10, y=130)
            else:
                self.add_onclick_template_btn.place_forget()
            e.bind("<Leave>", update_fn)
            if i < 6:
                l.place(x=(i * 100) + 5, y=5)
                e.place(x=(i * 100) + 5, y=30)
            else:

                l.place(x=(i2 * 100) + 5, y=50)
                e.place(x=(i2 * 100) + 5, y=75)
                i2 += 1
            self.options_entries[supported] = e
            self.labels_supported[supported] = l

    def show(self):
        self.top_bar.config(height=170)
        self.txt_choosen_pos.place(x=440, y=150)
        self.txt_choosen_name.place(x=0, y=150)
        self.set_x_entry.place(x=490, y=155)
        self.set_y_entry.place(x=567, y=155)

        self.change_name_var_entry.place(x=88, y=155)

    def hide(self):
        self.txt_choosen_pos.place_forget()
        self.txt_choosen_name.place_forget()
        self.set_x_entry.place_forget()
        self.set_y_entry.place_forget()
        self.txt_choosen_name.place_forget()
        self.txt_choosen_pos.place_forget()
        self.change_name_var_entry.place_forget()

        self.top_bar.config(height=10)

    def update(self, widget: WBase):
        if self.editor.in_updating_options:
            return

        temp = dict(widget.conf.options)
        for option, value in temp.items():
            e = self.options_entries.get(option,None)
            if not e:
                continue

            else:
                e.delete(0, tk.END)
                e.insert(0, value)
        if "font" in widget.supported:

            font_conf = ("","font size","font style")
            for i,f in enumerate(widget.conf._font):
                if i == 0:
                    continue

                e = self.options_entries[font_conf[i]]
                e.delete(0,tk.END)
                e.insert(0,f)
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

    def update_widget_options(self, e, entry, supported,key=None):
        from tkinter import font
        if self.editor.placer.amounts < 1:
            return

        self.editor.in_updating_options = True
        wid: WBase = self.editor.placer.get_widget(self.editor.placer.choosen_name)
        op = wid.conf.options.get(supported, None)

        if op:
            if op == entry.get():
                print("not need to update")
                return
        print(entry, supported, key)
        if key:
            print(entry, supported, key)
            try:
                if entry.selection_get() in font.families():
                    value = entry.selection_get()
            except tkinter.TclError:
                return

        else:
            value = entry.get()
        wid.update_widget_option(value, supported)
        self.editor.in_updating_options = False

    def onclick_check_button(self):
        w = self.editor.placer.get_widget(self.editor.placer.choosen_name)
        w.onclick_template = bool(self.add_onclick_template_var.get())




