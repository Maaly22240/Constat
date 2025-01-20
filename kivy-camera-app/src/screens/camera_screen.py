from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CoreImage
import os
from datetime import datetime
from src.styles import apply_button_style

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Caméra
        self.camera = Camera(play=False, size_hint_y=0.8)
        
        # Layout pour les boutons
        button_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        # Bouton retour
        self.back_button = Button(
            text='Retour',
            size_hint_x=0.5,
            on_press=self.go_back
        )
        apply_button_style(self.back_button)
        
        # Bouton capture
        self.capture_button = Button(
            text='Prendre Photo',
            size_hint_x=0.5,
            on_press=self.capture_photo
        )
        apply_button_style(self.capture_button)
        
        # Ajout des boutons au layout
        button_layout.add_widget(self.back_button)
        button_layout.add_widget(self.capture_button)
        
        # Assemblage final
        layout.add_widget(self.camera)
        layout.add_widget(button_layout)
        self.add_widget(layout)
        
        self.photo_dir = 'photos'
        if not os.path.exists(self.photo_dir):
            os.makedirs(self.photo_dir)

    def on_enter(self):
        self.camera.play = True

    def on_leave(self):
        self.camera.play = False

    def capture_photo(self, instance):
        if not self.camera.texture:
            return
        
        timestr = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(self.photo_dir, f'img_{timestr}.png')
        self.camera.export_to_png(file_path)
        
        # Show preview screen
        preview_screen = self.manager.get_screen('preview')
        preview_screen.show_preview(file_path)
        self.manager.current = 'preview'

    def go_back(self, instance):
        self.camera.play = False
        self.manager.current = 'form'  # ou 'home' selon d'où on vient