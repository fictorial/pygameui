import pygame

import view
import render
import callback
import scroll


HORIZONTAL = 0
VERTICAL = 1


class SliderTrackView(view.View):
    "The track on which the thumb slides"

    def __init__(self, frame, direction):
        view.View.__init__(self, frame)
        self.direction = direction
        self.value_percent = 0.5

    def draw(self):
        if not view.View.draw(self):
            return False

        if self.value_percent > 0:
            t, l, b, r = self.get_border_widths()
            if self.direction == VERTICAL:
                w = self.frame.w - r - l
                h = self.value_percent * self.frame.h - b - t
                y = self.frame.h - b - h
            else:
                y = t
                w = self.value_percent * self.frame.w - r - l
                h = self.frame.h - b - t
            rect = pygame.Rect(l, y, w, h)
            render.fillrect(self.surface, self.value_color, rect=rect,
                            vertical=(self.direction == HORIZONTAL))

        return True


class SliderView(view.View):
    """Drag a thumb to select a value from a given range

    Signals
    on_value_changed(sliderview, value)

    """

    def __init__(self, frame, direction, low, high, show_thumb=True):
        view.View.__init__(self, frame)

        self.on_value_changed = callback.Signal()

        self.direction = direction
        self.low = min(low, high)
        self.high = max(low, high)

        self.thumb = scroll.ScrollbarThumbView(self.direction)
        self.thumb.hidden = (not show_thumb)
        self._add_track(show_thumb)
        self.add_child(self.thumb)

        self._value = None
        self.value = (low + high) / 2.0

    def _add_track(self, show_thumb):
        if self.direction == HORIZONTAL:
            trackh = self.thumb.frame.h - self.thumb.frame.h // 4
            offset = 0
            if show_thumb:
                offset = self.thumb.frame.w // 2
            trackrect = pygame.Rect(offset,
                                    self.frame.h // 2 - trackh // 2,
                                    self.frame.w - offset * 2, trackh)
        else:
            track_width = self.thumb.frame.w - self.thumb.frame.w // 4
            offset = 0
            if show_thumb:
                offset = self.thumb.frame.h // 2
            trackrect = pygame.Rect(self.frame.w // 2 - track_width // 2,
                                    offset, track_width,
                                    self.frame.h - offset * 2)
        self.track = SliderTrackView(trackrect, self.direction)
        self.add_child(self.track)

    @property
    def value(self):
        """value is in the range [low, high]"""
        return self._value

    @value.setter
    def value(self, val):
        self._set_value(val)

    def _set_value(self, val, update_thumb=True):
        if val == self._value:
            return

        self._value = max(self.low, min(self.high, val))
        self.track.value_percent = (val - self.low) / (self.high - self.low)

        if update_thumb:
            self._update_thumb()

        self.on_value_changed(self, self._value)

    def parented(self):
        self._update_thumb()

    def _update_thumb(self):
        if self.direction == VERTICAL:
            percentage = self._value / float(self.high - self.low)
            self.thumb.frame.centery = self.frame.h * percentage
        else:
            percentage = self._value / float(self.high - self.low)
            self.thumb.frame.centerx = self.frame.w * percentage

    def _child_dragged(self, child):
        assert child == self.thumb
        if self.direction == VERTICAL:
            self.thumb.frame.centerx = self.frame.w // 2
            self.thumb.frame.top = max(0, self.thumb.frame.top)
            self.thumb.frame.bottom = min(self.frame.h, self.thumb.frame.bottom)
            percent_px = self.thumb.frame.centery - self.thumb.frame.h // 2
            height = self.frame.h - self.thumb.frame.h
            t = percent_px / float(height)
            value = self.high + t * (self.low - self.high)
            self._set_value(value, False)
        else:
            self.thumb.frame.centery = self.frame.h // 2
            self.thumb.frame.left = max(0, self.thumb.frame.left)
            self.thumb.frame.right = min(self.frame.w, self.thumb.frame.right)
            percent_px = self.thumb.frame.centerx - self.thumb.frame.w // 2
            width = self.frame.w - self.thumb.frame.w
            t = percent_px / float(width)
            value = self.low + t * (self.high - self.low)
            self._set_value(value, False)
