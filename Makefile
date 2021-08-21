install:
	sudo apt-get update && sudo apt-get install git cups wiringpi build-essential libcups2-dev libcupsimage2-dev python3-serial samba smbclient && pip3 install -r requirements.txt

up:
	flask run --host=0.0.0.0

thermal_printer_work:
	git clone https://github.com/adafruit/zj-58 && cd zj-58 && make && sudo ./install && sudo lpadmin -p ZJ-58 -E -v serial:/dev/serial0?baud=19200 -m zjiang/ZJ-58.ppd
