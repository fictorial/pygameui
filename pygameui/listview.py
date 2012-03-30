import pygame

import view
import theme
import callback
import scroll


class ListView(view.View):
    """Vertical list of items with single - selection support.

    signals:
        on_selected(list_view, item, index)     -> item clicked
        on_deselected(list_view, item, index) -> item clicked when selected

    """

    def __init__(self, frame, items):
        """items: list of views"""

        view.View.__init__(self, frame)
        self.background_color = theme.view_background_color

        self.set_items(items)

        self.selected_index = None
        self.on_selected = callback.Signal()
        self.on_deselected = callback.Signal()

    def set_items(self, items):
        assert len(items) > 0

        for child in self.children:
            child.rm()

        self.items = items

        width, height = 0, 0
        for view in self.items:
            view.frame.topleft = (0, height)
            self.add_child(view)
            width = max(width, view.frame.w)
            height += view.frame.h
        self.frame = pygame.Rect(self.frame.topleft, (width, height))
        self._relayout()

    def deselect(self):
        if self.selected_index is not None:
            self.on_deselected(self, self.items[self.selected_index],
                self.selected_index)
        self.selected_index = None

    def select(self, index):
        self.deselect()
        self.selected_index = index

        if index is not None:
            item = self.items[self.selected_index]
            self.on_selected(self, item, index)

            if isinstance(self.parent, scroll.ScrollView):
                cy = item.frame.centery + self.frame.top
                if cy > self.parent.frame.h or cy < 0:
                    percentage = item.frame.top / float(self.frame.h)
                    self.parent.set_content_offset(
                        self.parent._content_offset[0],
                        percentage)

    def mouse_down(self, button, point):
        for index, child in enumerate(self.children):
            if point[1] >= child.frame.top and point[1] <= child.frame.bottom:
                self.select(index)
                break

    def key_down(self, key, code):
        index = self.selected_index

        if index is None:
            index = 0

        if key == pygame.K_DOWN:
            self.select(min(len(self.items) - 1, index + 1))
        elif key == pygame.K_UP:
            self.select(max(0, index - 1))
