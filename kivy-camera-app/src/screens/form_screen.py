from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime
from plyer import gps
from fpdf import FPDF
import os
from kivy.clock import Clock
from functools import partial
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class FormScreen(Screen):
    def __init__(self, **kwargs):
        super(FormScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        
        # En-tête avec date et heure
        self.header = BoxLayout(size_hint_y=0.1)
        self.date_label = Label(text=datetime.now().strftime('%Y-%m-%d %H:%M'))
        self.location_label = Label(text='Recherche position...')
        self.header.add_widget(self.date_label)
        self.header.add_widget(self.location_label)
        
        # Mise à jour de l'heure toutes les secondes
        Clock.schedule_interval(self.update_time, 1)
        
        # Initialisation GPS
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except:
            self.location_label.text = "GPS non disponible"

        # Form fields
        form = GridLayout(cols=2, spacing=10, size_hint_y=0.8)
        self.inputs = {}
        fields = [
            'Lieu', 'Nom Conducteur A', 'Assurance A', 'N° Police A',
            'Nom Conducteur B', 'Assurance B', 'N° Police B'
        ]
        
        for field in fields:
            form.add_widget(Label(text=field))
            self.inputs[field] = TextInput(multiline=False)
            form.add_widget(self.inputs[field])
        
        # Boutons
        buttons = BoxLayout(size_hint_y=0.1, spacing=10)
        save_btn = Button(text='Générer PDF', on_press=self.generate_pdf)
        photo_btn = Button(text='Photos', on_press=self.add_photos)
        back_btn = Button(text='Retour', on_press=self.go_back)
        
        buttons.add_widget(back_btn)
        buttons.add_widget(photo_btn)
        buttons.add_widget(save_btn)
        
        layout.add_widget(self.header)
        layout.add_widget(form)
        layout.add_widget(buttons)
        self.add_widget(layout)

    def update_time(self, dt):
        self.date_label.text = datetime.now().strftime('%Y-%m-%d %H:%M')

    def on_location(self, **kwargs):
        self.location_label.text = f"GPS: {kwargs['lat']:.5f}, {kwargs['lon']:.5f}"

    def generate_pdf(self, instance):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Titre
        pdf.cell(0, 10, 'Constat Automobile', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        
        # Date et position
        pdf.cell(0, 10, f"Date: {self.date_label.text}", 0, 1)
        pdf.cell(0, 10, f"Position: {self.location_label.text}", 0, 1)
        
        # Informations du formulaire
        for field, input in self.inputs.items():
            pdf.cell(0, 10, f"{field}: {input.text}", 0, 1)
        
        # Photos
        photos_dir = 'photos'
        if os.path.exists(photos_dir):
            pdf.add_page()
            pdf.cell(0, 10, 'Photos:', 0, 1)
            for photo in os.listdir(photos_dir):
                if photo.endswith('.png'):
                    pdf.image(os.path.join(photos_dir, photo), x=10, w=190)
        
        # Sauvegarde du PDF
        pdf_path = f'constat_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        pdf.output(pdf_path)
        
        # Envoi par email
        self.send_pdf_to_admin(pdf_path)

    def send_pdf_to_admin(self, pdf_path):
        try:
            msg = MIMEMultipart()
            msg['From'] = "votre_email@gmail.com"
            msg['To'] = "admin@example.com"
            msg['Subject'] = f"Nouveau constat - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            with open(pdf_path, "rb") as f:
                pdf = MIMEApplication(f.read(), _subtype="pdf")
                pdf.add_header('Content-Disposition', 'attachment', filename=pdf_path)
                msg.attach(pdf)
            
            # Configuration SMTP (à adapter selon votre serveur mail)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("votre_email@gmail.com", "votre_mot_de_passe")
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            print(f"Erreur d'envoi: {e}")

    def add_photos(self, instance):
        self.manager.current = 'camera'

    def go_back(self, instance):
        self.manager.current = 'home'
