import os
import requests
import serial
import cups
from tempfile import mktemp
from time import sleep
from PIL import Image, ImageOps

from flask import Flask
from flask import request, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

photo_printer_name = 'Canon-SELPHY-CP1300'
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
    output = mktemp(prefix='jpg')
    img = Image.open(image_path)
    img.thumbnail((500, 500))
    # generate 2x2 grid
    img_grid = image_grid(img, 2, 2, margin=100)
    # add white border
    img_grid = ImageOps.expand(img_grid, border=100, fill='white')
    # Send the picture to the printer

    # make image to use up all available space of the printer which is 100,0 x 148,0 mm with 300dpi
    printer_output_size = (1181, 1748)
    # result_img = Image.new('RGB', size color="WHITE")

    img_grid = add_white_background(img_grid, printer_output_size)
    img_grid = img_grid.rotate(180)

    img_grid.show()

    img_grid.save(output, format='jpeg')

    print_id = cups_connection.printFile(photo_printer_name, output, "Photo Booth", {})

    # Wait until the job finishes
    while cups_connection.getJobs().get(print_id, None):
        sleep(1)

    print("yo finished")


def print_text(text="yoyoyoyoyo"):
    text = text.encode("ascii", "ignore").decode()
    ser = serial.Serial("/dev/serial0", baudrate=19200)
    ser.write(bytes(text + "\n", 'ascii'))

def image_grid(img, rows=2, cols=2, margin=30):
    w, h = img.size
    grid = Image.new('RGB', size=(cols*(w + margin) - margin, rows*(h + margin) - margin), color="WHITE")
    grid_w, grid_h = grid.size
    
    for i in range(rows * cols):
        grid.paste(img, box=(i%cols*(w + margin), i//cols*(h + margin)))
    return grid


def add_white_background(img, size):
    img_w, img_h = img.size
    background = Image.new('RGB', size, (255, 255, 255, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)
    return background
