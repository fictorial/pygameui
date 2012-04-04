import pygame

import view
import callback
import label
import theme
import focus


class Checkbox(view.View):
    """A checkbox.

    Signals

        on_checked(checkbox)
        on_unchecked(checkbox)

    """

    def __init__(self, frame, text):
        view.View.__init__(self, frame)

        self.checked = False

        check_frame = pygame.Rect(0, 0, 1, 1)
        self.check_label = label.Label(check_frame, ' ')
        self.add_child(self.check_label)

        self.label = label.Label(pygame.Rect(0, 0, 1, 1), text)
        self.add_child(self.label)

        self.on_checked = callback.Signal()
        self.on_unchecked = callback.Signal()

    def layout(self):
        self.check_label.frame.topleft = self.padding
        check_size = theme.current.label_height - self.padding[1] * 2
        self.check_label.frame.w = check_size
        self.check_label.frame.h = check_size
        self.check_label.layout()

        self.label.shrink_wrap()
        margin = max(self.check_label.margin[0], self.label.margin[0])
        self.label.frame.top = self.padding[1]
        self.label.frame.left = self.check_label.frame.right + margin
        self.label.frame.h = check_size
        self.label.layout()

        self.frame.w = (self.check_label.frame.w + margin +
                        self.label.frame.w + self.padding[0] * 2)
        self.frame.h = theme.current.label_height

        view.View.layout(self)

    def mouse_up(self, button, point):
        view.View.mouse_up(self, button, point)
        self.toggle()
        focus.set(None)

    def toggle(self, *args, **kwargs):
        self.checked = not self.checked
        if self.checked:
            self.check_label.text = 'X'
            self.on_checked()
        else:
            self.check_label.text = ' '
            self.on_unchecked()

    def __repr__(self):
        return self.label.text
