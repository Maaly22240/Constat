import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from src.screens.camera_screen import CameraScreen
from src.screens.preview_screen import PreviewScreen
from src.screens.home_screen import HomeScreen
from src.screens.form_screen import FormScreen
from src.screens.sketch_screen import SketchScreen
from src.screens.reports_screen import ReportsScreen
from src.screens.login_screen import LoginScreen
from src.screens.chat_screen import ChatScreen
from src.screens.signup_screen import SignupScreen

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        # Add login screen first and set as default
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(PreviewScreen(name='preview'))
        sm.add_widget(FormScreen(name='form'))
        sm.add_widget(SketchScreen(name='sketch'))
        sm.add_widget(ReportsScreen(name='reports'))
        sm.add_widget(ChatScreen(name='chat'))
        
        # Set login as the initial screen
        sm.current = 'login'
        return sm

if __name__ == '__main__':
    MainApp().run()