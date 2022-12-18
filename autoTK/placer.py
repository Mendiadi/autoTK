import tkinter as tk

import threading

from autoTK.w_base import WTypes
from autoTK.w_button import WButton
from autoTK.w_canvas import WCanvas
from autoTK.w_entry import WEntry
from autoTK.w_label import WLabel


class Parent:
    def __init__(self, p, n):
        self.parent = p
        self.name = n


class Placer:
    def __init__(self, root):
        self.root = root
        self.root.bind('<Motion>', self.motion)
        self.root.bind("<ButtonPress-1>", lambda event: self.capture(True))
        self.root.bind("<ButtonRelease-1>", lambda event: self.capture(False))
        self.capture(False)
        self.do_capture = False
        self.choosen = None
        self.choosen_name = None
        self.widgets = {}
        self.force_select = False
        self.amounts = 0
        self.memorize_detect = set()
        self.in_motion = False
        self.in_multiple_selection = False
        self.selected_multi_list = set()
        self.is_auto_correct_enabled = False

    def get_widget(self, name):
        wid = self.widgets.get(name, None)
        return wid

    def add_widget(self, type_, name, parent=None):
        if parent:
            par_wid = self.widgets.get(parent,None)
            if not par_wid:
                parent__ = Parent(self.root, "self.win")
            else:
                parent__ = Parent(par_wid.widget, f"self.{parent}")
            print(par_wid.__dict__,"$"*200)
        else:
            parent__ = Parent(self.root, "self.win")

        if name in self.widgets:
            name = f"{name}_{self.amounts}"
        if type_.value == WTypes.LABEL.value:
            wid = tk.Label(parent__.parent)
            wid.pack()
            w = WLabel.create_widget(name,
                                     parent__.name, wid, self.set_choosen)
            w.set_conf(text="sample")
        elif type_.value == WTypes.BUTTON.value:
            wid = tk.Button(parent__.parent)
            wid.pack()
            w = WButton.create_widget(name,
                                      parent__.name, wid, self.set_choosen)
            w.set_conf(text="sample")
        elif type_.value == WTypes.ENTRY.value:
            wid = tk.Entry(parent__.parent)
            wid.pack()
            w = WEntry.create_widget(name, parent__.name, wid, self.set_choosen)
            w.set_conf()
        elif type_.value == WTypes.CANVAS.value:
            wid = tk.Canvas(parent__.parent)
            wid.pack_propagate(False)
            wid.pack()
            w = WCanvas.create_widget(name, parent__.name, wid, self.set_choosen)
            w.set_conf()

        w.update()

        self.choosen_name = w.name
        self.widgets[w.name] = w
        w.index = self.amounts
        self.amounts += 1

    def set_choosen(self, wid):
        if not self.in_multiple_selection:
            self.force_select = True
            self.choosen = wid.widget
            self.choosen_name = wid.name
            self.memorize_detect.clear()
        else:
            self.selected_multi_list.add(wid)

    def delete_selected(self, list_box, m_list_box):
        if self.in_multiple_selection:
            for w in self.selected_multi_list:
                w.widget.destroy()
                self.widgets.pop(w.name, 0)
                self.amounts -= 1
            m_list_box.delete(0, tk.END)
            self.selected_multi_list.clear()
        else:
            w = self.widgets.get(self.choosen_name, None)
            if not w:
                return
            self.choosen.destroy()
            self.widgets.pop(w.name, 0)
            self.amounts -= 1
        list_box.delete(0, tk.END)
        for i, widget in enumerate(self.widgets.values()):
            list_box.insert(i, widget.name)
        if len(self.widgets):
            first_wid = list(self.widgets.values())[0]
            print(first_wid.name,self.widgets,"^"*100)
        else:
            first_wid = None
        self.choosen = first_wid.widget
        self.choosen_name = first_wid.name if first_wid else None

    def motion(self, event):
        if self.do_capture and self.choosen:
            self.in_motion = True
            x, y = event.x, event.y
            self.choosen.place_configure(x=x, y=y)
            if not self.in_multiple_selection:
                if self.is_auto_correct_enabled:
                    self.detect_horizontal_points()
                    self.detect_vertical_points()
            else:
                if not self.selected_multi_list:
                    return

        print(threading.activeCount(), len(self.selected_multi_list))

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
                    print("&" * 500)
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
        print(self.widgets[self.choosen_name].type,"@"*100)
        self.add_widget(self.widgets[self.choosen_name].type,
                        name,self.widgets[self.choosen_name].parent.replace("self.",""))
        self.widgets[name].set_conf(**self.widgets[temp].conf.options)
        print(self.widgets[name].__dict__, "*" * 200)
        self.widgets[name].update()

    def capture(self, flag):
        self.do_capture = flag
        if not flag:
            self.force_select = False

        self.in_motion = False
