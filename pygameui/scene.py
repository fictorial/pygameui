import view
import window
import focus


stack = []
current = None


def push(scene):
    global current
    stack.append(scene)
    current = scene
    current.appeared()
    focus.set(current)


def pop():
    global current

    if len(stack) > 0:
        current.disappeared()
        stack.pop()

    if len(stack) > 0:
        current = stack[-1]
        current.appeared()
        focus.set(current)


class Scene(view.View):
    """A view that takes up the entire window content area;
    scene space = window space.

    """

    def __init__(self):
        view.View.__init__(self, window.rect)

    def key_down(self, key, code):
        import pygame

        if key == pygame.K_ESCAPE:
            pop()
