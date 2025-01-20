from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from src.utils.styles import apply_button_style
from src.utils.user_manager import UserManager

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.user_manager = UserManager()
        layout = BoxLayout(orientation='vertical', padding='40dp', spacing='20dp')
        
        # Title
        title = Label(
            text='Constat Auto - Connexion', 
            size_hint_y=0.2, 
            font_size='24sp'
        )
        
        # Username input
        self.username = TextInput(
            multiline=False,
            hint_text='Nom d\'utilisateur',
            size_hint_y=None,
            height='40dp'
        )
        
        # Password input
        self.password = TextInput(
            multiline=False,
            password=True,
            hint_text='Mot de passe',
            size_hint_y=None,
            height='40dp'
        )
        
        # Login button
        login_btn = Button(
            text='Se connecter',
            size_hint_y=None,
            height='48dp',
            on_press=self.do_login
        )
        apply_button_style(login_btn)
        
        signup_btn = Button(
            text='Créer un compte',
            size_hint_y=None,
            height='48dp',
            on_press=self.go_to_signup
        )
        apply_button_style(signup_btn)
        
        # Error message label (hidden by default)
        self.error_label = Label(
            text='',
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height='30dp'
        )
        
        layout.add_widget(title)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.error_label)
        layout.add_widget(login_btn)
        layout.add_widget(signup_btn)
        
        self.add_widget(layout)
    
    def do_login(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        success, message = self.user_manager.verify_user(username, password)
        
        if success:
            self.error_label.text = ''
            self.username.text = ''
            self.password.text = ''
            self.manager.current = 'home'
        else:
            self.error_label.text = message
    
    def go_to_signup(self, instance):
        self.manager.current = 'signup'