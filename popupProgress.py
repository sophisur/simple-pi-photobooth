from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
import time

class PopupProgress(Popup):
    def __init__(self, **kwargs):
        super(PopupProgress, self).__init__(**kwargs)

        # Set Label
        self.label = Label()
        self.label.font_size = '200dp'
        self.content = self.label

    def start_progress(self, count):
        # Seconds before Dismiss
        self.count = count

        # Set base text
        self.label.text = str(self.count)

        # Call text changer
        Clock.schedule_once(self.change_progress_text_value, 1)

    def change_progress_text_value(self, instance):
        # Discrement second counter
        self.count -= 1

        # Modify text content
        if self.count != 0:
            # Change current text
            self.label.text = str(self.count)

            # Recall method until count is equal to 0
            Clock.schedule_once(self.change_progress_text_value, 1)
        else:
            # Change current text
            self.label.text = 'SMILE'

            # Call dismiss_popup in 1 seconds
            Clock.schedule_once(self.dismiss, 1)
