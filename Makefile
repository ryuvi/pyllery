all: run

init:
	pip install -r requirements.txt

build: init
	pyinstaller pyllery/main.py --onefile --name gallery --hidden-import='PIL._tkinter_finder'

run: build
	./dist/gallery