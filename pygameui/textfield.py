import pygame

import view
import label
import theme
import callback


class TextField(view.View):
    """Editable single line of text.

    There are no fancy keybindings; just backspace.

    signals:
    on_text_change(text_field, text)
    on_return(text_field, text)

    """

    def __init__(self, frame, text='', placeholder=''):
        view.View.__init__(self, frame)
        self.text = text or ''
        self.placeholder = placeholder
        self.padding = theme.padding
        self.label = label.Label(
            pygame.Rect((0, 0), frame.size),
            text or placeholder,
            font=theme.default_font)
        self.label.halign = label.LEFT
        self.add_child(self.label)
        self.enabled = True
        self.max_len = None
        self.secure = False
        self.border_color = theme.border_color
        self.border_width = 1
        self.blink_cursor = True
        self.background_color = theme.view_background_color
        self._update_text()
        self.on_return = callback.Signal()
        self.on_text_change = callback.Signal()

    def focused(self):
        view.View.focused(self)
        self._update_text()

    def blurred(self):
        view.View.blurred(self)
        self._update_text()

    def key_down(self, key, code):
        if not self.enabled:
            return

        if key == pygame.K_BACKSPACE:
            self.text = self.text[0:-1]
        elif key == pygame.K_RETURN:
            can_submit = True
            if self.placeholder and self.text == self.placeholder:
                can_submit = False
            if can_submit:
                self.on_return(self, self.text)
        else:
            try:
                self.text = '%s%s' % (self.text, str(code))
            except:
                pass
            self.on_text_change(self, self.text)

        if self.max_len:
            self.text = self.text[0:self.max_len]

        self._update_text()

        w = self.label.font.size(self.text)[0]
        if w > self.frame.w - self.padding * 2:
            self.label.frame.right = self.frame.w - self.padding * 2
        else:
            self.label.frame.left = self.padding

    def _update_text(self):
        if (len(self.text) == 0 and
            self.placeholder is not None and
            not self.has_focus()):
            self.label.text_color = theme.light_gray_color
            self.label.text = self.placeholder
        elif len(self.text) >= 0:
            self.label.text_color = theme.text_color
            self.label.text = self.text
        elif self.secure:
            self.label.text = ' * ' * len(self.text)

        if self.has_focus():
            self.background_color = theme.focused_view_background_color
        else:
            self.background_color = theme.view_background_color

    def draw(self):
        if not view.View.draw(self) or not self.has_focus():
            return False

        if (not self.blink_cursor or
            pygame.time.get_ticks() / theme.cursor_blink_duration % 2 == 0):
            size = self.label.font.size(self.text)
            rect = pygame.Rect(
                self.label.frame.left + self.label.padding[0] + size[0],
                self.label.frame.bottom - self.label.padding[1],
                10, 2)
            pygame.draw.rect(self.surface, theme.text_color, rect)
        return True

    def __repr__(self):
        return self.text
