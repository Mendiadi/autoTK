import tkinter
from tkinter import *


win = Tk()

# Set the size of the window
win.geometry("700x350")

# Create a Listbox widget

# Define a function to edit the listbox ite

# Add items in the Listbox

flag = True
l = Canvas(win,bg="red",height=100,width=100
)
oval = l.create_oval(0,0,100,100,fill="green")


def do():
    global flag,oval
    if flag:
        l.delete(oval)
        oval  = l.create_oval(0, 0, 50, 50, fill="blue")
    else:
        l.delete(oval)
        oval = l.create_oval(0, 0, 100, 100, fill="green")
    flag = not flag



btn = tkinter.Button(win,text="ckick",command=do)
btn.pack()
l.pack()
win.mainloop()




