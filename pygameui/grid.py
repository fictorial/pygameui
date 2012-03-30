import pygame

import view
import label
import theme


class GridView(view.View):
    """A view which renders a grid using lines."""

    def __init__(self, frame, spacing=50, line_color=theme.gray_color):
        view.View.__init__(self, frame)

        self.spacing = spacing
        self.line_color = line_color

        tl = label.Label(pygame.Rect(0, 0, 1, 1), 'TL')
        tl.shrink_wrap()
        self.add_child(tl)

        bl = label.Label(pygame.Rect(0, 0, 1, 1), 'BL')
        bl.shrink_wrap()
        bl.frame.bottomleft = (0, frame.h)
        self.add_child(bl)

        br = label.Label(pygame.Rect(0, 0, 1, 1), 'BR')
        br.shrink_wrap()
        br.frame.bottomright = (frame.w, frame.h)
        self.add_child(br)

        tr = label.Label(pygame.Rect(0, 0, 1, 1), 'TR')
        tr.shrink_wrap()
        tr.frame.topright = (frame.w, 0)
        self.add_child(tr)

        self.background_color = theme.white_color
        tl.background_color = self.background_color
        bl.background_color = self.background_color
        br.background_color = self.background_color
        tr.background_color = self.background_color

    def draw(self):
        if not view.View.draw(self):
            return False

        for y in range(0, self.frame.h, self.spacing):
            pygame.draw.line(
                self.surface, self.line_color,
                (0, y), (self.frame.w, y))

        for x in range(0, self.frame.w, self.spacing):
            pygame.draw.line(
                self.surface, self.line_color,
                (x, 0), (x, self.frame.h))

        return True
