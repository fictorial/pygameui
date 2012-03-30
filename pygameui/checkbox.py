import pygame

import view
import callback
import theme
import label


class Checkbox(view.View):
    """A checkbox.

    signals:
        on_checked(checkbox)
        on_unchecked(checkbox)

    """

    def __init__(self, frame, text):
        view.View.__init__(self, frame)

        self.checked = False

        check_size = frame.h
        self.check_label = label.Label(pygame.Rect(
            0, 0, check_size, check_size),
            ' ', font=theme.default_bold_font)
        self.check_label.interactive = True
        self.check_label.border_color = theme.light_gray_color
        self.check_label.border_width = 1
        self.check_label.background_color = theme.view_background_color
        self.check_label.on_mouse_down.connect(self._click_active)
        self.check_label.on_mouse_up.connect(self._click_done)
        self.check_label.on_blurred.connect(self._blurred)
        self.check_label.on_mouse_up.connect(self.toggle)
        self.add_child(self.check_label)

        self.label = label.Label(pygame.Rect(0, 0, 0, 0), text)
        self.label.interactive = True
        self.label.on_mouse_down.connect(self._click_active)
        self.label.on_mouse_up.connect(self._click_done)
        self.label.on_blurred.connect(self._blurred)
        self.label.on_mouse_up.connect(self.toggle)
        self.add_child(self.label)

        self.on_checked = callback.Signal()
        self.on_unchecked = callback.Signal()

    def _layout(self):
        view.View._layout(self)
        self.label.shrink_wrap()
        self.label.frame.left = self.check_label.frame.right + theme.padding
        self.label.frame.centery = self.check_label.frame.centery
        self.frame.w = self.label.frame.right
        self._update_surface()

    def appeared(self):
        view.View.appeared(self)
        self._relayout()

    # it is possible to click in the padding b / w check_label and label

    def mouse_up(self, button, point):
        view.View.mouse_up(self, button, point)
        self.toggle()

    def _click_active(self, lbl, mbtn, point):
        self.check_label.background_color = theme.focused_view_background_color

    def _click_done(self, lbl, mbtn, point):
        self.check_label.background_color = theme.view_background_color

    def _blurred(self):
        self.check_label.background_color = theme.view_background_color

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
