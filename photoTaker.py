#from picamera import PiCamera
from time import sleep
from io import BytesIO
from PIL import Image


class PhotoTaker:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (3280, 2464)
        #self.camera.framerate = 15

    def start_preview(self):
        #window=(1,1,400,400)
        self.camera.start_preview(alpha=200, fullscreen=True, rotation=180)

    def stop_preview(self):
        self.camera.stop_preview()

    def take_photo(self):
        image = self.take_one_photo()
        return image

    def take_one_photo(self):
        stream = BytesIO()

        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        image = Image.open(stream)
        return image
