"""Rudimentary theme support.

A pair of colors signifies a linear gradient.

"""

import asset


default_font = None
default_bold_font = None


clear_color = (0, 0, 0, 0)
black_color = (0, 0, 0)
white_color = (255, 255, 255)
near_white_color = (240, 240, 240)
gray_color = (128, 128, 128)
light_gray_color = (192, 192, 192)
dark_gray_color = (100, 100, 100)
highlight_color = (255, 255, 177)
accent_color = (227, 227, 159)
dark_accent_color = (77, 148, 83)
main_gradient_colors = (accent_color, (173, 222, 78))
scene_background_color = (near_white_color, white_color)
view_background_color = (white_color, near_white_color)
focused_view_background_color = main_gradient_colors
border_color = light_gray_color
text_color = dark_gray_color
text_shadow_color = white_color
selected_text_color = dark_accent_color
thumb_color = (white_color, light_gray_color)
focused_thumb_color = main_gradient_colors
scrollbar_background_color = near_white_color
selected_background_color = main_gradient_colors
slider_track_background_color = (near_white_color, white_color)
slider_value_color = main_gradient_colors
progress_value_color = main_gradient_colors
slider_border_color = light_gray_color
dialog_background_color = (white_color, light_gray_color)
alert_title_background_color = gray_color
button_background_color = (white_color, light_gray_color)
focused_button_background_color = accent_color
button_text_color = text_color

padding = 6
font_size = 16
min_font_size = 10
label_height = font_size + padding * 2
button_height = font_size + padding * 2
scrollbar_size = 18
shadow_size = 140
cursor_blink_duration = 450  # ms


def init():
    """Initialize theme support."""
    global default_font, default_bold_font
    default_font = asset.get_font(font_size)
    default_bold_font = asset.get_font(font_size, usebold=True)
