from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label  # Ajout de l'import manquant
from kivy.graphics import Color, Line, Rectangle, Ellipse, InstructionGroup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from functools import partial
import io
import os
from datetime import datetime

class DrawingWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = []
        self.undo_stack = []
        self.redo_stack = []
        self.current_tool = 'pen'  # 'pen', 'rectangle', 'circle', 'select'
        self.start_pos = None
        self.scale = 1
        self.translation = [0, 0]
        self.current_line = None
        self.line_color = (0, 0, 0, 1)
        self.line_width = 2
        self.background = InstructionGroup()
        self.bind(size=self.update_grid)
        self.draw_grid()

    def update_grid(self, *args):
        self.canvas.before.clear()
        self.draw_grid()

    def draw_grid(self):
        with self.canvas.before:
            # Fond blanc
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            # Grille
            Color(0.9, 0.9, 0.9, 1)
            grid_spacing = dp(20)
            for x in range(0, int(self.width), int(grid_spacing)):
                Line(points=[x, 0, x, self.height], width=0.5)
            for y in range(0, int(self.height), int(grid_spacing)):
                Line(points=[0, y, self.width, y], width=0.5)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.start_pos = touch.pos
            if self.current_tool == 'pen':
                with self.canvas:
                    Color(*self.line_color)
                    self.current_line = Line(points=[touch.x, touch.y], width=self.line_width)
                    self.lines.append((self.current_line, self.line_color, self.line_width))
            elif self.current_tool == 'rectangle':
                with self.canvas:
                    Color(*self.line_color)
                    self.current_shape = Rectangle(pos=touch.pos, size=(0, 0))
            elif self.current_tool == 'circle':
                with self.canvas:
                    Color(*self.line_color)
                    self.current_shape = Ellipse(pos=touch.pos, size=(0, 0))

    def on_touch_move(self, touch):
        if self.start_pos and self.collide_point(*touch.pos):
            if self.current_tool == 'pen':
                if self.current_line and self.collide_point(*touch.pos):
                    self.current_line.points += [touch.x, touch.y]
            elif self.current_tool in ['rectangle', 'circle']:
                # Update shape size based on drag
                size = (touch.x - self.start_pos[0], touch.y - self.start_pos[1])
                self.current_shape.size = size

    def clear_canvas(self, *args):  # Ajout de *args pour gérer les arguments supplémentaires
        self.canvas.clear()
        self.lines = []
        self.draw_grid()

    def add_text(self, text, pos):
        with self.canvas:
            Color(*self.line_color)
            # Utiliser Rectangle pour le texte (simplifié)
            # Dans une vraie application, utilisez Label avec canvas.add()
            Rectangle(pos=pos, size=(100, 30))

    def undo(self):
        if self.lines:
            self.redo_stack.append(self.lines.pop())
            self.redraw()

    def redo(self):
        if self.redo_stack:
            self.lines.append(self.redo_stack.pop())
            self.redraw()

    def redraw(self):
        self.canvas.clear()
        self.draw_grid()
        for line, color, width in self.lines:
            with self.canvas:
                Color(*color)
                self.canvas.add(line)

    def save_image(self):
        # Créer un dossier pour les sauvegardes s'il n'existe pas
        save_dir = os.path.join(os.path.expanduser('~'), 'ConstatAuto', 'sketches')
        os.makedirs(save_dir, exist_ok=True)
        
        # Générer un nom de fichier unique avec timestamp
        filename = f'sketch_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(save_dir, filename)
        
        # Sauvegarder l'image
        self.export_to_png(filepath)
        return filepath

class SketchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        main_layout = BoxLayout(orientation='horizontal', spacing='5dp', padding='5dp')
        
        # Créer d'abord le widget de dessin
        drawing_container = BoxLayout(padding='2dp')
        self.drawing_widget = DrawingWidget(size_hint=(1, 1))
        
        # Fond du conteneur de dessin
        with drawing_container.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(pos=drawing_container.pos, size=drawing_container.size)
        drawing_container.bind(pos=self._update_rect, size=self._update_rect)
        
        drawing_container.add_widget(self.drawing_widget)

        # Style des boutons
        button_style = {
            'size_hint_y': None,
            'height': '50dp',
            'background_normal': '',
            'background_color': (0.2, 0.6, 0.8, 1),
            'color': (1, 1, 1, 1),
            'bold': True,
            'font_size': '16sp',
        }
        
        # Barre d'outils
        tools_layout = BoxLayout(
            orientation='vertical',
            spacing='10dp',
            padding='10dp',
            size_hint=(0.2, 1)
        )
        
        with tools_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=tools_layout.pos, size=tools_layout.size)
        tools_layout.bind(pos=self._update_rect, size=self._update_rect)
        
        # Création des boutons après avoir créé drawing_widget
        buttons = [
            ('🎨 Couleur', self.show_color_picker),
            ('📏 Taille', self.show_width_slider),
            ('📝 Texte', self.add_text),
            ('🗑️ Effacer', lambda x: self.drawing_widget.clear_canvas()),
            ('💾 Sauvegarder', self.save_sketch),
            ('⬅️ Retour', self.go_back)
        ]
        
        for text, callback in buttons:
            btn = Button(text=text, **button_style)
            btn.bind(on_press=callback)
            tools_layout.add_widget(btn)

        # Nouveaux boutons pour les outils
        tools_buttons = [
            ('✏️ Crayon', lambda x: self.set_tool('pen')),
            ('⬜ Rectangle', lambda x: self.set_tool('rectangle')),
            ('⭕ Cercle', lambda x: self.set_tool('circle')),
            ('↩️ Annuler', lambda x: self.drawing_widget.undo()),
            ('↪️ Rétablir', lambda x: self.drawing_widget.redo()),
            ('🔍 Zoom', self.show_zoom_controls),
        ]

        for text, callback in tools_buttons:
            btn = Button(text=text, **button_style)
            btn.bind(on_press=callback)
            tools_layout.add_widget(btn)

        tools_layout.add_widget(Widget())  # Espacement flexible

        main_layout.add_widget(tools_layout)
        main_layout.add_widget(drawing_container)
        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        """Mettre à jour la position et la taille du rectangle de fond"""
        if hasattr(instance, 'canvas'):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                Rectangle(pos=instance.pos, size=instance.size)

    def show_color_picker(self, instance):
        popup = Popup(
            title='Choisir une couleur',
            content=ColorPicker(),
            size_hint=(None, None),
            size=(400, 400),
            background='atlas://data/images/defaulttheme/button'
        )
        popup.content.bind(color=lambda inst, val: self.set_color(val))
        popup.open()

    def show_width_slider(self, instance):
        slider = Slider(min=1, max=10, value=self.drawing_widget.line_width)
        popup = Popup(title='Épaisseur du trait',
                     content=slider,
                     size_hint=(0.8, 0.2))
        slider.bind(value=lambda inst, val: self.set_width(val))
        popup.open()

    def set_color(self, color):
        self.drawing_widget.line_color = color

    def set_width(self, width):
        self.drawing_widget.line_width = width

    def add_text(self, instance):
        text_input = TextInput(multiline=False)
        popup = Popup(title='Ajouter du texte',
                     content=text_input,
                     size_hint=(0.8, 0.2))
        text_input.bind(on_text_validate=lambda inst: self.drawing_widget.add_text(inst.text, (100, 100)))
        popup.open()

    def save_sketch(self, instance):
        filepath = self.drawing_widget.save_image()
        popup = Popup(
            title='Croquis sauvegardé',
            content=Label(
                text=f'Sauvegardé sous:\n{filepath}',
                text_size=(300, None),  # Ajout d'une taille maximale pour le texte
                halign='center'  # Centrer le texte
            ),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'home'

    def set_tool(self, tool_name):
        self.drawing_widget.current_tool = tool_name

    def show_zoom_controls(self, instance):
        content = BoxLayout(orientation='vertical')
        zoom_in = Button(text='Zoom +')
        zoom_out = Button(text='Zoom -')
        zoom_in.bind(on_press=lambda x: self.zoom(1.2))
        zoom_out.bind(on_press=lambda x: self.zoom(0.8))
        content.add_widget(zoom_in)
        content.add_widget(zoom_out)
        
        popup = Popup(
            title='Contrôles du zoom',
            content=content,
            size_hint=(None, None),
            size=(200, 200)
        )
        popup.open()

    def zoom(self, factor):
        self.drawing_widget.scale *= factor
        # Mettre à jour l'affichage avec le nouveau zoom
        self.drawing_widget.redraw()
