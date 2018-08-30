from kivy.uix.image import Image as kivyImage
from kivy.uix.behaviors import ButtonBehavior

class ImageButton(ButtonBehavior, kivyImage):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
