from chipy8 import chip8
from tkinter import *
import argparse

root = Tk()
root.geometry("400x300")


app = chip8.Chip8(root)
app.bind("<Key>", app.on_key_press)
app.bind("<KeyRelease>", app.on_key_release)
app.focus_set()
app.pack()
while True:
    app.update_idletasks()
    app.update()
    app.main()
