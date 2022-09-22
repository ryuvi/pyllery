#!/usr/bin/env python3

from sys import argv
from tkinter import Menu, PhotoImage, Tk, Label
from tkinter import CENTER
from os.path import isdir, join, dirname

from pyllery.extra import *


def init():
    root = Tk()
    root.title('pyllery')
    
    # TODO: Later add the icon (This shit does not work yet)
    # basedir = dirname(__file__)
    # root.iconphoto(True, PhotoImage(file=join(basedir, '..', 'icon.png')))

    label = Label(master=root)
    menu = Menu(root)

    files = []

    label.place(anchor=CENTER, rely=0.5, relx=0.5)
    root.config(menu=menu)
    root.geometry('800x600')
    menu.add_command(label='<', command=lambda: left_key('a'))
    menu.add_command(label='>', command=lambda: right_key('a'))
    menu.add_command(label='Open File', command=open_file)
    menu.add_command(label='Open Folder', command=open_folder)

    root.bind('<Left>', left_key)
    root.bind('<Right>', right_key)
    set_label(label)
    set_win(root)

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

if __name__ == '__main__':
    init()