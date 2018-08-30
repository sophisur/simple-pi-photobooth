#!/usr/bin/env python

from PIL import Image as pilImage
import glob
import os
from kivy.app import App
from kivy.uix.image import Image as kivyImage
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.config import Config
from imageEditor import ImageEditor
from imageButton import ImageButton
from popupProgress import PopupProgress
from shutil import copyfile

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

        # PROPOSAL 1
        self.layout = BoxLayout(orientation='horizontal')
        ########################################
        #LAYOUT PHOTOS
        ########################################
        #Main photos layout for pictures display
        layout_photos = BoxLayout(orientation='vertical')

        #Last photo layout declaration
        layout_last_photo = BoxLayout(orientation='vertical')
        self.last_photo = kivyImage(source='fine_pictures/last_photo.jpg')

        #Layout containing max_pictures_in_bottom_layout pictures
        self.layout_bottom = GridLayout(cols=max_pictures_in_bottom_layout/max_row_number_for_old_photos)

        #Adding sublayouts/wodgets in the layout_photos
        layout_photos.add_widget(self.last_photo)
        layout_photos.add_widget(self.layout_bottom)

        ########################################
        #LAYOUT BUTTONS
        ########################################
        #Main button layout for pictures manipulations
        layout_buttons = BoxLayout(orientation='vertical', size_hint_x=.33)

        #Shortcut layout declaration
        one_photo_default_picture = kivyImage(source='raw_pictures/profil_picture_default.jpg')
        one_photo_button = Button(text = 'Prendre 1 photo', size_hint=(1,.3))
        four_photo_default_picture = kivyImage(source='raw_pictures/profil_picture_default.jpg')
        four_photo_button = Button(text = 'Prendre 4 photos', size_hint=(1,.3))

        #Adding widgets in the layout_photos
        layout_buttons.add_widget(one_photo_default_picture)
        layout_buttons.add_widget(one_photo_button)
        layout_buttons.add_widget(four_photo_default_picture)
        layout_buttons.add_widget(four_photo_button)

        #Shorcuts buttons clicked connections
        one_photo_button.bind(on_press = self.take1)
        four_photo_button.bind(on_press = self.take4)

        ########################################
        #GENERAL
        ########################################
        #Adding photos layout in the main layout
        self.layout.add_widget(layout_buttons)
        #Adding photos layout in the main layout
        self.layout.add_widget(layout_photos)

        # # PROPOSAL 2
        # self.layout = BoxLayout(orientation='vertical')
        # ########################################
        # #LAYOUT PHOTOS
        # ########################################
        # #Main photos layout for pictures display
        # layout_photos = BoxLayout(orientation='horizontal')

        # #Last photo layout declaration
        # layout_last_photo = BoxLayout(orientation='vertical')
        # self.last_photo = kivyImage(source='fine_pictures/last_photo.jpg')

        # #Layout containing max_pictures_in_bottom_layout pictures
        # self.layout_bottom = GridLayout(cols=max_pictures_in_bottom_layout/max_row_number_for_old_photos)

        # #Adding sublayouts/wodgets in the layout_photos
        # layout_photos.add_widget(self.last_photo)
        # layout_photos.add_widget(self.layout_bottom)

        # ########################################
        # #LAYOUT BUTTONS
        # ########################################
        # #Main button layout for pictures manipulations
        # layout_buttons = BoxLayout(orientation='horizontal', size_hint_y=0.3)

        # #Layout for taken one photo
        # layout_one_photo_button = BoxLayout(orientation='vertical')
        # #Layout for taken four photos
        # layout_four_photo_button = BoxLayout(orientation='vertical')

        # #Shortcut layout declaration
        # one_photo_default_picture = kivyImage(source='raw_pictures/profil_picture_default.jpg')
        # one_photo_button = Button(text = 'Prendre 1 photo', size_hint=(1,.3))
        # four_photo_default_picture = kivyImage(source='raw_pictures/profil_picture_default.jpg')
        # four_photo_button = Button(text = 'Prendre 4 photos', size_hint=(1,.3))

        # #Adding widgets in the layout_photos
        # layout_one_photo_button.add_widget(one_photo_default_picture)
        # layout_one_photo_button.add_widget(one_photo_button)
        # layout_four_photo_button.add_widget(four_photo_default_picture)
        # layout_four_photo_button.add_widget(four_photo_button)
        
        # #Shorcuts buttons clicked connections
        # one_photo_button.bind(on_press = self.take1)
        # four_photo_button.bind(on_press = self.take4)

        # #Adding sublayouts into buttons layout
        # layout_buttons.add_widget(layout_one_photo_button)
        # layout_buttons.add_widget(layout_four_photo_button)

        # ########################################
        # #GENERAL
        # ########################################
        # #Adding photos layout in the main layout
        # self.layout.add_widget(layout_buttons)
        # #Adding photos layout in the main layout
        # self.layout.add_widget(layout_photos)

        ########################################
        #APP
        ########################################
        #Load application
        self.load()

        return self.layout

    def reload(self):
        self.last_photo.reload()

    def load(self):
        pictures_files = glob.glob('fine_pictures/*/*.jpg')
        pictures_files.sort(key=os.path.getmtime)
        for picture_path in pictures_files:
            self.add_picture(picture_path)

    def add_picture(self, picture_path):
        #Create new picture button
        im = ImageButton(source=picture_path)

        #Old pictures layout management
        self.nb_pictures = self.nb_pictures + 1
        if self.nb_pictures > max_pictures_in_bottom_layout:
            self.layout_bottom.remove_widget(self.layout_bottom.children[len(self.layout_bottom.children)-1])

        #Connecting on_press signal
        im.bind(on_press = self.display_old_picture)

        #Adding new widget in old pictures layout
        self.layout_bottom.add_widget(im)

    def take1(self, instance):
        print('Take 1 picture')
        
        # Create Popup Progress
        popupProgress = PopupProgress(title='', separator_height=0)
        popupProgress.start_progress(3)

        # Connection dismiss signal on take_one_photo_action
        popupProgress.bind(on_dismiss=self.take_one_photo_action)

        # Open Popup Progress
        popupProgress.open()

    def take4(self, instance):
        print('take 4 pictures')

        # # Create Popup Progress
        # popupProgress = PopupProgress(title='', separator_height=0)
        # popupProgress.start_progress(3)

        # # Connection dismiss signal on take_four_photo_action
        # popupProgress.bind(on_dismiss=self.take_four_photo_action)

        # # Open Popup Progress
        # popupProgress.open()
        
    def take_one_photo_action(self, instance):
        if faking_it:
            image = pilImage.open('raw_pictures/default_picture.jpg')
        else:
            image = photo.take_photo()
            
        #Display last picture taken
        self.add_picture(image_editor.apply_big_picture_mask(image))
        self.reload()

    def take_four_photo_action(self, instance):
        print('take 4 pictures')
        # photo = PhotoTaker()
        # photo.take_4_photo()

    def display_old_picture(self, instance):
        #Main popup layout
        layout_popup = BoxLayout(orientation='vertical', spacing=5)

        #Create popup layout content
        back_to_main_button = Button(text='<-', size_hint=(.2,.2))

        #Adding contents into popup layout
        layout_popup.add_widget(back_to_main_button)
        layout_popup.add_widget(ImageButton(source=instance.source))

        #Create popup
        popup = Popup(title='', separator_height=0, content=layout_popup)

        #Bind the on_press event of the button to the dismiss function
        back_to_main_button.bind(on_press=popup.dismiss)

        #Open popup
        popup.open()

if __name__ == '__main__':
    SoPhotoApp().run()
