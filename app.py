from flask import Flask
from flask import request

import cups
# import Image
from tempfile import mktemp
from time import sleep
import serial
from PIL import Image

photo_printer_name = 'SELPHY-CP1300'

app = Flask(__name__)
cups_connection = cups.Connection()

@app.route('/submit', methods = ['POST'])
def user(user_id):
    if request.method == 'POST':
    	pass

def print_image():
	printers = cups_connection.getPrinters()

	# Save the picture to a temporary file for printing
	from tempfile import mktemp
	im = Image.new('RGB', (683, 384))
	im.paste(Image.open('test.jpg').resize((683, 384)), ( 0, 0, 683, 384))
	output = mktemp(prefix='jpg')
	im.save(output, format='jpeg')

	# Send the picture to the printer
	print_id = conn.printFile(printer_name, output, "Photo Booth", {})

	# Wait until the job finishes
	from time import sleep
	while conn.getJobs().get(print_id, None):
	    sleep(1)

	print("yo finished")


def print_text(text="yoyoyoyoyo")
	uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
	ser.write("text\r\n")

# print_image()
print_text()