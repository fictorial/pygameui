import pygame

import view
import render
import callback


HORIZONTAL = 0
VERTICAL = 1


SCROLLBAR_SIZE = 16


class ScrollbarThumbView(view.View):
    """Draggable thumb of a scrollbar."""

    def __init__(self, direction):
        size = SCROLLBAR_SIZE
        view.View.__init__(self, pygame.Rect(0, 0, size, size))
        self.direction = direction
        self.draggable = True

    def key_down(self, key, code):
        # Simulate mouse drag to scroll with keyboard.

        if self.direction == VERTICAL:
            if key == pygame.K_DOWN:
                self.mouse_drag((0, 0), (0, 1))
            elif key == pygame.K_UP:
                self.mouse_drag((0, 0), (0, - 1))
        else:
            if key == pygame.K_RIGHT:
                self.mouse_drag((0, 0), (1, 0))
            elif key == pygame.K_LEFT:
                self.mouse_drag((0, 0), (-1, 0))


class ScrollbarView(view.View):
    """A scrollbar."""

    def __init__(self, scroll_view, direction):
        """Create a scrollbar for the given scrollable view."""
        if direction == VERTICAL:
            height = scroll_view.frame.h - SCROLLBAR_SIZE
            frame = pygame.Rect(0, 0, SCROLLBAR_SIZE, height)
            frame.right = scroll_view.frame.w
        else:
            width = scroll_view.frame.w - SCROLLBAR_SIZE
            frame = pygame.Rect(0, 0, width, SCROLLBAR_SIZE)
            frame.bottom = scroll_view.frame.h
        view.View.__init__(self, frame)

        self.direction = direction
        self.scroll_view = scroll_view

        self.thumb = ScrollbarThumbView(self.direction)
        self.add_child(self.thumb)

    def layout(self):
        self._update_thumb()
        self.thumb.layout()
        view.View.layout(self)

    def _update_thumb(self):
        self.thumb.frame.top = max(0, self.thumb.frame.top)
        self.thumb.frame.bottom = min(self.frame.bottom,
                                      self.thumb.frame.bottom)
        self.thumb.frame.left = max(0, self.thumb.frame.left)
        self.thumb.frame.right = min(self.frame.right, self.thumb.frame.right)

        if self.direction == VERTICAL:
            self.thumb.frame.centerx = SCROLLBAR_SIZE // 2
        else:
            self.thumb.frame.centery = SCROLLBAR_SIZE // 2

        if self.direction == VERTICAL:
            self.frame.right = self.scroll_view.frame.w
            off_x = self.scroll_view._content_offset[0]
            off_y = self.thumb.frame.top / float(self.frame.h)
            self.scroll_view.set_content_offset(off_x, off_y)
            percentage = (self.scroll_view.frame.h /
                          float(self.scroll_view.content_view.frame.h))
            self.thumb.frame.h = self.frame.h * percentage
            # self.hidden = (percentage >= 1)
        else:
            self.frame.bottom = self.scroll_view.frame.h
            off_x = self.thumb.frame.left / float(self.frame.w)
            off_y = self.scroll_view._content_offset[1]
            self.scroll_view.set_content_offset(off_x, off_y)
            percentage = (self.scroll_view.frame.w /
                          float(self.scroll_view.content_view.frame.w))
            self.thumb.frame.w = self.frame.w * percentage
            self.hidden = (percentage >= 1)

        if (self.direction == VERTICAL and
            self.scroll_view.hscrollbar.hidden and
            not self.scroll_view.vscrollbar.hidden):
            self.frame.h = self.scroll_view.frame.h
        elif (self.direction == HORIZONTAL and
              self.scroll_view.vscrollbar.hidden and
              not self.scroll_view.hscrollbar.hidden):
            self.frame.w = self.scroll_view.frame.w

    def _child_dragged(self, child):
        assert child == self.thumb
        self.layout()

    # Jump to offset at clicked point; does not allow dragging
    # without reclicking thumb

    def mouse_down(self, button, point):
        if self.direction == VERTICAL:
            self.thumb.frame.top = point[1]
            self._update_thumb()
        else:
            self.thumb.frame.left = point[0]
            self._update_thumb()


class ScrollView(view.View):
    """A view that scrolls a content view

    Signals

        on_scrolled(scroll_view)
            content offset was updated.

    """

    def __init__(self, frame, content_view):
        width = frame.size[0] + SCROLLBAR_SIZE
        height = frame.size[1] + SCROLLBAR_SIZE
        rect = pygame.Rect(frame.topleft, (width, height))
        view.View.__init__(self, rect)

        self.on_scrolled = callback.Signal()

        self.content_view = content_view
        self._content_offset = (0, 0)
        self.add_child(self.content_view)

        self.hscrollbar = ScrollbarView(self, HORIZONTAL)
        self.vscrollbar = ScrollbarView(self, VERTICAL)
        self.add_child(self.hscrollbar)
        self.add_child(self.vscrollbar)

    def layout(self):
        self.hscrollbar.layout()
        self.vscrollbar.layout()
        view.View.layout(self)

    def set_content_offset(self, percent_w, percent_h,
                           update_scrollbar_size=True):

        self._content_offset = (min(1, max(0, percent_w)),
                                min(1, max(0, percent_h)))

        self.content_view.frame.topleft = (
            -self._content_offset[0] * self.content_view.frame.w,
            -self._content_offset[1] * self.content_view.frame.h)

        if update_scrollbar_size:
            self.vscrollbar.thumb.centery = percent_h * self.vscrollbar.frame.h
            self.hscrollbar.thumb.centerx = percent_w * self.hscrollbar.frame.w

        self.on_scrolled(self)

    def draw(self):
        if not view.View.draw(self):
            return False

        if not self.vscrollbar.hidden and not self.hscrollbar.hidden:
            hole = pygame.Rect(self.vscrollbar.frame.left,
                               self.vscrollbar.frame.bottom,
                               SCROLLBAR_SIZE,
                               SCROLLBAR_SIZE)
            render.fillrect(self.surface, self.hole_color, hole)

        return True
