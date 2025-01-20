from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from src.utils.user_manager import UserManager
from kivy.clock import Clock

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        self.user_manager = UserManager()
        layout = BoxLayout(orientation='vertical', padding='40dp', spacing='20dp')
        
        title = Label(text='Inscription', size_hint_y=0.2, font_size='24sp')
        
        self.username = TextInput(
            multiline=False,
            hint_text='Nom d\'utilisateur',
            size_hint_y=None,
            height='40dp'
        )
        
        self.email = TextInput(
            multiline=False,
            hint_text='Email',
            size_hint_y=None,
            height='40dp'
        )
        
        self.password = TextInput(
            multiline=False,
            password=True,
            hint_text='Mot de passe',
            size_hint_y=None,
            height='40dp'
        )
        
        self.confirm_password = TextInput(
            multiline=False,
            password=True,
            hint_text='Confirmer mot de passe',
            size_hint_y=None,
            height='40dp'
        )
        
        signup_btn = Button(
            text='S\'inscrire',
            size_hint_y=None,
            height='48dp',
            on_press=self.do_signup
        )
        
        back_btn = Button(
            text='Retour à la connexion',
            size_hint_y=None,
            height='48dp',
            on_press=self.go_to_login
        )
        
        self.error_label = Label(
            text='',
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height='30dp'
        )
        
        for widget in [title, self.username, self.email, self.password, 
                      self.confirm_password, self.error_label, signup_btn, back_btn]:
            layout.add_widget(widget)
        
        self.add_widget(layout)
    
    def do_signup(self, *args):
        username = self.username.text.strip()
        password = self.password.text.strip()
        confirm_password = self.confirm_password.text.strip()
        email = self.email.text.strip()

        # Debug prints for form values
        print("Form Values:")
        print(f"Username field: '{username}'")
        print(f"Password field: '{password}'")
        print(f"Confirm field: '{confirm_password}'")
        
        success, message = self.user_manager.register_user(
            username=username,
            password=password,
            confirm_password=confirm_password,
            email=email
        )
        
        self.error_label.text = message
        if success:
            # Clear fields
            self.username.text = ''
            self.password.text = ''
            self.confirm_password.text = ''
            self.email.text = ''
            # Retour à la page de connexion après 2 secondes
            Clock.schedule_once(lambda dt: self.go_to_login(None), 2)
    
    def go_to_login(self, instance):
        self.manager.current = 'login'
