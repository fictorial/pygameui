import pygame

import dialog
import label
import theme
import button


OK = 1
CANCEL = 2


class AlertView(dialog.DialogView):
    """A non-modal alert dialog box with a title, message, a set of
    buttons, and an optional image.

    """

    def __init__(self, title, message, buttons=0xFF):
        padding = theme.padding

        text_width = theme.default_bold_font.size('Cancel')[0]
        button_width = text_width + padding * 2
        buttons_width = button_width * 2 + padding * 3

        message_label = label.Label(pygame.Rect(
            padding, 0, buttons_width, 1),
            message, wrap_mode=label.WORDWRAP)
        message_label.shrink_wrap()
        size = (buttons_width,
                padding * 6 + theme.label_height +
                message_label.text_size[1] + theme.button_height)
        frame = pygame.Rect((0, 0), size)
        dialog.DialogView.__init__(self, frame)

        title_label = label.Label(pygame.Rect(
            padding, padding, frame.w - padding * 2, theme.label_height),
            title, text_color=theme.light_gray_color,
            font=theme.default_bold_font, text_shadow_color=None)
        title_label.background_color = theme.alert_title_background_color
        self.add_child(title_label)

        message_label.valign = label.TOP
        message_label.frame.top = title_label.frame.bottom + padding
        message_label.frame.centerx = size[0] // 2
        self.add_child(message_label)

        ok = button.Button(pygame.Rect(
            frame.w // 2 - button_width // 2,
            frame.bottom - theme.button_height - padding,
            button_width, theme.button_height), 'OK')
        ok.on_clicked.connect(self._dismiss)
        self.add_child(ok)

        if buttons & CANCEL:
            ok.frame.centerx = frame.w // 2 - button_width // 2 - padding // 2
            cancel = button.Button(pygame.Rect(
                frame.w // 2 + padding // 2,
                frame.bottom - theme.button_height - padding,
                button_width, theme.button_height), 'Cancel')
            cancel.on_clicked.connect(self._dismiss)
            self.add_child(cancel)

    def _dismiss(self, btn, mbtn):
        self.dismiss()

    def key_down(self, key, code):
        dialog.DialogView.key_down(self, key, code)

        if key == pygame.K_RETURN:  # ~ ok
            self.dismiss()
