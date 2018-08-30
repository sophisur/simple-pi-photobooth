#!/usr/bin/env python

from PIL import Image as pilImage
import glob
from kivy.app import App
from kivy.uix.image import Image as kivyImage
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from imageEditor import ImageEditor

faking_it = True
if not faking_it:
    from photoTaker import PhotoTaker
    photo = PhotoTaker()

image_editor = ImageEditor()

max_pictures_in_bottom_layout = 16
max_row_number_for_old_photos = 2

class SoPhotoApp(App):
    def build(self):
        self.nb_pictures = 0
        self.layout = BoxLayout(orientation='vertical', spacing=10)

        #Shortcut layout declaration
        layout_buttons = BoxLayout(orientation='horizontal', size_hint=(1, .2))
        uphoto = Button(text = 'Prendre une grande photo')
        qphoto = Button(text = 'Prendre 4 photos')
        ##Shorcuts buttons clicked connections
        uphoto.bind(on_press = self.take1)
        qphoto.bind(on_press = self.take4)
        ##Shortcuts insert inside layout
        layout_buttons.add_widget(uphoto)
        layout_buttons.add_widget(qphoto)

        #Last photo layout declaration
        layout_last_photo = BoxLayout(orientation='horizontal', size_hint=(1, .7))
        self.last_photo = kivyImage(source='fine_pictures/last_photo.jpg')
        layout_last_photo.add_widget(self.last_photo)

        #Layout containing max_pictures_in_bottom_layout pictures
        self.layout_bottom = GridLayout(cols=max_pictures_in_bottom_layout/max_row_number_for_old_photos, size_hint=(1, .3))

        #Insert layouts in main app
        self.layout.add_widget(layout_last_photo)
        self.layout.add_widget(self.layout_bottom)
        self.layout.add_widget(layout_buttons)

        self.load()

        return self.layout

    def reload(self):
        self.last_photo.reload()

    def load(self):
        for picture_path in glob.iglob('fine_pictures/*/*.jpg'):
            self.add_picture(picture_path)

    def add_picture(self, picture_path):
        im = kivyImage(source=picture_path)
        self.nb_pictures = self.nb_pictures + 1
        if self.nb_pictures > max_pictures_in_bottom_layout:
            self.layout_bottom.remove_widget(self.layout_bottom.children[len(self.layout_bottom.children)-1])
        self.layout_bottom.add_widget(im)

    def take1(self, instance):
        print('Take 1 picture')
        if faking_it:
            image = pilImage.open('raw_pictures/default_picture.jpg')
        else:
            image = photo.take_photo()

        picture_path = image_editor.apply_big_picture_mask(image)
        self.add_picture(picture_path)
        self.reload()

    def take4(self, instance):
        print('take 4 pictures')
        # photo = PhotoTaker()
        # photo.take_4_photo()


if __name__ == '__main__':
    SoPhotoApp().run()
