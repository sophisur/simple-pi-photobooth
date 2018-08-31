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
        self.background_color = [255, 0, 255, 0]
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
            if self.count - 1 == 0:
                self.label.text = 'SMILE'
            else:
                self.label.text = str(self.count)

            # Recall method until count is equal to 0
            Clock.schedule_once(self.change_progress_text_value, 1)
        else:
            self.label.text = 'Click'
            Clock.schedule_once(self.dismiss, 0.2)


class PopupProgressFour(PopupProgress):
    def __init__(self, photomaton, **kwargs):
        super(PopupProgressFour, self).__init__(**kwargs)
        self.photomaton = photomaton

    def change_progress_text_value(self, instance):
        # Discrement second counter
        self.count -= 1

        # Modify text content
        if self.count != 0:
            if (self.count - 1) % 4 == 0:
                self.label.text = 'SMILE'
            elif self.count % 4 == 0:
                self.label.text = 'Click'
                self.photomaton.take_one_of_four_photo_action()
            else:
                self.label.text = str(self.count)

            # Recall method until count is equal to 0
            Clock.schedule_once(self.change_progress_text_value, 1)
        else:
            # Change current text
            self.label.text = ':)'
            self.photomaton.take_one_of_four_photo_action()

            # Call dismiss_popup in 1 seconds
            Clock.schedule_once(self.dismiss, 0.2)
