import pygame
import render
import theme
import callback
import resource
import focus


class View(object):
    """A rectangular portion of the window.

    Views may have zero or more child views contained within it.

    signals:
        on_mouse_down(view, button, point)
        on_mouse_up(view, button, point)
        on_mouse_motion(view, point)
        on_mouse_drag(view, point, delta)
        on_key_down(view, key, code)
        on_key_up(view, key)
        on_focused(view)
        on_blurred(view)
        on_removed(view) (from parent view)

    All mouse points passed to event methods and to slots are in local
    view coordinates. Use `to_parent` and `to_window` to convert.

    """

    def __init__(self, frame=None):
        self.frame = frame

        self.parent = None
        self.children = []  # back->front

        self.interactive = True
        self.hidden = False
        self.draggable = False

        self.background_color = theme.clear_color

        self.border_color = None
        self.border_width = 0

        self.shadowed = False
        self.shadow_image = None

        self.on_focused = callback.Signal()
        self.on_blurred = callback.Signal()
        self.on_mouse_up = callback.Signal()
        self.on_mouse_down = callback.Signal()
        self.on_mouse_motion = callback.Signal()
        self.on_mouse_drag = callback.Signal()
        self.on_key_down = callback.Signal()
        self.on_key_up = callback.Signal()
        self.on_removed = callback.Signal()

        self._update_surface()

    def _update_surface(self):
        if not self.frame:
            return

        if self.shadowed:
            shadowed_frame_size = (self.frame.w + theme.shadow_size,
                                   self.frame.h + theme.shadow_size)
            self.surface = pygame.Surface(
                shadowed_frame_size, pygame.SRCALPHA, 32)
            shadow_image = resource.get_image('shadow')
            self.shadow_image = resource.scale_image(
                shadow_image, shadowed_frame_size)
        else:
            self.surface = pygame.Surface(self.frame.size, pygame.SRCALPHA, 32)
            self.shadow_image = None

    def _relayout(self):
        self._update_surface()
        self._layout()

    def _layout(self):
        for child in self.children:
            child._layout()

    def sizetofit(self):
        rect = self.frame
        for child in self.children:
            rect = rect.union(child.frame)
        self.frame = rect
        self._relayout()

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def to_parent(self, point):
        return (point[0] + self.frame.topleft[0],
                point[1] + self.frame.topleft[1])

    def from_parent(self, point):
        return (point[0] - self.frame.topleft[0],
                point[1] - self.frame.topleft[1])

    def from_window(self, point):
        curr = self
        ancestors = [curr]
        while curr.parent:
            ancestors.append(curr.parent)
            curr = curr.parent
        for a in reversed(ancestors):
            point = a.from_parent(point)
        return point

    def to_window(self, point):
        curr = self
        while curr:
            point = curr.to_parent(point)
            curr = curr.parent
        return point

    def mouse_up(self, button, point):
        self.on_mouse_up(self, button, point)

    def mouse_down(self, button, point):
        self.on_mouse_down(self, button, point)

    def mouse_motion(self, point):
        self.on_mouse_motion(self, point)

    # only called on drag event if .draggable is True

    def mouse_drag(self, point, delta):
        self.on_mouse_drag(self, point, delta)

        self.frame.topleft = (self.frame.topleft[0] + delta[0],
                              self.frame.topleft[1] + delta[1])

        if self.parent:
            self.parent._child_dragged(self)

    def key_down(self, key, code):
        self.on_key_down(self, key, code)

    def key_up(self, key):
        self.on_key_up(self, key)

    def focus(self):
        focus.set(self)

    def has_focus(self):
        return focus.view == self

    def focused(self):
        self.on_focused()

    def blurred(self):
        self.on_blurred()

    def draw(self):
        """Do not call directly."""

        if self.hidden:
            return False

        if self.background_color is not None:
            render.fillrect(
                self.surface, self.background_color,
                rect=pygame.Rect((0, 0), self.frame.size))

        for child in self.children:
            if not child.hidden:
                child.draw()

                topleft = child.frame.topleft

                if child.shadowed:
                    shadow_topleft = (topleft[0] - theme.shadow_size // 2,
                                      topleft[1] - theme.shadow_size // 2)
                    self.surface.blit(child.shadow_image, shadow_topleft)

                self.surface.blit(child.surface, topleft)

                if child.border_color and child.border_width > 0:
                    pygame.draw.rect(self.surface, child.border_color,
                        child.frame, child.border_width)
        return True

    def hit(self, pt):
        """Find the view (self, child, or None) under the point `pt`."""

        if self.hidden or not self.interactive:
            return None

        if not self.frame.collidepoint(pt):
            return None

        local_pt = (pt[0] - self.frame.topleft[0],
                    pt[1] - self.frame.topleft[1])

        for child in reversed(self.children):
            view = child.hit(local_pt)
            if view is not None:
                return view

        return self

    def add_child(self, child):
        self.rm_child(child)
        self.children.append(child)
        child.parent = self
        child.appeared()

    def rm_child(self, child):
        for index, ch in enumerate(self.children):
            if ch == child:
                ch.on_removed()
                del self.children[index]
                break

    def rm(self):
        if self.parent:
            self.parent.rm_child(self)

    def iter_ancestors(self):
        curr = self
        while curr.parent:
            yield curr.parent
            curr = curr.parent

    def iter_children(self):
        for child in self.children:
            yield child

    def appeared(self):
        for child in self.children:
            child.appeared()

    def disappeared(self):
        for child in self.children:
            child.disappeared()

    def center(self):
        if self.parent is not None:
            self.frame.center = (self.parent.frame.w // 2,
                                 self.parent.frame.h // 2)

    def bring_to_front(self):
        if self.parent is not None:
            ch = self.parent.children
            index = ch.index(self)
            ch[-1], ch[index] = ch[index], ch[-1]

    def move_to_back(self):
        if self.parent is not None:
            ch = self.parent.children
            index = ch.index(self)
            ch[0], ch[index] = ch[index], ch[0]
