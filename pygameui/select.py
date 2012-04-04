import pygame

import view
import theme
import callback
import listview
import scroll
import label
import button


class SelectView(view.View):
    """Drop-down selector with single selection support.

    Signals

        on_list_opened(select_view, yesno)
            list opened / closed

        on_selection_changed(select_view, item, index)
            item selected
    """

    def __init__(self, frame, items):
        """items: list of views; str(item) used for selection display"""
        assert len(items) > 0

        view.View.__init__(self, pygame.Rect(frame.topleft, (1, 1)))

        self.on_selection_changed = callback.Signal()
        self.on_list_opened = callback.Signal()

        self.top_label = label.Label(pygame.Rect(0, 0, 1, 1), '')
        self.top_label.halign = label.LEFT
        self.top_label._enabled = True
        self.top_label.on_mouse_down.connect(self.show_list)
        self.add_child(self.top_label)

        self.list_view = listview.ListView(pygame.Rect(0, 0, 1, 1), items)
        self.list_view.on_selected.connect(self.item_selected)
        self.list_view.on_deselected.connect(self.item_deselected)
        self.scroll_view = scroll.ScrollView(pygame.Rect(0, 0, 1, 1),
                                             self.list_view)
        self.scroll_view.hidden = True
        self.add_child(self.scroll_view)

        self.disclosure = button.Button(pygame.Rect(0, 0, 1, 1), caption='')
        self.disclosure.on_clicked.connect(self._toggle_show_list)
        self.add_child(self.disclosure)

    def layout(self):
        assert self.padding[0] == 0 and self.padding[1] == 0

        self.scroll_view.frame.top = self.top_label.frame.bottom - 1
        self.scroll_view.frame.h = 100
        self.scroll_view.frame.w = (self.list_view.frame.w +
                                    scroll.SCROLLBAR_SIZE)

        self.frame.w = self.scroll_view.frame.w

        if self.scroll_view.hidden:
            self.frame.h = theme.current.label_height
        else:
            self.frame.h = (self.top_label.frame.h +
                            self.scroll_view.frame.h - 1)

        self.disclosure.frame.w = theme.current.label_height
        self.disclosure.frame.h = theme.current.label_height
        self.disclosure.frame.right = self.scroll_view.frame.right

        self.top_label.frame.w = self.disclosure.frame.left
        self.top_label.frame.h = theme.current.label_height
        self.top_label.frame.topleft = (0, 0)

        self.list_view.layout()
        self.scroll_view.layout()
        self.top_label.layout()
        self.disclosure.layout()
        view.View.layout(self)

    def show_list(self, show=True, *args, **kwargs):
        self.list_view.focus()
        if show:
            self.scroll_view.hidden = False
            self.bring_to_front()
        else:
            self.scroll_view.hidden = True
        self.on_list_opened(self, show)
        self.layout()

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

        pygame.draw.polygon(self.surface,
                            self.disclosure_triangle_color,
                            points)
        return True

    def item_selected(self, list_view, item, index):
        item.state = 'selected'
        self.top_label.text = str(item)
        self.show_list(False)
        self.on_selection_changed(list_view, item, index)

    def item_deselected(self, list_view, item, index):
        item.state = 'normal'
        self.top_label.text = ''
        self.on_selection_changed(list_view, item, index)
