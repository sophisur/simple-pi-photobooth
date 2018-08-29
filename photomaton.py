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

faking_it = False
if not faking_it:
    from photoTaker import PhotoTaker
    photo = PhotoTaker()

image_editor = ImageEditor()


class SoPhotoApp(App):
    def build(self):
        self.nb_pictures = 0
        self.layout = BoxLayout(orientation='vertical')

        layout_buttons = BoxLayout(orientation='horizontal')
        uphoto = Button(text='Prendre une grande photo')
        uphoto.bind(on_press=self.take1)
        qphoto = Button(text='Prendre 4 photos')
        qphoto.bind(on_press=self.take4)
        layout_buttons.add_widget(uphoto)
        layout_buttons.add_widget(qphoto)

        self.last_photo = kivyImage(source='fine_pictures/last_photo.jpg')
        layout_buttons.add_widget(self.last_photo)

        self.layout.add_widget(layout_buttons)

        self.layout_bottom = GridLayout(cols=10)
        self.layout.add_widget(self.layout_bottom)

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
        if self.nb_pictures > 40:
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
