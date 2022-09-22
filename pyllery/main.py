#!/usr/bin/env python3

from sys import argv
from tkinter import W, Menu, Tk, Label
from os import listdir
from os.path import join, isdir, isfile

from extra import *
from PIL import Image, ImageTk
from tkinter import Label


def init():
    root = Tk()
    label = Label(master=root)
    menu = Menu(root)

    files = []

    label.grid(row=1, column=0)
    root.config(menu=menu)
    menu.add_command(label='Open File', command=open_file)
    menu.add_command(label='Open Folder', command=open_folder)

    root.bind('<Left>', left_key)
    root.bind('<Right>', right_key)
    set_label(label)

    if len(argv) > 1:
        dir = argv[1]
        if isdir(dir) and have_file(dir):
            files = take_files(dir)
            set_image(label, files[0])

        elif isdir(dir) and not have_file(dir):
            files = search_files(dir)
            set_image(label, files[0])
        
        else:
            set_image(label, dir)


    root.mainloop()
