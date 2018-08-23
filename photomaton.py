from picamera import PiCamera
from time import sleep
import toga
from io import BytesIO
from PIL import Image


import os


camera = PiCamera()
camera.rotation = 180
    
def start_preview():
    #window=(1,1,400,400)
    camera.start_preview(alpha=200, fullscreen=True, rotation=180)

def stop_preview():
    camera.stop_preview()
    
def take_photo(widget):
    start_preview()
    image = take_one_photo()


    stop_preview()

def take_one_photo():
    stream = BytesIO()

    sleep(2)
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    image = Image.open(stream)
    return image

    
    
def take_4_photo(widget):
    start_preview()
    image1 = take_one_photo()
    image2 = take_one_photo()
    image3 = take_one_photo()
    image4 = take_one_photo()

    stop_preview()


def build(app):

    
    path = os.path.dirname(os.path.abspath(__file__))
    toga.types

    #default_image = toga.Image('default_picture.jpg', factory=None)
    top_container = toga.Box()

    bottom_content = toga.Box()

    bottom_content.add(toga.Button('take photo', on_press= take_photo))
    bottom_content.add(toga.Button('take 4 photo', on_press= take_4_photo))

    split = toga.SplitContainer(direction=toga.SplitContainer.HORIZONTAL)
    split.content = [top_container, bottom_content]

    return split

def main():
    return toga.App('Photomaton', 'pouet', startup=build)

if __name__ == '__main__':
    main().main_loop()
    
                              
    
