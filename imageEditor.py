from PIL import Image as pilImage
from datetime import date, time, datetime
import os

class ImageEditor:
    def __init__(self):
        self.top_left = pilImage.open('mask_images/topleft.png')

    def apply_big_picture_mask(self, image):
        image.paste(self.top_left, box=None)
        self.save(image)

    def save(self, image):
        today = datetime.today().strftime('%Y_%m_%d')
        now = datetime.now().strftime('%H_%M_%S_%f')
        path = os.path.join('fine_pictures', today)
        if not os.path.exists(path):
            os.makedirs(path)
        path_img = os.path.join(path, '%s.jpg' % now)
        image.save(path_img)

    def apply_4_pictures_mask(self, images):
        pass