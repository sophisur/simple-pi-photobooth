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

max_pictures_in_bottom_layout = 20
max_row_number_for_old_photos = 4

class SoPhotoApp(App):
    def build(self):
        self.nb_pictures = 0
        self.layout = BoxLayout(orientation='horizontal', spacing=20)

        ########################################
        #LAYOUT PHOTOS
        ########################################
        #Main photos layout for pictures display
        layout_photos = BoxLayout(orientation='vertical', size_hint_x=0.7, spacing=10)

        #Last photo layout declaration
        layout_last_photo = BoxLayout(orientation='vertical')
        self.last_photo = kivyImage(source='fine_pictures/last_photo.jpg')

        #Layout containing max_pictures_in_bottom_layout pictures
        self.layout_bottom = GridLayout(cols=max_pictures_in_bottom_layout/max_row_number_for_old_photos)

        #Adding sublayouts/wodgets in the layout_photos
        layout_photos.add_widget(self.last_photo)
        layout_photos.add_widget(self.layout_bottom)

        #Adding photos layout in the main layout
        self.layout.add_widget(layout_photos)

        ########################################
        #LAYOUT BUTTONS
        ########################################
        #Main button layout for pictures manipulations
        layout_buttons = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.3)

        #Shortcut layout declaration
        one_photo_default_picture = kivyImage(source='raw_pictures/profil_picture_default.jpg')
        one_photo_button = Button(text = 'Prendre une grande photo')
        four_photo_default_picture = kivyImage(source='raw_pictures/profil_picture_default.jpg')
        four_photo_button = Button(text = 'Prendre 4 photos')

        #Adding widgets in the layout_photos
        layout_buttons.add_widget(one_photo_default_picture)
        layout_buttons.add_widget(one_photo_button)
        layout_buttons.add_widget(four_photo_default_picture)
        layout_buttons.add_widget(four_photo_button)
        
        #Adding photos layout in the main layout
        self.layout.add_widget(layout_buttons)

        #Shorcuts buttons clicked connections
        one_photo_button.bind(on_press = self.take1)
        four_photo_button.bind(on_press = self.take4)

        ########################################
        #APP
        ########################################
        #Load application
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
