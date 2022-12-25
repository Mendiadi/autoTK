import tkinter as tk

import threading

from autoTK.widgets.w_base import WTypes, WBase


from autoTK.utils.common_types import Parent
from autoTK.editor.scrolled import ScrolledWin

class RenderWindow:
    def __init__(self, root,h,w):

        self.hook_scroll = False
        self.handlers = {}
        self.win = root

        if self.hook_scroll:
            self.scrolled = ScrolledWin(root,h,w)
            self.root = self.scrolled.hook()
            print("*"*100)
        else:
            self.root = tk.Frame(self.win, height=h, width=w, bg="white")
            self.root.pack(pady=50)

        self.root.pack_propagate(False)
        self.root.bind('<Motion>', self.motion)
        self.root.bind("<ButtonPress-1>", lambda event: self.capture(True))
        self.root.bind("<ButtonRelease-1>", lambda event: self.capture(False))
        self.capture(False)
        self.do_capture = False
        self.choosen = None
        self.choosen_name = None
        self.widgets = {}
        self.amounts = 0
        self.memorize_detect = set()
        self.in_motion = False
        self.selected_multi_list = set()
        self.is_auto_correct_enabled = False



    def get_widget(self, name):
        wid = self.widgets.get(name, None)
        return wid


    def config_parent(self, parent):
        if parent:
            par_wid = self.widgets.get(parent, None)
            if not par_wid:
                parent__ = Parent(self.root, "self.win")
            else:
                parent__ = Parent(par_wid.widget, f"self.{parent}")
                print(par_wid.__dict__, "$" * 200)
        else:
            parent__ = Parent(self.root, "self.win")
        return parent__

    def add_handler(self, name, func):
        if name not in self.handlers:
            self.handlers[name] = func

    def add_widget(self, widget: WBase, name, parent=None):
        parent__ = self.config_parent(parent)
        if name in self.widgets:
            name = f"{name}_{self.amounts}"
        new_widget = widget.create_widget(name, parent__, self.set_choosen)
        new_widget.update()

        self.widgets[new_widget.name] = new_widget
        self.set_choosen(new_widget)
        new_widget.index = self.amounts
        self.amounts += 1

    def update_widget(self,e, value,h=None,w_=None):
        w = self.widgets[self.choosen_name]
        if not value():
            return
        if w.type.value == WTypes.OVAL.value:
            w.bg = value()
            print(h,w_)

            self.choosen.delete(w.shape)
            w.shape = self.choosen.create_oval(0, 0,
                                     w_ if w_ else w.conf.options['width'],
                                     h if h else w.conf.options['height'],
                                     fill=w.bg,tags=("oval",))
        if w.type.value == WTypes.LABEL.value or w.type.value == WTypes.BUTTON.value:
            #todo fix images
            op = w.conf.options.get("image",None)
            print(value(),str(op),type(op),type(value()),"*"*100)
            if op:
                if str(op) == value():
                    print("not need to update")
                    return
            try:
                img = tk.PhotoImage(file=value(),name=value())
                w.set_conf(image=img)
            except tk.TclError:
                pass

            w.update()

    def set_choosen(self, wid):
        if not wid:
            self.choosen = None
            self.choosen_name = None
        else:
            self.force_select = True
            self.choosen = wid.widget
            self.choosen_name = wid.name
            self.memorize_detect.clear()
            self.handlers["select"](wid)

        self.handlers["top_bar"]()

    def delete_selected(self, list_box):
        w = self.widgets.get(self.choosen_name, None)
        if not w:
            return
        self.choosen.destroy()
        self.widgets.pop(w.name, 0)
        self.amounts -= 1
        list_box.delete(0, tk.END)
        for i, widget in enumerate(self.widgets.values()):
            widget.index = i
            list_box.insert(i, widget.name)
        if len(self.widgets):
            first_wid = list(self.widgets.values())[0]
            print(first_wid.name, self.widgets, "^" * 100)
        else:
            first_wid = None
        self.set_choosen(first_wid)

    def motion(self, event):

        if self.do_capture and self.choosen:

            self.in_motion = True
            x, y = event.x, event.y
            self.choosen.place_configure(x=x, y=y)

            if self.is_auto_correct_enabled:
                self.detect_horizontal_points()
                self.detect_vertical_points()

            if self.handlers and self.choosen:
                self.handlers["update"](self.get_widget(self.choosen_name))




    def detect_vertical_points(self):
        canvases = []

        def clear(w):
            [c_.destroy() for c_ in canvases]
            self.choosen.place_configure(y=w.widget.winfo_y())
            canvases.clear()

        src_ = self.choosen.winfo_y()
        if not self.choosen:
            return
        for name, w in self.widgets.items():
            if len(canvases) > 1:
                break

            if self.choosen_name != name:

                if (src_ == w.widget.winfo_y() or src_ - 1 == w.widget.winfo_y() - 1
                    or src_ + 1 == w.widget.winfo_y() + 1
                ) and (self.choosen, w) not in self.memorize_detect:

                    c = tk.Canvas(self.root, width=abs(w.widget.winfo_x() - self.choosen.winfo_x()) + 5, height=0.1)

                    canvases.append(c)
                    print("&" * 500)
                    if w.widget.winfo_x() < self.choosen.winfo_x():
                        c.place(x=w.widget.winfo_x(), y=w.widget.winfo_y())
                    else:
                        c.place(y=src_, x=self.choosen.winfo_x())
                    self.memorize_detect.add((self.choosen, w))
                    threading.Timer(0.5, lambda: clear(w)).start()

                    break

    def detect_horizontal_points(self):
        canvases = []

        def clear(w):
            [c_.destroy() for c_ in canvases]
            if not self.in_motion:
                self.choosen.place_configure(x=w.widget.winfo_x())
            canvases.clear()

        src_ = self.choosen.winfo_x()
        if not self.choosen:
            return
        for name, w in self.widgets.items():
            if len(canvases) > 1:
                break
            if self.choosen_name != name:
                if (src_ == w.widget.winfo_x() or src_ - 1 == w.widget.winfo_x() - 1
                    or src_ + 1 == w.widget.winfo_x() + 1
                ) and (self.choosen, w) not in self.memorize_detect:
                    c = tk.Canvas(self.root, width=0.1, height=abs(w.widget.winfo_y() - self.choosen.winfo_y()) + 5)
                    canvases.append(c)
                    if w.widget.winfo_y() < self.choosen.winfo_y():
                        c.place(x=w.widget.winfo_x(), y=w.widget.winfo_y())
                    else:
                        c.place(x=src_, y=self.choosen.winfo_y())
                    self.memorize_detect.add((self.choosen, w))
                    threading.Timer(0.5, lambda: clear(w)).start()
                    break

    def duplicate(self):

        temp = self.choosen_name
        if not temp:
            return
        name = self.choosen_name + str(self.amounts)

        w = self.widgets[self.choosen_name]

        self.add_widget(type(w),
                        name, w.parent.name.replace("self.", ""))
        new_w = self.get_widget(name)
        new_w.set_conf(**self.widgets[temp].conf.options)
        new_w.conf._font = list(w.conf._font)
        new_w.update()
        self.handlers["select"](new_w)

    def redo(self,name, x, y,conf):
        w = self.get_widget(name)
        if not w:
            return

        w.conf = conf
        w.update()
        print(w.conf.__dict__)
        if name != self.choosen_name:
            self.set_choosen(w)
        self.choosen.place_configure(x=x,y=y)


    def capture(self, flag):
        self.do_capture = flag
        if not flag:
            self.force_select = False
        else:
            func = self.handlers.get("redo",0)
            if func:
                func()
        self.in_motion = False
