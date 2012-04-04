import pygame

import view


class GridView(view.View):
    """A view which renders a uniform 2-D grid using solid lines."""

    def __init__(self, frame, spacing=50):
        view.View.__init__(self, frame)
        self.spacing = spacing

    def layout(self):
        view.View.layout(self)

    def draw(self):
        if not view.View.draw(self):
            return False

        for y in range(self.spacing, self.frame.h, self.spacing):
            pygame.draw.line(self.surface, self.line_color,
                             (0, y), (self.frame.w, y))

        for x in range(self.spacing, self.frame.w, self.spacing):
            pygame.draw.line(self.surface, self.line_color,
                             (x, 0), (x, self.frame.h))

        return True
