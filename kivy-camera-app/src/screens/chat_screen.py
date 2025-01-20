from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Add back button
        back_button = Button(
            text='Retour',
            size_hint=(1, 0.1),
            on_press=self.go_back
        )
        
        # Chat messages area
        self.chat_area = TextInput(
            multiline=True, 
            readonly=True, 
            size_hint=(1, 0.7)  # Adjusted size to accommodate back button
        )
        
        # Message input and send button
        input_area = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.2)
        )
        self.message_input = TextInput(
            multiline=False,
            size_hint=(0.8, 1)
        )
        send_button = Button(
            text='Send',
            size_hint=(0.2, 1),
            on_press=self.send_message
        )
        
        input_area.add_widget(self.message_input)
        input_area.add_widget(send_button)
        
        layout.add_widget(back_button)  # Add back button first
        layout.add_widget(self.chat_area)
        layout.add_widget(input_area)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'home'
        
    def send_message(self, instance):
        message = self.message_input.text.strip()
        if message:
            self.chat_area.text += f'\nYou: {message}'
            self.message_input.text = ''