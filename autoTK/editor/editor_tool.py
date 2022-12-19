import tkinter as tk
from tkinter import filedialog, messagebox



from autoTK.editor.renderwindow import RenderWindow
from autoTK.editor.widget_layer import WidgetLayer
from autoTK.utils.common_types import Screen
from autoTK.editor.top_bar import TopBar

class RenderEditor(Screen):
    def __init__(self, win, gui, height, width):
        super().__init__(win, gui)
        # master window
        self.win = win

        self.top_bar = TopBar(self.win, self)
        # actual rendering window
        self.widget_layer = WidgetLayer(self.win, self)
        self.menu_bar = tk.Menu(self.win,title="menu")
        self.win.config(menu=self.menu_bar)

        fileMenu = tk.Menu(self.menu_bar,bg="lightblue")
        self.menu_bar.add_cascade(label="Project", menu=fileMenu)

        editMenu =  tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="View", menu=editMenu)

        fileMenu.add_command(label="New Project",command=self.gui.new_project)
        fileMenu.add_command(label="Export", command=self.save)
        fileMenu.add_command(label="Exit", command=self.gui.exit)



        self.placer = RenderWindow(self.win,height,width)
        self.placer.add_handler("update", self.top_bar.update)
        self.placer.add_handler("select", self.select_widget)
        self.placer.add_handler("top_bar", self.handle_top_bar)


        # widgets layer
        self.bg_label_info = tk.Label(self.win,text="BG COLOR: ",font="none 12 bold",bg="lightblue")
        self.bg_label_info.place(x=5,y=50)
        self.bg_entry = tk.Entry(self.win,width=8,font="none 10 bold",bg="lightblue")
        self.bg_entry.place(x=20, y=80)
        self.bg_entry.insert(0, "white")
        self.bg_entry.bind("<Leave>", lambda e: self.placer.root.config(bg=self.bg_entry.get()))
        # top bar
        self.enable_auto_correct_check_var = tk.IntVar()
        self.enable_auto_correct_check_btn = tk.Checkbutton(self.win,
                                                            text="Enable Auto Correct",font="none 10 bold",
                                                            variable=self.enable_auto_correct_check_var,
                                                            offvalue=0, onvalue=1,
                                                            bg="lightblue", border=0, activebackground="lightblue",
                                                            command=self.enable_auto_correct)
        self.enable_scrolled_check_var = tk.IntVar()
        self.enable_scrolled_check_btn = tk.Checkbutton(self.win,
                                                            text="Enable Scroll", font="none 10 bold",
                                                            variable=self.enable_scrolled_check_var,
                                                            offvalue=0, onvalue=1,
                                                            bg="lightblue", border=0, activebackground="lightblue",
                                                            command=self.enable_scrolled)
        self.label_project_name = tk.Label(self.win,text=f"Project: {self.gui.builder.name}",
                                           font="none 10 bold")
        self.label_project_name.place(x=0,y=0)
        # list box
        self.list_box = tk.Listbox(self.win,bg="lightblue",font="none 10 bold")
        self.list_box.place(x=10, y=300)
        self.list_box_multi = tk.Listbox(self.win, bg="lightblue", height=9, font="none 10 bold")
        self.duplicate_btn = tk.Button(self.win, text="clone", command=self.duplicate_widget,
                                    bg = "lightblue", font = "none 10 bold",
                                   border = 0, activebackground = "lightgreen",
        )
        self.duplicate_btn.place(x=770, y=80)
        self.button_del_wid = tk.Button(self.win, text="DELETE",bg="lightblue",font="none 10 bold",
                                        border=0,activebackground="lightgreen",
                                        command=lambda: self.placer.delete_selected(self.list_box))
        self.button_del_wid.place(x=770, y=50)
        # tools



        self.active = True
        self.list_box.bind("<Motion>", lambda x: self.handle_choose_from_list_box())
        self.in_updating_options = False
        self.temp_values = None
        self.enable_scrolled_check_btn.place(x=0,y=120)
        self.enable_auto_correct_check_btn.place(x=0, y=150)

    def enable_scrolled(self):
        self.placer.hook_scroll = bool(self.enable_scrolled_check_var.get())

    def enable_auto_correct(self):

        self.placer.is_auto_correct_enabled = bool(self.enable_auto_correct_check_var.get())

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
        name = self.widget_layer.w_entry_name.get()
        if not name or name in self.placer.widgets:
            name = f"var_{self.placer.amounts}"

        p = self.widget_layer.w_entry_set_parent.get()
        if p not in self.placer.widgets:
            p = None
        self.placer.add_widget(type_, name, parent=p if p else None)
        self.list_box.insert(tk.END, self.placer.choosen_name)



    def save(self):
        dir = filedialog.askdirectory(title="Select Folder to Save the Project")
        self.gui.builder.bg = self.bg_entry.get()
        self.gui.builder.build(dir,*self.placer.widgets.values())
        messagebox.showinfo(title="SUCCESS",message=f"Your Project has Saved in {dir}.")


