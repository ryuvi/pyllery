all: run

init:
	pip install -r requirements.txt

build: init
	pyinstaller pyllery/main.py --noconsole --onedir --icon=icon.ico --name pyllery --hidden-import='PIL._tkinter_finder'

run: build
	./dist/gallery