from PIL import Image as pilImage
import glob
from kivy.app import App
from kivy.uix.image import Image as kivyImage
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from imageEditor import ImageEditor

faking_it = True
if not faking_it:
    from photoTaker import PhotoTaker

image_editor = ImageEditor()


def take1(instance):
    print('Take 1 picture')
    if faking_it:
        image = pilImage.open('raw_pictures/default_picture.jpg')
    else:
        photo = PhotoTaker()
        image = photo.take_photo()

    image_editor.apply_big_picture_mask(image)


def take4(instance):
    print('take 4 pictures')
    #photo = PhotoTaker()
    #photo.take_4_photo()


class SoPhotoApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        layout_top = BoxLayout(orientation='horizontal')

        #TODO reload this
        for picture_path in glob.iglob('fine_pictures/*/*.jpg'):
            im = kivyImage(source=picture_path)
            layout_top.add_widget(im)

        layout_bottom = BoxLayout(orientation='horizontal')
        uphoto = Button(text='Prendre une grande photo')
        uphoto.bind(on_press=take1)
        qphoto = Button(text='Prendre 4 photos')
        qphoto.bind(on_press=take4)
        layout_bottom.add_widget(uphoto)
        layout_bottom.add_widget(qphoto)

        layout.add_widget(layout_top)
        layout.add_widget(layout_bottom)

        return layout


if __name__ == '__main__':
    SoPhotoApp().run()
