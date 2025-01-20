def apply_button_style(button):
    button.background_color = (0.2, 0.6, 1, 1)  # Blue color
    button.background_normal = ''  # Remove default background
    button.size_hint = (0.8, None)
    button.height = '48dp'
    button.pos_hint = {'center_x': 0.5}
    button.background_down = button.background_normal
    button.color = (1, 1, 1, 1)  # White text

def apply_input_style(textinput):
    textinput.background_color = (0.95, 0.95, 0.95, 1)
    textinput.padding = [10, 10, 10, 10]
    textinput.size_hint_x = 0.8
    textinput.pos_hint = {'center_x': 0.5}
