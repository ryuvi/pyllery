from os import listdir
from os.path import join, isdir, isfile, basename, splitext
from pathlib import Path

from PIL import Image, ImageTk
from PIL.ImageFile import LOAD_TRUNCATED_IMAGES
from tkinter import Label, filedialog, Tk
from threading import Timer

from pyaes import AESModeOfOperationCTR

LOAD_TRUNCATED_IMAGES = True
_file_list = []
_curr_image = ""
_old_size = (0, 0)
_curr_img_size = (0, 0)
_label: Label
_win: Tk
key = ''
_is_from_search = False
extensions = [
    ".jpg",
    ".jpeg",
    ".jpe",
    ".jif",
    ".jfif",
    ".jfi",
    ".png",
    ".gif",
    ".webp",
    ".tiff",
    ".tif",
    ".psd",
    ".raw",
    ".arw",
    ".cr2",
    ".nrw",
    ".k25",
    ".bmp",
    ".dib",
    ".heif",
    ".heic",
    ".ind",
    ".indd",
    ".indt",
    ".jp2",
    ".j2k",
    ".jpf",
    ".jpx",
    ".jpm",
    ".mj2",
    ".svg",
    ".svgz",
    ".ai",
    ".eps",
    ".pdf",
]
_cur_theme = "classic"


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def is_valid_file(file) -> bool:
    result = False
    filename, extension = splitext(file)
    if extension in extensions:
        result = True

    return result


def check_list(file_list) -> None:
    global _file_list

    flist = []
    for file in file_list:
        if is_valid_file(file):
            flist.append(file)

    _file_list = flist


def set_win(widget):
    global _win
    _win = widget


def search_files(folder):
    global _file_list, _is_from_search
    _is_from_search = True
    arr = []
    for item in listdir(folder):
        new_path = join(folder, item)

        if isdir(new_path):
            arr += search_files(new_path)

        else:
            arr.append(new_path)

    return arr


def have_file(folder):
    for item in listdir(folder):
        if isfile(f"{folder}/{item}"):
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

    check_list(_files)
    return _files


def open_file():
    file = filedialog.askopenfilename(initialdir=f"{Path.home()}")
    take_files(file.replace(basename(file), ""))
    set_image(_label, file)


def open_folder():
    folder = filedialog.askdirectory(initialdir=f"{Path.home()}")

    if have_file(folder):
        files = take_files(folder)
        check_list(files)
        set_image(_label, files[0])

    else:
        files = search_files(folder)
        check_list(files)
        set_image(_label, files[0])


def set_label(widget):
    global _label
    _label = widget


def _win_size() -> tuple:
    return (_win.winfo_width(), _win.winfo_height())


def rule_of_three(total, target) -> float:
    return (total * target) / 100


def take_bigger(size: tuple) -> float:
    return size[0] if size[0] > size[1] else size[1]


def take_percentage(usize, fsize) -> float:
    return ((100 * usize) / fsize) / 100


def get_key():
    global key
    with open(filedialog.askopenfilename(initialdir=f'{Path.home()}', title="Open Key"), 'rb') as r:
        key = r.read()


def set_image(widget: Label, image: str):
    global _curr_image, _curr_img_size

    if (is_valid_file(image) is True) or (image.endswith('.broken')):
        if image.endswith('.broken'):
            if key in (None, ''):
                get_key()            
            with open(image, 'rb') as f:
                _ = AESModeOfOperationCTR(key).decrypt(f.read())
            with open(f'{Path.cwd()}/temp.temp', 'wb') as w:
                w.write(_)
            img_path = f'{Path.cwd()}/temp.temp'
        else:
            img_path = image
        img = Image.open(img_path)
        width, height = img.size
        w_size = _win_size() if _win_size() > (1, 1) else (600, 400)
        w_width, w_height = w_size

        # Take 90% of the screen
        usable_size = rule_of_three(take_bigger(w_size), 90)

        # Take percentage to be multiplied into the image size to resize it to a fitable size
        ratio = take_percentage(usable_size, take_bigger(img.size))
        while height > w_height or width > w_width:
            width *= ratio
            height *= ratio

        size = (int(width), int(height))

        _curr_img_size = size
        img = img.resize(size)
        img = ImageTk.PhotoImage(img)

        widget["image"] = img
        widget.photo = img

        _curr_image = image

        if _is_from_search is False:
            take_files(image.replace(basename(image), ""))


def left_key(key):
    global _curr_image
    old_idx = _file_list.index(_curr_image)
    _curr_image = _file_list[old_idx - 1]

    set_image(_label, _curr_image)


def right_key(key):
    global _curr_image
    old_idx = _file_list.index(_curr_image)
    new_idx = old_idx + 1
    if new_idx >= len(_file_list):
        new_idx = 0
    _curr_image = _file_list[new_idx]

    set_image(_label, _curr_image)


def mouse_click(key):
    global _curr_img_size, _old_size

    img = Image.open(_curr_image)
    width, height = img.size
    ratio = take_percentage(
        rule_of_three(take_bigger(img.size), 25), take_bigger(img.size)
    )

    if _curr_img_size > _win_size():
        size = _old_size
        _curr_img_size = size
    else:
        _old_size = _curr_img_size
        size = (int(width / ratio), int(height / ratio))
        _curr_img_size = size

    img = img.resize(size)
    img = ImageTk.PhotoImage(img)

    _label["image"] = img
    _label.photo = img


_timer = RepeatTimer(2, right_key, args=("a",))


def set_slideshow():
    if _timer.is_alive():
        _timer.cancel()
    else:
        _timer.start()
