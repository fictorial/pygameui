import pygame

import view
import callback
import scroll


class ListView(view.View):
    """Vertical list of items with single-selection support.

    Signals

        on_selected(list_view, item, index)
            item clicked

        on_deselected(list_view, item, index)
            item clicked when selected

    """

    def __init__(self, frame, items):
        """items: list of views"""
        frame.size = self._find_size_to_contain(items)
        view.View.__init__(self, frame)
        self.items = items
        self.selected_index = None
        self.on_selected = callback.Signal()
        self.on_deselected = callback.Signal()

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        for child in self.children:
            child.rm()

        w, h = 0, 0
        for item in new_items:
            item.frame.topleft = (0, h)
            self.add_child(item)
            w = max(w, item.frame.w)
            h += item.frame.h
        self.frame.size = (w, h)

        self._items = new_items

        if self.parent is not None:
            self.layout()

    def _find_size_to_contain(self, items):
        w, h = 0, 0
        for item in items:
            w = max(w, item.frame.w)
            h += item.frame.h
        return (w, h)

    def deselect(self):
        if self.selected_index is not None:
            self.items[self.selected_index].state = 'normal'
            self.on_deselected(self,
                               self.items[self.selected_index],
                               self.selected_index)
        self.selected_index = None

    def select(self, index):
        self.deselect()
        self.selected_index = index

        if index is not None:
            item = self.items[self.selected_index]
            item.state = 'selected'
            self.on_selected(self, item, index)

            if isinstance(self.parent, scroll.ScrollView):
                # auto-scroll container scroll view on new selection
                cy = item.frame.centery + self.frame.top
                if cy > self.parent.frame.h or cy < 0:
                    percentage = item.frame.top / float(self.frame.h)
                    self.parent.set_content_offset(
                        self.parent._content_offset[0], percentage)

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
