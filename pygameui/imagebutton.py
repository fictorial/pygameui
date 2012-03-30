import pygame

import view
import theme
import callback
import imageview
import focus


class ImageButton(view.View):
    """A button that uses an image instead of a text caption.

    signals:
    on_clicked(button, mousebutton)

    """

    def __init__(self, frame, image):
        frame.size = (
            image.get_size()[0] + theme.padding * 2,
            image.get_size()[1] + theme.padding * 2)
        view.View.__init__(self, frame)
        self.on_clicked = callback.Signal()
        self.decorate()
        self.image_view = imageview.ImageView(pygame.Rect(0, 0, 0, 0), image)
        self.add_child(self.image_view)
        self.image_view.center()

    def decorate(self):
        """Add border and use standard button background coloring."""

        self.decorated = True
        self.border_width = 1
        self.border_color = theme.border_color
        self.background_color = theme.button_background_color

    def undecorate(self):
        """Remove border and do not use button background coloring."""

        self.decorated = False
        self.border_width = 0
        self.border_color = None
        self.background_color = None

    def focused(self):
        view.View.focused(self)
        if self.decorated:
            self.background_color = theme.focused_button_background_color

    def blurred(self):
        view.View.blurred(self)
        if self.decorated:
            self.background_color = theme.button_background_color

    def mouse_up(self, button, point):
        focus.set(None)
        self.on_clicked(self, button)

    def set_enabled(self, yesno):
        self.interactive = yesno
