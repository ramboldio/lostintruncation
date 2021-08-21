install:
	sudo apt-get install libcups2-dev && pip3 install -r requirements.txt
up:
	flask run
