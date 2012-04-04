import pygame

import dialog
import label
import theme
import button
import window


OK = 1
CANCEL = 2


class AlertView(dialog.DialogView):
    """A non-modal alert dialog box."""

    def __init__(self, title, message, buttons=0xFF):
        dialog.DialogView.__init__(self, pygame.Rect(0, 0, 1, 1))

        self.title = title
        self.message = message
        self.buttons = buttons

        self.message_label = label.Label(pygame.Rect(0, 0, 1, 1),
            message, wrap=label.WORD_WRAP)
        self.message_label.valign = label.TOP
        self.add_child(self.message_label)

        self.title_label = label.Label(pygame.Rect(0, 0, 1, 1), title)
        self.add_child(self.title_label)

        self.ok = button.Button(pygame.Rect(0, 0, 0, 0), 'OK')
        self.ok.on_clicked.connect(self._dismiss)
        self.add_child(self.ok)

        self.cancel = button.Button(pygame.Rect(0, 0, 0, 0), 'Cancel')
        self.cancel.on_clicked.connect(self._dismiss)
        self.add_child(self.cancel)

    def layout(self):
        self.frame.w = max(100, window.rect.w // 3)
        self.frame.h = max(100, window.rect.h // 3)

        self.title_label.frame.topleft = self.padding
        self.title_label.frame.w = self.frame.w - self.padding[0] * 2
        self.title_label.frame.h = theme.current.label_height
        self.title_label.layout()

        self.message_label.frame.top = (self.title_label.frame.bottom +
                                        max(self.message_label.margin[1],
                                            self.title_label.margin[1]))
        self.message_label.frame.w = self.frame.w - self.padding[0] * 2
        self.message_label.render()
        self.message_label.shrink_wrap()
        self.message_label.frame.centerx = self.frame.w // 2

        assert self.ok.margin[1] == self.cancel.margin[1]

        self.ok.frame.h = theme.current.button_height
        self.cancel.frame.h = theme.current.button_height

        btn_top = (self.message_label.frame.bottom +
                   max(self.message_label.margin[1],
                       self.ok.margin[1]))
        self.ok.frame.top = btn_top
        self.cancel.frame.top = btn_top

        if self.buttons & CANCEL:
            self.cancel.hidden = False
            buttons_width = (self.ok.frame.w +
                             max(self.ok.margin[0], self.cancel.margin[0]) +
                             self.cancel.frame.w)

            self.ok.frame.centerx = self.frame.w // 2 - buttons_width // 2
            self.cancel.frame.centerx = self.frame.w // 2 + buttons_width // 2
        else:
            self.cancel.hidden = True
            self.ok.frame.centerx = self.frame.w // 2

        self.ok.layout()
        self.cancel.layout()

        self.frame.h = (self.padding[1] +
                        self.title_label.frame.h +
                        max(self.title_label.margin[1],
                            self.message_label.margin[1]) +
                        self.message_label.frame.h +
                        max(self.message_label.margin[1],
                            self.ok.margin[1]) +
                        self.ok.frame.h +
                        self.padding[1])

        dialog.DialogView.layout(self)

    def _dismiss(self, btn, mbtn):
        self.dismiss()

    def key_down(self, key, code):
        dialog.DialogView.key_down(self, key, code)
        if key == pygame.K_RETURN:  # ~ ok
            self.dismiss()


def show_alert(message, title='Info', buttons=OK):
    alert_view = AlertView(title, message, buttons)
    import scene
    scene.current.add_child(alert_view)
    alert_view.focus()
    alert_view.center()
