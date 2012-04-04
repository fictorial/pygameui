import view
import window
import focus


stack = []
current = None


def push(scene):
    global current
    stack.append(scene)
    current = scene
    current.entered()
    focus.set(None)


def pop():
    global current

    if len(stack) > 0:
        current.exited()
        stack.pop()

    if len(stack) > 0:
        current = stack[-1]
        current.entered()

    focus.set(None)


class Scene(view.View):
    """A view that takes up the entire window content area."""

    def __init__(self):
        view.View.__init__(self, window.rect)

    def key_down(self, key, code):
        import pygame

        if key == pygame.K_ESCAPE:
            pop()

    def exited(self):
        pass

    def entered(self):
        self.stylize()
