from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

def apply_button_style(button):
    button.background_color = (0.2, 0.6, 1, 1)
    button.background_normal = ''
    button.size_hint = (0.8, None)
    button.height = '48dp'
    button.pos_hint = {'center_x': 0.5}

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        title = Label(text='Constat Auto', size_hint_y=0.2, font_size='24sp')
        
        new_report_btn = Button(
            text='Nouveau Constat',
            on_press=self.new_report,
            size_hint_y=0.15
        )
        take_photo_btn = Button(
            text='Prendre Photos',
            on_press=self.take_photos,
            size_hint_y=0.15
        )
        draw_sketch_btn = Button(
            text='Faire un Croquis',
            on_press=self.draw_sketch,
            size_hint_y=0.15
        )
        view_reports_btn = Button(
            text='Voir Constats Sauvegardés',
            on_press=self.view_reports,
            size_hint_y=0.15
        )
        
        chat_btn = Button(
            text='Chat',
            on_press=self.go_to_chat,
            size_hint_y=0.15
        )
        apply_button_style(chat_btn)
        
        layout.add_widget(title)
        layout.add_widget(new_report_btn)
        layout.add_widget(take_photo_btn)
        layout.add_widget(draw_sketch_btn)
        layout.add_widget(view_reports_btn)
        layout.add_widget(chat_btn)
        self.add_widget(layout)

    def new_report(self, instance):
        self.manager.current = 'form'
        
    def take_photos(self, instance):
        self.manager.current = 'camera'
        
    def draw_sketch(self, instance):
        self.manager.current = 'sketch'
        
    def view_reports(self, instance):
        self.manager.current = 'reports'
        
    def go_to_chat(self, instance):
        self.manager.current = 'chat'
