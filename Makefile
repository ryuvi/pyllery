init:
	pip install -r requirements.txt

build:
	pyinstaller pyllery/init.py --onefile --name gallery --hidden-import='PIL._tkinter_finder'

test:
	nosetest tests