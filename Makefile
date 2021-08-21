install:
	sudo apt-get install libcups2-dev && pip install -r requirements.txt

up:
	flask run