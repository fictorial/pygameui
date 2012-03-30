import pygame

import view
import theme
import render
import callback


HORIZONTAL = 0
VERTICAL = 1


class ScrollbarThumbView(view.View):
    """Draggable thumb of a scrollbar."""

    def __init__(self, direction):
        size = theme.scrollbar_size
        view.View.__init__(self, pygame.Rect(0, 0, size, size))
        self.direction = direction
        self.draggable = True
        self.background_color = theme.thumb_color
        self.border_width = 1
        self.border_color = theme.border_color

    def focused(self):
        self.background_color = theme.focused_thumb_color

    def blurred(self):
        self.background_color = theme.thumb_color

    def key_down(self, key, code):
        """simulate mouse drag to scroll with keyboard"""

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
    """Ye olde scrollbar"""

    def __init__(self, scroll_view, direction):
        if direction == VERTICAL:
            height = scroll_view.frame.h - theme.scrollbar_size
            frame = pygame.Rect(0, 0, theme.scrollbar_size, height)
            frame.right = scroll_view.frame.w
        else:
            width = scroll_view.frame.w - theme.scrollbar_size
            frame = pygame.Rect(0, 0, width, theme.scrollbar_size)
            frame.bottom = scroll_view.frame.h
        view.View.__init__(self, frame)

        self.background_color = theme.scrollbar_background_color
        self.border_width = 1
        self.border_color = theme.border_color
        self.direction = direction
        self.scroll_view = scroll_view

        self.thumb = ScrollbarThumbView(self.direction)
        self.add_child(self.thumb)

    def appeared(self):
        self._update_offset()

    def _update_thumb(self):
        self.thumb.frame.top = max(0, self.thumb.frame.top)
        self.thumb.frame.bottom = min(self.frame.bottom,
                                      self.thumb.frame.bottom)
        self.thumb.frame.left = max(0, self.thumb.frame.left)
        self.thumb.frame.right = min(self.frame.right, self.thumb.frame.right)

        if self.direction == VERTICAL:
            overlap = 0
            if not self.scroll_view.hscrollbar.hidden:
                overlap = theme.scrollbar_size
            else:
                self.frame = pygame.Rect(
                    0, 0, theme.scrollbar_size, self.scroll_view.frame.h)
                self.frame.right = self.scroll_view.frame.w
                self._relayout()

            off_x = self.scroll_view._content_offset[0]
            off_y = self.thumb.frame.top / float(self.frame.h - overlap)
            self.scroll_view.set_content_offset(off_x, off_y)

            percentage = (self.scroll_view.frame.h /
                          float(self.scroll_view.content_view.frame.h))
            self.thumb.frame.h = self.frame.h * percentage
            # self.hidden = (percentage >= 1)
        else:
            overlap = 0
            if not self.scroll_view.vscrollbar.hidden:
                overlap = theme.scrollbar_size
            else:
                self.frame = pygame.Rect(0, 0,
                    self.scroll_view.frame.w,
                    theme.scrollbar_size)
                self.frame.bottom = self.scroll_view.frame.h
                self._relayout()

            off_x = self.thumb.frame.left / float(self.frame.w - overlap)
            off_y = self.scroll_view._content_offset[1]
            self.scroll_view.set_content_offset(off_x, off_y)

            percentage = (self.scroll_view.frame.w /
                          float(self.scroll_view.content_view.frame.w))
            self.thumb.frame.w = self.frame.w * percentage
            self.hidden = (percentage >= 1)
        self.thumb._relayout()  # w or h altered

    def _update_offset(self):
        if self.direction == VERTICAL:
            self.thumb.frame.centerx = theme.scrollbar_size // 2
        else:
            self.thumb.frame.centery = theme.scrollbar_size // 2
        self._update_thumb()

    def _child_dragged(self, child):
        assert child == self.thumb
        self._update_offset()

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
    """A view that contains another potentially larger view allowing scrolling
    via HORIZONTAL and / or VERTICAL scrollbar size.

    signals:
        on_scrolled(scroll_view) -> content offset updated

    """

    def __init__(self, frame, content_view):
        width = frame.size[0] + theme.scrollbar_size
        height = frame.size[1] + theme.scrollbar_size
        rect = pygame.Rect(frame.topleft, (width, height))
        view.View.__init__(self, rect)

        self.on_scrolled = callback.Signal()

        self.content_view = content_view
        self._content_offset = (0, 0)
        self.add_child(self.content_view)

        self.vscrollbar = ScrollbarView(self, VERTICAL)
        self.hscrollbar = ScrollbarView(self, HORIZONTAL)
        self.add_child(self.vscrollbar)
        self.add_child(self.hscrollbar)

        self.border_width = 1
        self.border_color = theme.border_color
        self.background_color = self.content_view.background_color

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

        if not self.vscrollbar.hidden or not self.hscrollbar.hidden:
            hole = pygame.Rect(
                self.vscrollbar.frame.left,
                self.vscrollbar.frame.bottom,
                theme.scrollbar_size,
                theme.scrollbar_size)
            render.fillrect(self.surface, theme.thumb_color, hole)

        return True
