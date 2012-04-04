import pygame

import view
import focus
import callback


class DialogView(view.View):
    """A non-modal dialog box.

    Signals

        on_dismissed(dialog)
    """

    def __init__(self, frame):
        view.View.__init__(self, frame)
        self.on_dismissed = callback.Signal()

    def dismiss(self):
        self.rm()
        focus.set(None)
        self.on_dismissed()

    def key_down(self, key, code):
        if key == pygame.K_ESCAPE:
            self.dismiss()
