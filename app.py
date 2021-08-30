from flask import Flask
from flask import request, send_from_directory

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

photo_printer_name = 'SELPHY-CP1300'
#photo_printer_name = 'ZJ-58'

app = Flask(__name__, static_url_path='',  static_folder='ui')
CORS(app)
cups_connection = cups.Connection()

colab_url = os.environ.get('COLABURL')


@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join('./uploaded_images', filename)
            file.save(image_path)
            print("start colab generation process")
            stylized_image_path = stylize_image_colab(image_path)
            print("recieved stylized image; start printing")
            print_image(stylized_image_path)
            return "success"

@app.route('/submit_text', methods = ['POST'])
def submit_text():
    input_text = request.form['text']
    print("start generation process")
    response_text = requests.post(colab_url + "/generate_text", data={"text": input_text}).text
    print("start printing process")
    print(response_text)
    print_text(response_text)
    return "success"

def stylize_image_colab(filename):
    output_filename = 'stylized-image.png'

    files = {'file': open(filename, 'rb')}
    response = requests.post(colab_url + "/generate_image", files=files)
    file = open(output_filename, "wb")
    file.write(response.content)
    file.close()
    return output_filename


def print_image(image_path='test.jpg'):
    # Save the picture to a temporary file for printing
    from tempfile import mktemp
    im = Image.new('RGB', (1024, 1024))
    im.paste(Image.open(image_path).resize((1024, 1024)), ( 0, 0, 1024, 1024))
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
    text = text.encode("ascii", "ignore").decode()
    ser = serial.Serial("/dev/serial0", baudrate=19200)
    ser.write(bytes(text + "\n", 'ascii'))
    
#    ser.write(bytes(text + "\n"))

# print_image()
# print_text()