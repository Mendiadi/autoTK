import tkinter as tk

import threading

from autoTK.w_base import WTypes, WBase



class Parent:
    def __init__(self, p, n):
        self.parent = p
        self.name = n


class Placer:
    def __init__(self, root):
        self.handlers = {}
        self.root = root
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

    def update_widget(self, value):
        w = self.widgets[self.choosen_name]
        if w.type.value == WTypes.OVAL.value:
            w.bg = value
            self.choosen.create_oval(0, 0,
                                     w.conf.options['width'],
                                     w.conf.options['height'],
                                     fill=w.bg)

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

        print(self.handlers)

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
        name = self.choosen_name + str(self.amounts)
        w = self.widgets[self.choosen_name]
        self.add_widget(type(w),
                        name, w.parent.name.replace("self.", ""))
        new_w = self.get_widget(name)
        new_w.set_conf(**self.widgets[temp].conf.options)
        new_w.update()
        self.handlers["select"](new_w)

    def capture(self, flag):
        self.do_capture = flag
        if not flag:
            self.force_select = False

        self.in_motion = False
