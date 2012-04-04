import pygame

import view
import callback
import imageview
import focus


class ImageButton(view.View):
    """A button that uses an image instead of a text caption.

    Signals

        on_clicked(button, mousebutton)

    """

    def __init__(self, frame, image):
        if frame is None:
            frame = pygame.Rect((0, 0), image.get_size())
        elif frame.w == 0 or frame.h == 0:
            frame.size = image.get_size()

        view.View.__init__(self, frame)

        self.on_clicked = callback.Signal()

        self.image_view = imageview.ImageView(pygame.Rect(0, 0, 0, 0), image)
        self.image_view._enabled = False
        self.add_child(self.image_view)

    def layout(self):
        self.frame.w = self.padding[0] * 2 + self.image_view.frame.w
        self.frame.h = self.padding[1] * 2 + self.image_view.frame.h
        self.image_view.frame.topleft = self.padding
        self.image_view.layout()
        view.View.layout(self)

    def mouse_up(self, button, point):
        focus.set(None)
        self.on_clicked(self, button)
