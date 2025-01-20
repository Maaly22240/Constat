from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import os
from src.styles import apply_button_style

class ReportsScreen(Screen):
    def __init__(self, **kwargs):
        super(ReportsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Titre
        title = Label(
            text='Constats Sauvegardés',
            size_hint_y=0.1,
            font_size='24sp'
        )
        
        # Zone de défilement pour la liste des rapports
        scroll_view = ScrollView(size_hint_y=0.8)
        self.reports_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.reports_layout.bind(minimum_height=self.reports_layout.setter('height'))
        scroll_view.add_widget(self.reports_layout)
        
        # Bouton retour
        back_btn = Button(
            text='Retour',
            size_hint_y=0.1,
            on_press=self.go_back
        )
        apply_button_style(back_btn)
        
        layout.add_widget(title)
        layout.add_widget(scroll_view)
        layout.add_widget(back_btn)
        self.add_widget(layout)
        
    def on_enter(self):
        self.load_reports()
        
    def load_reports(self):
        self.reports_layout.clear_widgets()
        reports_dir = '.'  # Dossier où sont stockés les PDFs
        for file in os.listdir(reports_dir):
            if file.startswith('constat_') and file.endswith('.pdf'):
                btn = Button(
                    text=file,
                    size_hint_y=None,
                    height='48dp'
                )
                apply_button_style(btn)
                btn.bind(on_press=lambda x, f=file: self.open_report(f))
                self.reports_layout.add_widget(btn)
                
    def open_report(self, filename):
        # Ouvrir le PDF avec l'application par défaut
        os.startfile(os.path.join('.', filename))
        
    def go_back(self, instance):
        self.manager.current = 'home'
