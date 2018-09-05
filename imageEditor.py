from PIL import Image as pilImage
from datetime import date, time, datetime
import os


class ImageEditor:
    def __init__(self):
        self.top_large = pilImage.open('mask_images/Ornements-09.png')
        self.bottom_large = pilImage.open('mask_images/Ornements-10.png')
        self.top_medium = pilImage.open('mask_images/Ornements-07.png')
        self.bottom_medium = pilImage.open('mask_images/Ornements-08.png')

        self.top_large = self.resize(self.top_large, 3)
        self.bottom_large = self.resize(self.bottom_large, 3)

        today = datetime.today().strftime('%Y_%m_%d')

        self.raw_path = self.make_path('raw_pictures', today)
        self.fine_path = self.make_path('fine_pictures', today)
        self.small_path = self.make_path('small_pictures', today)

        self.top_width, self.top_h = self.top_large.size
        self.bottom_width, self.bottom_h = self.bottom_large.size

    def resize(self, image, ratio):
        w, h = image.size
        return image.resize((int(w*ratio), int(h*ratio)))

    def make_path(self, folder_name, today):
        path_maked = os.path.join(folder_name, today)
        if not os.path.exists(path_maked):
            os.makedirs(path_maked)
        return path_maked

    def apply_big_picture_mask(self, image):
        now = datetime.now().strftime('%H_%M_%S_%f')
        self.save(image, self.raw_path, now)
        copy = image.rotate(180)

        width, height = copy.size

        return self.apply_mask(copy, width, height, now)

    def apply_mask(self, image, width, height, now):
        width = width + self.top_h
        height = height + self.top_h + self.bottom_h

        super_image = pilImage.new('RGB', (width, height), color='white')
        super_image.paste(image, (int(self.top_h / 2), self.top_h))

        banner_w = int(width / 2 - self.top_width / 2)
        super_image.paste(self.top_large, (banner_w, 0), mask=self.top_large)

        banner_w = int(width / 2 - self.bottom_width / 2)
        super_image.paste(self.bottom_large, (banner_w, height - self.bottom_h), mask=self.bottom_large)

        self.save(super_image, self.fine_path, now)
        super_image.thumbnail((640, 480))
        return self.save(super_image, self.small_path, now)

    def save(self, image, path_folder, now):
        path_img = os.path.join(path_folder, '%s.jpg' % now)
        image.save(path_img)
        if path_folder == self.small_path:
            image.save('small_pictures/last_photo.jpg')#constant override
        return path_img

    def apply_4_pictures_mask(self, images):
        now = datetime.now().strftime('%H_%M_%S_%f')
        print(len(images))
        image = self.resize(images[0], 0.5)
        or_width, or_height = image.size
        or_width = int(or_width)
        or_height = int(or_height)

        margin = 50
        width = or_width * 4
        tot_width = width + margin * 3
        height = or_height

        super_image = pilImage.new('RGB', (tot_width, height), color='white')

        w = 0
        for i in range(0, 4):
            image = images[i]
            self.save(image, self.raw_path, now + '_' + str(i))
            copy = self.resize(image.rotate(180), 0.6)
            super_image.paste(copy, (w, 0))
            w = w + or_width + margin

        return self.apply_mask(super_image, tot_width, height, now)
