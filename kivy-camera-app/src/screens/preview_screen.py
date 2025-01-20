from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
import os

class PreviewScreen(Screen):
    def __init__(self, **kwargs):
        super(PreviewScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Image preview
        self.preview = Image()
        
        # Buttons layout
        button_layout = BoxLayout(size_hint_y=0.2)
        self.save_button = Button(text='Save', on_press=self.save_photo)
        self.reject_button = Button(text='Retake', on_press=self.reject_photo)
        
        button_layout.add_widget(self.reject_button)
        button_layout.add_widget(self.save_button)
        
        self.layout.add_widget(self.preview)
        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)
        
        self.temp_file = None

    def show_preview(self, image_path):
        self.temp_file = image_path
        self.preview.source = image_path
        
    def save_photo(self, instance):
        # Photo is already saved in the right place
        self.manager.current = 'camera'
        
    def reject_photo(self, instance):
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        self.manager.current = 'camera'
