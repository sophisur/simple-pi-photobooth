from PIL import Image as pilImage
from datetime import date, time, datetime
import os


class ImageEditor:
    def __init__(self):
        self.top_left = pilImage.open('mask_images/topleft.png')

        today = datetime.today().strftime('%Y_%m_%d')

        self.raw_path = self.make_path('raw_pictures', today)
        self.fine_path = self.make_path('fine_pictures', today)
        self.small_path = self.make_path('small_pictures', today)

    def make_path(self, folder_name, today):
        path_maked = os.path.join(folder_name, today)
        if not os.path.exists(path_maked):
            os.makedirs(path_maked)
        return path_maked

    def apply_big_picture_mask(self, image):
        self.save(image, self.raw_path)
        image.paste(self.top_left, (0, 0), mask=self.top_left)
        copy = image.rotate(180)
        self.save(copy, self.fine_path)
        copy.thumbnail((640, 480))
        return self.save(copy, self.small_path)

    def save(self, image, path_folder):
        now = datetime.now().strftime('%H_%M_%S_%f')
        
        path_img = os.path.join(path_folder, '%s.jpg' % now)
        image.save(path_img)
        if path_folder == self.small_path:
            image.save('small_pictures/last_photo.jpg')#constant override
        return path_img

    def apply_4_pictures_mask(self, images):
        pass
