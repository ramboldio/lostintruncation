from flask import Flask
from flask import request

import cups
import requests
# import Image
from tempfile import mktemp
from time import sleep
import os
import serial
from PIL import Image
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename  

#photo_printer_name = 'SELPHY-CP1300'
photo_printer_name = 'ZJ-58'

app = Flask(__name__)
CORS(app)
cups_connection = cups.Connection()

@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        print(request.files.keys())
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join('./uploaded_images', filename)
            file.save(image_path)
            stylized_image_path = stylize_image_colab(image_path)
            print_image(stylized_image_path)

def stylize_image_colab(filename):
    output_filename = 'stylized-image.png'

    files = {'file': open(filename, 'rb')}
    response = requests.post(ENV['COLABURL'], files=files)
    file = open(output_filename, "wb")
    file.write(response.content)
    file.close()
    return output_filename


def print_image(image_path='test.jpg'):
    # Save the picture to a temporary file for printing
    from tempfile import mktemp
    im = Image.new('RGB', (683, 384))
    im.paste(Image.open(image_path).resize((683, 384)), ( 0, 0, 683, 384))
    output = mktemp(prefix='jpg')
    im.save(output, format='jpeg')

    # Send the picture to the printer
    print_id = cups_connection.printFile(photo_printer_name, output, "Photo Booth", {})

    # Wait until the job finishes
    from time import sleep
    while cups_connection.getJobs().get(print_id, None):
        sleep(1)

    print("yo finished")


def print_text(text="yoyoyoyoyo"):
    ser = serial.Serial("/dev/serial0", baudrate=19200)
    ser.write(bytes(text + "\n", 'ascii'))

# print_image()
# print_text()