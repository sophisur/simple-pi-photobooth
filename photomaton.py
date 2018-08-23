from time import sleep
from PIL import Image
#from photoTaker import PhotoTaker
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


def take1(instance):
    print('Take 1 picture')


def take4(instance):
    print('take 4 pictures')


class PhotoApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        layout_top = BoxLayout(orientation='horizontal')

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
    PhotoApp().run()
    
                              
