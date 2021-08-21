from flask import Flask
from flask import request

import cups
# import Image
from tempfile import mktemp
from time import sleep
import serial
from PIL import Image
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename  

photo_printer_name = 'SELPHY-CP1300'

app = Flask(__name__)
CORS(app)
cups_connection = cups.Connection()

@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join('./uploaded_images', filename)
            file.save(image_path)
            print_image(image_path)

def print_image(image_path='test.jpg'):
    # Save the picture to a temporary file for printing
    from tempfile import mktemp
    im = Image.new('RGB', (683, 384))
    im.paste(Image.open(image_path).resize((683, 384)), ( 0, 0, 683, 384))
    output = mktemp(prefix='jpg')
    im.save(output, format='jpeg')

    # Send the picture to the printer
    print_id = cups.printFile(photo_printer_name, output, "Photo Booth", {})

    # Wait until the job finishes
    from time import sleep
    while conn.getJobs().get(print_id, None):
        sleep(1)

    print("yo finished")


def print_text(text="yoyoyoyoyo"):
    ser = serial.Serial("/dev/serial0", baudrate=19200)
    ser.write(bytes(text + "\n", 'ascii'))

# print_image()
# print_text()