import tkinter as tk


from autoTK.utils.common_types import Screen


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
        self.headline = tk.Label(self.win, text="WELCOME TO TKINTER DESIGNER", font="none 20 bold", bg="lightblue")
        self.canvas = tk.Canvas(self.win, width=100, height=100, bg="lightblue", border=0)
        self.content_label = tk.Label(self.win, text=self.content, bg="lightblue", font="none 10 bold")
        self.canvas.bind("<Enter>", self.canvas_enter)
        self.canvas.bind("<Leave>", self.canvas_leave)
        self.create_btn = tk.Button(self.canvas, text="Create New Window", command=self._create,
                                    border=0, font="none 10 bold", bg="deepskyblue2")
        self.entry_name = tk.Entry(self.canvas, width=15, border=0, bg="deepskyblue2", font="none 10 bold")

        self.label_on_canvas = tk.Label(self.canvas, text="NEW", bg="lightblue")
        self.label_info = tk.Label(self.canvas, text="Enter Project name:", bg="lightblue")
        self.entry_width = tk.Entry(self.canvas, width=10, border=0, bg="deepskyblue2", font="none 10 bold")
        self.label_info_width = tk.Label(self.canvas, text="WIDTH: ", bg="lightblue")
        self.entry_height = tk.Entry(self.canvas, width=10, border=0, bg="deepskyblue2", font="none 10 bold")
        self.label_info_height = tk.Label(self.canvas, text="HEIGHT: ", bg="lightblue")
        self.headline.pack()
        self.canvas.pack(pady=100)
        self.label_on_canvas.pack(pady=5)
        self.content_label.pack(pady=5)
        self.entry_height.insert(0, "500")
        self.entry_width.insert(0, "500")

    def _create(self):
        height, width = self.entry_height.get(), self.entry_width.get()
        self.gui.add_provider(self.entry_name.get(), f"{width}x{height}")
        self.gui.move_to_editor(w=width, h=height)

    def canvas_enter(self, e):
        self.canvas.config(width=1000, height=1000, bg="lightblue", border=0)

        self.label_on_canvas.config(bg="lightblue", width=100, text="")
        self.label_info.pack()
        self.entry_name.pack(pady=5)

        self.label_info_width.pack(pady=5)
        self.entry_width.pack(pady=5)
        self.label_info_height.pack(pady=5)
        self.entry_height.pack(pady=5)
        self.create_btn.pack(pady=5)

    def canvas_leave(self, e):
        self.label_on_canvas.config(bg="lightblue", width=3, text="NEW")
        self.canvas.config(width=100, height=100)
        self.label_info_width.forget()
        self.entry_width.forget()
        self.label_info_height.forget()
        self.entry_height.forget()
        self.label_info.forget()
        self.create_btn.forget()
        self.entry_name.pack_forget()
        self.entry_name.pack_forget()


