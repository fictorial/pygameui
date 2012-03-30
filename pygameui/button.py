import label
import callback
import focus
import theme


class Button(label.Label):
    """A button with a text caption.

    signals:
        on_clicked(button, mousebutton)

    """

    def __init__(self, frame, caption):
        label.Label.__init__(
            self, frame, caption,
            text_color=theme.button_text_color,
            font=theme.default_bold_font)
        self.on_clicked = callback.Signal()
        self.interactive = True
        self.border_width = 1
        self.border_color = theme.border_color
        self.background_color = theme.button_background_color
        self.blurred()

    def mouse_up(self, button, point):
        focus.set(None)
        self.on_clicked(self, button)

    def set_enabled(self, yesno):
        self.interactive = yesno
        if yesno:
            self.text_color = theme.text_color
        else:
            self.text_color = theme.light_gray_color

    def focused(self):
        label.Label.focused(self)
        self.background_color = theme.focused_button_background_color

    def blurred(self):
        label.Label.blurred(self)
        self.background_color = theme.button_background_color
