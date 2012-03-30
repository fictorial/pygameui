import pygame

import view
import theme
import focus


class DialogView(view.View):
    """A non-modal dialog box."""

    def __init__(self, frame):
        view.View.__init__(self, frame)
        self.background_color = theme.dialog_background_color
        self.border_color = theme.border_color
        self.border_width = 1
        self.shadowed = True
        self._update_surface()

    def appeared(self):
        view.View.appeared(self)
        self.center()
        self.focus()

    def dismiss(self):
        self.rm()
        focus.set(None)

    def key_down(self, key, code):
        if key == pygame.K_ESCAPE:
            self.dismiss()
