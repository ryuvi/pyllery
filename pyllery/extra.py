from os import listdir
from os.path import join, isdir, isfile, basename

from PIL import Image, ImageTk
from tkinter import Label, filedialog, Tk


_file_list = []
_curr_image = ''
_label: Label
_win: Tk


def set_win(widget):
    global _win
    _win = widget


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


def _win_size() -> tuple:
    return (_win.winfo_width(), _win.winfo_height())


def rule_of_three(total, target) -> float:
    return ((total*target)/100)


def set_image(widget: Label, image: str):
    global _curr_image

    img = Image.open(image)
    width, height = img.size
    w_width, w_height = _win_size() if _win_size() > (1,1) else (600,400)

    # Take 75% of the screen
    usable_size = rule_of_three(w_width, 90)

    # Take percentage to be multiplied into the image size to resize it to a fitable size
    ratio = ((100 * usable_size) / width) / 100
    while height > w_height or width > w_width:
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