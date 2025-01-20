from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import datetime
from src.utils.styles import apply_button_style
from src.utils.pdf_generator import generate_report, generate_pdf_report

class AccidentViewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        main_layout = BoxLayout(orientation='vertical', spacing='10dp', padding='10dp')
        
        # En-tête avec la date et l'ID
        header = BoxLayout(size_hint_y=0.1)
        self.date_label = Label(text='Date: --')
        self.id_label = Label(text='ID: --')
        header.add_widget(self.date_label)
        header.add_widget(self.id_label)
        
        # Contenu scrollable
        scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', 
                                      spacing='10dp', 
                                      size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        # Boutons d'action
        actions = BoxLayout(size_hint_y=0.15, spacing='10dp')
        buttons = [
            ('📱 Partager', self.share_report),
            ('📄 PDF', self.generate_pdf),
            ('🗺️ Voir sur carte', self.show_map),
            ('⬅️ Retour', self.go_back)
        ]
        
        for text, callback in buttons:
            btn = Button(text=text)
            apply_button_style(btn)
            btn.bind(on_press=callback)
            actions.add_widget(btn)
        
        scroll.add_widget(self.content_layout)
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        main_layout.add_widget(actions)
        self.add_widget(main_layout)

    def load_accident(self, accident_data):
        self.content_layout.clear_widgets()
        
        # Mettre à jour les labels d'en-tête
        self.date_label.text = f"Date: {datetime.fromtimestamp(accident_data['timestamp'])}"
        self.id_label.text = f"ID: {accident_data['id']}"
        
        # Ajouter les détails
        sections = [
            ('📍 Localisation', accident_data.get('location', 'Non spécifié')),
            ('👥 Participants', accident_data.get('participants', [])),
            ('📝 Description', accident_data.get('description', 'Aucune description')),
        ]
        
        for title, content in sections:
            self.content_layout.add_widget(Label(
                text=f"{title}",
                size_hint_y=None,
                height='40dp',
                bold=True
            ))
            self.content_layout.add_widget(Label(
                text=str(content),
                size_hint_y=None,
                height='40dp'
            ))

        # Ajouter les photos
        if 'photos' in accident_data:
            self.content_layout.add_widget(Label(
                text='📸 Photos',
                size_hint_y=None,
                height='40dp',
                bold=True
            ))
            for photo in accident_data['photos']:
                img = Image(source=photo, size_hint_y=None, height='200dp')
                self.content_layout.add_widget(img)

        # Ajouter le croquis
        if 'sketch' in accident_data:
            self.content_layout.add_widget(Label(
                text='✏️ Croquis',
                size_hint_y=None,
                height='40dp',
                bold=True
            ))
            sketch = Image(source=accident_data['sketch'], 
                         size_hint_y=None, 
                         height='300dp')
            self.content_layout.add_widget(sketch)

    def share_report(self, instance):
        # Implémenter le partage
        pass

    def generate_pdf(self, instance):
        try:
            # Générer le PDF
            pdf_path = generate_pdf_report(self.current_accident_data)
            
            # Créer le popup de succès avec options
            content = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
            
            message = Label(
                text=f'PDF généré avec succès!\nEnregistré sous:\n{pdf_path}',
                size_hint_y=0.7,
                text_size=(300, None),
                halign='center'
            )
            
            buttons = BoxLayout(size_hint_y=0.3, spacing='10dp')
            
            open_btn = Button(text='Ouvrir')
            share_btn = Button(text='Partager')
            close_btn = Button(text='Fermer')
            
            open_btn.bind(on_press=lambda x: self.open_pdf(pdf_path))
            share_btn.bind(on_press=lambda x: self.share_pdf(pdf_path))
            
            for btn in [open_btn, share_btn, close_btn]:
                apply_button_style(btn)
                buttons.add_widget(btn)
            
            content.add_widget(message)
            content.add_widget(buttons)
            
            popup = Popup(
                title='PDF Généré',
                content=content,
                size_hint=(None, None),
                size=(400, 300)
            )
            
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
            
        except Exception as e:
            error_popup = Popup(
                title='Erreur',
                content=Label(text=f'Erreur lors de la génération du PDF:\n{str(e)}'),
                size_hint=(None, None),
                size=(400, 200)
            )
            error_popup.open()

    def open_pdf(self, pdf_path):
        import webbrowser
        webbrowser.open(pdf_path)

    def share_pdf(self, pdf_path):
        try:
            from plyer import share
            share.share(pdf_path)
        except:
            Popup(
                title='Partage',
                content=Label(text=f'Le fichier est disponible à:\n{pdf_path}'),
                size_hint=(None, None),
                size=(400, 200)
            ).open()

    def show_map(self, instance):
        # Afficher la carte
        pass

    def go_back(self, instance):
        self.manager.current = 'home'
