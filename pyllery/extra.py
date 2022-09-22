from os import listdir
from os.path import join, isdir, isfile, basename

from PIL import Image, ImageTk
from tkinter import Label, filedialog


_file_list = []
_curr_image = ''
_label: Label


def search_files(folder):
    global _file_list
    arr = []
    for item in listdir(folder):
        new_path = join(folder, item)
        if isdir(item):
            search_files(new_path)
            
        else:
            arr.append(new_path)

    _file_list = arr   
    return arr


def have_file(folder):
    for item in listdir(folder):
        if isfile(f'{folder}/{item}'):
            return True
        else:
            return False


def take_files(folder):
    global _file_list
    _files = []
    for item in listdir(folder):
        filepath = join(folder, item)
        if isfile(filepath):
            _files.append(filepath)

    _file_list = _files
    return _files


def open_file():
    file = filedialog.askopenfilename()
    take_files(file.replace(basename(file), ''))
    set_image(_label, file)


def open_folder():
    folder = filedialog.askdirectory()

    if have_file(folder):
        files = take_files(folder)
        set_image(_label, files[0])

    else:
        files = search_files(folder)
        set_image(_label, files[0])



def set_label(widget):
    global _label
    _label = widget


def set_image(widget: Label, image: str):
    global _curr_image

    img = Image.open(image)
    width, height = img.size
    ratio = ((100 * 500) / width) / 100
    width *= ratio
    height *= ratio

    size = (int(width), int(height))
    img = img.resize(size)
    img = ImageTk.PhotoImage(img)
    
    widget['image'] = img
    widget.photo = img

    _curr_image = image

    take_files(image.replace(basename(image), ''))


def left_key(key):
    global _curr_image
    old_idx = _file_list.index(_curr_image)
    _curr_image = _file_list[old_idx-1]
    
    set_image(_label, _curr_image)


def right_key(key):
    global _curr_image
    old_idx = _file_list.index(_curr_image)
    new_idx = old_idx + 1
    if new_idx >= len(_file_list):
        new_idx = 0
    _curr_image = _file_list[new_idx]
    
    set_image(_label, _curr_image)