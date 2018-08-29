from PIL import Image as pilImage
from datetime import date, time, datetime
import os


class ImageEditor:
    def __init__(self):
        self.top_left = pilImage.open('mask_images/topleft.png')

        today = datetime.today().strftime('%Y_%m_%d')

        self.raw_path = os.path.join('raw_pictures', today)
        if not os.path.exists(self.raw_path):
            os.makedirs(self.raw_path)

        self.fine_path = os.path.join('fine_pictures', today)
        if not os.path.exists(self.fine_path):
            os.makedirs(self.fine_path)


    def apply_big_picture_mask(self, image):
        self.save(image, self.raw_path)
        image.paste(self.top_left, (0, 0), mask=self.top_left)
        return self.save(image, self.fine_path)

    def save(self, image, path_folder):
        now = datetime.now().strftime('%H_%M_%S_%f')
        
        path_img = os.path.join(path_folder, '%s.jpg' % now)
        image.save(path_img)
        if path_folder == self.fine_path:
            image.save('fine_pictures/last_photo.jpg')#constant override
        return path_img

    def apply_4_pictures_mask(self, images):
        pass
