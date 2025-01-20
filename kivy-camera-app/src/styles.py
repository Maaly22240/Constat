from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex

def apply_button_style(button):
    # Couleurs modernes
    button.background_color = (0, 0, 0, 0)  # Transparent pour notre propre style
    button.color = get_color_from_hex('#FFFFFF')  # Texte blanc
    
    # Style du texte
    button.font_size = '18sp'
    button.bold = True
    
    # Padding et taille
    button.height = '48dp'
    button.padding = ('20dp', '10dp')
    
    def _update_rect(instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            # Couleur bleue moderne
            Color(*get_color_from_hex('#2196F3'))
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[24]  # Coins plus arrondis
            )
    
    button.bind(pos=_update_rect, size=_update_rect)
    _update_rect(button, None)  # Initial draw

    # Effets au survol et au clic
    button.background_normal = ''
    button.background_down = ''
    button.border = (0, 0, 0, 0)

    # Animation au clic
    def on_press(instance):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*get_color_from_hex('#1976D2'))  # Bleu plus foncé
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[24])

    def on_release(instance):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*get_color_from_hex('#2196F3'))  # Retour à la couleur normale
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[24])

    button.bind(on_press=on_press, on_release=on_release)
