#!/usr/bin/env python

from PIL import Image as pilImage
import glob
import os
from kivy.app import App
# from kivy.uix.image import Image as kivyImage
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from imageEditor import ImageEditor
from imageButton import ImageButton
from popupProgress import PopupProgress, PopupProgressFour

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
        # LAYOUT PHOTOS
        ########################################
        # Main photos layout for pictures display
        layout_photos = BoxLayout(orientation='vertical', spacing=5)

        # Last photo layout declaration
        self.last_photo = ImageButton(source='small_pictures/last_photo.jpg')
        # Connecting on_press signal
        self.last_photo.bind(on_press=self.display_picture_on_popup)

        # Layout containing max_pictures_in_bottom_layout pictures
        cols = int(max_pictures_in_bottom_layout / max_row_number_for_old_photos)
        self.layout_bottom = GridLayout(cols=cols, spacing=(5, 5))

        # Adding sublayouts/widgets in the layout_photos
        layout_photos.add_widget(self.last_photo)
        layout_photos.add_widget(self.layout_bottom)

        ########################################
        # LAYOUT BUTTONS
        ########################################
        # Main button layout for pictures manipulations
        layout_buttons = BoxLayout(orientation='vertical', size_hint_x=.33)

        # Shortcut layout declaration
        one_photo_default_picture = ImageButton(source='small_pictures/default_1.jpg')
        one_photo_button = Button(text='Prendre 1 photo', size_hint = (1, .3))
        four_photo_default_picture = ImageButton(source='small_pictures/default_2.jpg')
        four_photo_button = Button(text='Prendre 4 photos', size_hint=(1, .3))

        # Adding widgets in the layout_photos
        layout_buttons.add_widget(one_photo_default_picture)
        layout_buttons.add_widget(one_photo_button)
        layout_buttons.add_widget(four_photo_default_picture)
        layout_buttons.add_widget(four_photo_button)

        # Shorcuts buttons clicked connections
        one_photo_default_picture.bind(on_press=self.take1)
        one_photo_button.bind(on_press=self.take1)
        four_photo_default_picture.bind(on_press=self.take4)
        four_photo_button.bind(on_press=self.take4)

        ########################################
        # GENERAL
        ########################################
        # Adding photos layout in the main layout
        self.layout.add_widget(layout_buttons)
        # Adding photos layout in the main layout
        self.layout.add_widget(layout_photos)

        ########################################
        # APP
        ########################################
        # Load application
        self.load()

        return self.layout

    def reload(self):
        self.last_photo.reload()

    def load(self):
        pictures_files = glob.glob('small_pictures/*/*.jpg')
        pictures_files.sort(key=os.path.getmtime)
        for picture_path in pictures_files:
            self.add_picture(picture_path)

    def add_picture(self, picture_path):
        # Create new picture button
        im = ImageButton(source=picture_path)

        # Old pictures layout management
        self.nb_pictures = self.nb_pictures + 1
        if self.nb_pictures > max_pictures_in_bottom_layout:
            self.layout_bottom.remove_widget(self.layout_bottom.children[len(self.layout_bottom.children)-1])

        # Connecting on_press signal
        im.bind(on_press=self.display_picture_on_popup)

        # Adding new widget in old pictures layout
        self.layout_bottom.add_widget(im)

    def take1(self, instance):
        print('Take 1 picture')
        
        # Create Popup Progress
        popup_progress = PopupProgress(title='', separator_height=0)
        popup_progress.bind(on_open=self.start_preview)

        popup_progress.start_progress(3)

        # Connection dismiss signal on take_one_photo_action
        popup_progress.bind(on_dismiss=self.take_one_photo_action)

        # Open Popup Progress
        popup_progress.open()

    def take4(self, instance):
        print('take 4 pictures')

        self.images = []
        popup_progress = PopupProgressFour(title='', separator_height=0, photomaton=self)
        popup_progress.bind(on_open=self.start_preview)
        popup_progress.bind(on_dismiss=self.four_photo_assembly)

        popup_progress.start_progress(15)
        popup_progress.open()

    def start_preview(self, instance):
        if faking_it:
            pass
        else:
            photo.start_preview()

    def take_one_photo_action(self, instance):
        if faking_it:
            image = pilImage.open('raw_pictures/default_picture.jpg')
        else:
            image = photo.take_photo()
            photo.stop_preview()
            
        # Display last picture taken
        self.add_picture(image_editor.apply_big_picture_mask(image))
        self.reload()

    def take_one_of_four_photo_action(self):
        if faking_it:
            image = pilImage.open('raw_pictures/default_picture.jpg')
        else:
            image = photo.take_photo()
        self.images.append(image)

    def four_photo_assembly(self, instance):
        if faking_it:
            pass
        else:
            photo.stop_preview()

        self.add_picture(image_editor.apply_4_pictures_mask(self.images))
        self.reload()

    def display_picture_on_popup(self, instance):
        # Main popup layout
        layout_popup = BoxLayout(orientation='vertical', spacing=5)

        # Create popup layout content
        back_to_main_button = Button(text='<-', size_hint=(.2, .2))

        # Adding contents into popup layout
        layout_popup.add_widget(back_to_main_button)
        layout_popup.add_widget(ImageButton(source=instance.source))

        # Create popup
        popup = Popup(title='', separator_height=0, content=layout_popup)

        # Bind the on_press event of the button to the dismiss function
        back_to_main_button.bind(on_press=popup.dismiss)

        # Open popup
        popup.open()


if __name__ == '__main__':
    SoPhotoApp().run()
