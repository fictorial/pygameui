import pygame

import view
import theme
import callback
import listview
import scroll
import label
import button


class SelectView(view.View):
    """Drop - down selector with single selection support.

    callback.Signals:
        on_list_opened(selectview, yesno) -> list opened / closed
        on_selection_changed(selectview, item, index) -> item selected
    """

    def __init__(self, frame, items):
        """items: list of views; str(item) used for selection display"""

        assert len(items) > 0
        width = frame.w + theme.scrollbar_size
        height = theme.label_height
        view.View.__init__(self, pygame.Rect(frame.topleft, (width, height)))
        self.on_selection_changed = callback.Signal()
        self.on_list_opened = callback.Signal()

        width = frame.w + theme.scrollbar_size - theme.font_size
        self.top_label = label.Label(pygame.Rect(0, 0, width, height), '')
        self.top_label.halign = label.LEFT
        self.top_label.border_color = theme.border_color
        self.top_label.border_width = 1
        self.top_label.background_color = theme.view_background_color
        self.top_label.interactive = True
        self.top_label.on_mouse_down.connect(self.show_list)
        self.add_child(self.top_label)

        self.list_view = listview.ListView(pygame.Rect(0, 0, 0, 0), items)
        self.list_view.background_color = theme.view_background_color
        self.list_view.on_selected.connect(self.selected)
        self.list_view.on_deselected.connect(self.deselected)

        top = self.top_label.frame.bottom - 1
        self.scroll_view = scroll.ScrollView(
            pygame.Rect(0, top, frame.w, 80),
            self.list_view)
        self.scroll_view.hidden = True
        self.add_child(self.scroll_view)

        left = frame.w + theme.scrollbar_size - height
        self.disclosure = button.Button(pygame.Rect(
            left, 0, height, height), '')
        self.disclosure.on_clicked.connect(self._toggle_show_list)
        self.add_child(self.disclosure)

    def show_list(self, show=True, *args, **kwargs):
        if show:
            self.frame.h = (self.top_label.frame.h +
                            self.scroll_view.frame.h - 1)
            self.scroll_view.hidden = False
            self.bring_to_front()
        else:
            self.frame.h = theme.label_height
            self.scroll_view.hidden = True
        self.on_list_opened(self, show)
        self._relayout()

    def _toggle_show_list(self, *args, **kwargs):
        self.show_list(self.scroll_view.hidden)
        if not self.scroll_view.hidden:
            self.list_view.focus()

    def draw(self):
        if not view.View.draw(self):
            return False

        f = self.disclosure.frame
        if self.scroll_view.hidden:
            points = [(f.left + f.w // 4, f.h // 3),
                      (f.right - f.w // 4, f.h // 3),
                      (f.centerx, f.h - f.h // 3)]
        else:
            points = [(f.left + f.w // 4, f.h - f.h // 3),
                      (f.right - f.w // 4, f.h - f.h // 3),
                      (f.centerx, f.h // 3)]

        pygame.draw.polygon(self.surface, theme.gray_color, points)
        return True

    def selected(self, list_view, item, index):
        if isinstance(item, label.Label):
            item.background_color = theme.selected_background_color
            item.text_color = theme.selected_text_color
        self.top_label.text = str(item)
        self.top_label._relayout()
        self.show_list(False)
        self.on_selection_changed(self, item, index)

    def deselected(self, list_view, item, index):
        if isinstance(item, label.Label):
            item.background_color = theme.clear_color
            item.text_color = theme.text_color
        self.top_label.text = ''
