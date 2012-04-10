"""This is a 2-hour hack of a UI toolkit for Pygame.

I really needed something dead-simple for quick prototypes.

What's here:

- simple nested controls (parent-child)
- flags: interactive, enabled, hidden, selected
- search for "class" :-)

What's not here:

- no multiline labels with word-wrapping
- no fancy text editing (just backspace)
- no layouts (e.g. no autoresizing, no border layouts, etc.)
- no scroll views (I prefer direct-dragging like on iOS)
- no dirty-rect updates; redraws all controls each frame
- documentation (just read the source)

To theme, update the class attributes (e.g. bgcolor) before instantiation.

"""

AUTHOR = 'Brian Hammond <brian@fictorial.com>'
COPYRIGHT = 'Copyright (C) 2012 Fictorial LLC.'
LICENSE = 'MIT'

__version__ = '0.1.0'

import pygame
import colors

window = None

font_name = 'Helvetica,Arial'
font_size = 18
font, bold_font = None, None
large_font, large_bold_font = None, None


rect = pygame.Rect


class Signal(object):
    def __init__(self):
        self.slots = []

    def add(self, slot):
        self.slots.append(slot)

    def __call__(self, *args, **kwargs):
        for slot in self.slots:
            slot(*args, **kwargs)


class Control(object):
    bgcolor = (255, 255, 255)
    border_color = (200, 200, 200)

    def __init__(self):
        self._frame = rect(0, 0, 0, 0)
        self.bgcolor = Control.bgcolor
        self.border_color = Control.border_color
        self.border_width = 0
        self.padding = (0, 0)
        self.parent = None
        self.children = []
        self.interactive = True
        self.enabled = True
        self.hidden = False
        self.draggable = False
        self._selected = False
        self.on_mouse_down = Signal()
        self.on_mouse_up = Signal()
        self.on_drag = Signal()
        self.on_selected = Signal()
        self.on_focused = Signal()
        self.on_blurred = Signal()

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, new_frame):
        self._frame = new_frame
        self.layout()

    def layout(self):
        for child in self.children:
            child.layout()

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def remove_child(self, to_remove):
        for i, child in enumerate(self.children):
            if child == to_remove:
                del self.children[i]
                break

    def hit(self, pos):
        if not self._frame.collidepoint(pos):
            return None
        pos = (pos[0] - self.frame.left, pos[1] - self.frame.top)
        for child in reversed(self.children):
            if child.interactive and child.enabled:
                control = child.hit(pos)
                if control is not None:
                    return control
        return self

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self):
        surf = pygame.surface.Surface(self._frame.size)
        surf.fill(self.bgcolor)
        for child in self.children:
            if child.hidden:
                continue
            child_surf = child.draw()
            surf.blit(child_surf, child._frame.topleft)
            if (child.border_width is not None and
                child.border_width > 0):
                pygame.draw.rect(surf, child.border_color, child._frame,
                                 child.border_width)
        return surf

    def became_focused(self):
        self._border_width_before_focus = self.border_width
        self.border_width = 2
        self.on_focused()

    def became_blurred(self):
        self.border_width = self._border_width_before_focus
        self.on_blurred()

    def became_selected(self, yesno):
        self.on_selected(self, yesno)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, yesno):
        self._selected = yesno
        self.became_selected(yesno)

    def mouse_down(self, btn, pt):
        self.on_mouse_down(self, btn, pt)

    def mouse_up(self, btn, pt):
        self.on_mouse_up(self, btn, pt)

    def dragged(self, rel):
        self.on_drag(self, rel)

    def child_dragged(self, child, rel):
        pass

    def to_parent_point(self, point):
        return (point[0] + self.frame.topleft[0],
                point[1] + self.frame.topleft[1])

    def from_parent_point(self, point):
        return (point[0] - self.frame.topleft[0],
                point[1] - self.frame.topleft[1])

    def from_window_point(self, point):
        curr = self
        ancestors = [curr]
        while curr.parent:
            ancestors.append(curr.parent)
            curr = curr.parent
        for a in reversed(ancestors):
            point = a.from_parent_point(point)
        return point

    def to_window_point(self, point):
        curr = self
        while curr:
            point = curr.to_parent_point(point)
            curr = curr.parent
        return point

    def key_down(self, key, code):
        pass

    def key_up(self, key):
        pass

    @property
    def scene(self):
        curr = self
        while curr.parent is not None and not isinstance(curr.parent, Scene):
            curr = curr.parent
        return curr.parent


class Label(Control):
    text_color = (90, 95, 90)
    padding = (8, 8)
    selected_bgcolor = (200, 224, 200)
    bgcolor = Control.bgcolor

    def __init__(self, text=None):
        Control.__init__(self)
        self.interactive = False
        self.font = font
        self.text = text
        self.text_color = Label.text_color
        self.padding = Label.padding

    def size_of(self, text):
        return self.draw().get_size()

    def size_to_fit(self):
        self.frame.size = self.size_of(self.text)

    def draw(self):
        text_surf = self.font.render(self.text, True,
                                     self.text_color, self.bgcolor)
        size = text_surf.get_size()
        padded_size = (size[0] + self.padding[0] * 2,
                       size[1] + self.padding[1] * 2)
        surf = pygame.surface.Surface(padded_size)
        surf.fill(self.bgcolor)
        surf.blit(text_surf, self.padding)
        return surf

    def became_selected(self, yesno):
        Control.became_selected(self, yesno)
        if yesno:
            self.bgcolor = Label.selected_bgcolor
        else:
            self.bgcolor = Label.bgcolor


class Button(Control):
    bgcolor = (220, 220, 220)
    active_bgcolor = (200, 200, 200)
    border_width = 1
    border_color = (100, 100, 100)
    disabled_text_color = (128, 128, 128)

    def __init__(self, text):
        Control.__init__(self)
        self.border_width = Button.border_width
        self.border_color = Button.border_color
        self.label = Label(text)
        self.label.font = bold_font
        self.label.bgcolor = Button.bgcolor
        self.bgcolor = Button.bgcolor
        self.active_bgcolor = Button.active_bgcolor
        self.add_child(self.label)
        self.on_clicked = Signal()
        self.is_pressed = False

    def enable(self, yesno):
        self.enabled = yesno
        if self.enabled:
            self.label.text_color = Label.text_color
        else:
            self.label.text_color = Button.disabled_text_color

    def layout(self):
        Control.layout(self)
        self.label.frame.size = self.frame.size

    def size_to_fit(self):
        self.label.size_to_fit()
        self.frame.size = self.label.frame.size

    def mouse_down(self, btn, pt):
        Control.mouse_down(self, btn, pt)
        if self.enabled:
            self.label.bgcolor = self.active_bgcolor
            self.is_pressed = True

    def mouse_up(self, button, pt):
        Control.mouse_up(self, button, pt)
        self.label.bgcolor = self.bgcolor
        self.is_pressed = False
        self.on_clicked(self)


class List(Control):
    def __init__(self, labels):
        Control.__init__(self)
        self.border_width = 1
        self.labels = labels

        self._selected_index = None
        self.on_selection = Signal()

        self.container = Control()
        self.container.draggable = True
        self.container.on_mouse_down.add(self.container_down)
        self.container.on_mouse_up.add(self.container_up)

        y, w = 0, 0
        for text in labels:
            lbl = Label(text)
            lbl.frame.topleft = (0, y)
            size = lbl.size_of(text)
            y += size[1]
            w = max(w, size[0])
            lbl.size_to_fit()
            self.container.add_child(lbl)
        for child in self.container.children:
            child.frame.w = w
        self.container.frame.size = (w, y)
        self.add_child(self.container)

    def child_dragged(self, child, rel):
        self.container.frame.top += rel[1]
        self.container.frame.top = min(0, max(-self.container.frame.h,
                                              self.container.frame.top))
        self.container.frame.bottom = max(self.frame.h,
                                          self.container.frame.bottom)
        self.down_at = None  # any drag kills a click for selecting

    def container_down(self, control, mouse_button, mouse_pos):
        self.down_at = mouse_pos

    def container_up(self, control, mouse_button, mouse_pos):
        if self.down_at is None:
            return
        for i, child in enumerate(self.container.children):
            if child.frame.collidepoint(mouse_pos):
                self.selected_index = i
                return
        self.selected_index = None

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, index):
        child = self.container.children[index]
        child.selected = True
        if self._selected_index is not None:
            prev = self.container.children[self._selected_index]
            prev.selected = False
        self._selected_index = index
        self.on_selection(self, index)


class SliderThumb(Control):
    border_width = 1
    border_color = (128, 148, 128)
    bgcolor = (240, 240, 240)

    def __init__(self):
        Control.__init__(self)
        self.draggable = True
        self.bgcolor = SliderThumb.bgcolor
        self.border_width = SliderThumb.border_width
        self.border_color = SliderThumb.border_color


class SliderTrack(Control):
    def __init__(self):
        Control.__init__(self)


class Slider(Control):
    track_bgcolor = (245, 245, 245)
    value_color = (200, 224, 200)

    def __init__(self):
        Control.__init__(self)
        self.track = SliderTrack()
        self.track.bgcolor = Slider.track_bgcolor
        self.track.border_width = 1
        self.track.border_color = SliderThumb.border_color
        self.add_child(self.track)
        self.value_track = SliderTrack()
        self.value_track.bgcolor = Slider.value_color
        self.add_child(self.value_track)
        self.thumb = SliderThumb()
        self.add_child(self.thumb)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = min(1.0, max(0.0, new_value))

        thumb_w, thumb_h = self.frame.h // 2, self.frame.h

        if self.thumb is not None:
            thumb_x = min(self.frame.w - thumb_w,
                          max(0.0, self._value * self._frame.w - thumb_w // 2))
            self.thumb.frame = rect(thumb_x, 0, thumb_w, thumb_h)

        h = 10
        self.track.frame = rect(thumb_w // 2,
                                self._frame.h // 2 - h // 2,
                                self._frame.w - thumb_w, h)

        value_w = self._value * (self._frame.w - thumb_w -
                                 self.track.border_width * 2)
        if value_w > 0:
            self.value_track.frame = rect(thumb_w // 2 +
                                          self.track.border_width,
                                          self._frame.h // 2 - h // 2 +
                                          self.track.border_width,
                                          value_w,
                                          h - self.track.border_width * 2)
            self.value_track.hidden = False
        else:
            self.value_track.hidden = True

    def child_dragged(self, child, rel):
        assert child == self.thumb
        self.value += rel[0] / float(self.frame.w)


class Progress(Slider):
    def __init__(self):
        Slider.__init__(self)
        self.remove_child(self.thumb)
        self.thumb = None


class Checkbox(Control):
    check_color = (128, 128, 128)
    check_bgcolor = (244, 244, 244)
    check_padding = (4, 2)

    def __init__(self, text):
        Control.__init__(self)
        self.checkmark = Label(' ')
        self.checkmark.border_width = 1
        self.checkmark.font = bold_font
        self.checkmark.text_color = Checkbox.check_color
        self.checkmark.bgcolor = Checkbox.check_bgcolor
        self.checkmark.padding = Checkbox.check_padding
        self.add_child(self.checkmark)
        self.label = Label(text)
        self.add_child(self.label)
        self._checked = False
        self.on_checked = Signal()

    def size_to_fit(self):
        self.checkmark.text = 'X'
        self.checkmark.size_to_fit()
        self._set_checkmark()
        self.label.size_to_fit()
        self.label.frame.left = self.checkmark.frame.right
        self.label.frame.centery = self.checkmark.frame.centery
        self.frame.w = self.checkmark.frame.w + self.label.frame.w
        self.frame.h = self.checkmark.frame.h

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, yesno):
        self._checked = yesno
        self.on_checked(self, yesno)
        self._set_checkmark()

    def _set_checkmark(self):
        if self._checked:
            self.checkmark.text = 'X'
        else:
            self.checkmark.text = '   '

    def toggle(self):
        self.checked = not self.checked

    def mouse_up(self, button, pt):
        self.toggle()


class TextField(Control):
    prompt = '_'
    padding = (5, 2)

    def __init__(self):
        Control.__init__(self)
        self.label = Label('')
        self.label.padding = TextField.padding
        self.add_child(self.label)
        self.text = ''
        self.label.text = TextField.prompt
        self.max_len = None
        self.secure = False
        self.border_width = 1
        self.on_return = Signal()
        self.on_text_change = Signal()

    def layout(self):
        Control.layout(self)
        self.label.frame.size = self.frame.size

    def key_down(self, key, code):
        if key == pygame.K_BACKSPACE:
            self.text = self.text[0:-1]
        elif key == pygame.K_RETURN:
            self.on_return(self, self.text)
        else:
            try:
                self.text = '%s%s' % (self.text, str(code))
            except:
                pass
            self.on_text_change(self, self.text)

        if self.max_len is not None:
            self.text = self.text[0:self.max_len]

        if self.secure:
            self.label.text = '*' * len(self.text)

        self.label.text = self.text + TextField.prompt
        self.label.size_to_fit()

        if self.label.frame.right > self.frame.w - self.padding[0] * 2:
            self.label.frame.right = self.frame.w - self.padding[0] * 2
        else:
            self.label.frame.left = self.padding[0]

    def mouse_up(self, button, pt):
        self.scene.focus = self


class Image(Control):
    def __init__(self, filename):
        Control.__init__(self)
        self.image = pygame.image.load(filename).convert()

    def size_to_fit(self):
        self.frame.size = self.image.get_size()

    def draw(self):
        return self.image


class Flipbook(Control):
    def __init__(self, filename, subimage_size, delay=0.1):
        """Images must have equal-sized subimages in a single row."""
        Control.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.subimage_size = subimage_size
        self.subimage_count = self.image.get_size()[0] // subimage_size[0]
        self.index = 0
        self._update_subimage()
        self.delay = delay
        self.elapsed = 0

    def update(self, dt):
        Control.update(self, dt)
        self.elapsed += dt
        if self.elapsed > self.delay:
            self.index = (self.index + 1) % self.subimage_count
            self.elapsed = 0
            self._update_subimage()

    def _update_subimage(self):
        x = self.index * self.subimage_size[0]
        self.subimage = self.image.subsurface(rect((x, 0), self.subimage_size))

    def draw(self):
        return self.subimage


class Spinner(Flipbook):
    size = 24

    def __init__(self):
        Flipbook.__init__(self, 'spinner.png', (Spinner.size, Spinner.size))


class Alert(Control):
    bgcolor = (240, 240, 200)

    def __init__(self, message):
        Control.__init__(self)

        self.bgcolor = Alert.bgcolor

        self.message = Label(message)
        self.message.font = large_font
        self.message.size_to_fit()
        self.message.bgcolor = self.bgcolor
        self.add_child(self.message)

        self.btn = Button('OK')
        self.btn.size_to_fit()
        self.btn.on_clicked.add(lambda btn: self.dismiss())
        self.add_child(self.btn)

    def layout(self):
        self.btn.frame.centerx = self.frame.w // 2
        self.btn.frame.bottom = self.frame.h - 10
        self.message.frame.centerx = self.frame.w // 2
        self.message.frame.centery = (self.btn.frame.top // 2)

    def dismiss(self):
        self.scene.remove_child(self)

    def draw(self):
        surf = Control.draw(self)
        pygame.draw.line(surf, (200, 200, 160),
                         (0, self.frame.bottom - 1),
                         (self.frame.w, self.frame.bottom - 1), 2)
        return surf


class Scene(Control):
    def __init__(self):
        Control.__init__(self)
        self._frame = rect((0, 0), window.get_size())
        self._focus = None

    def key_down(self, key, code):
        if self._focus is not None:
            self._focus.key_down(key, code)

    def key_up(self, key):
        if self._focus is not None:
            self._focus.key_up(key)

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, new_focus):
        if self._focus != new_focus:
            if self._focus is not None:
                self._focus.became_blurred()
            self._focus = new_focus
            self._focus.became_focused()

    def show_alert(self, message):
        alert = Alert(message)
        alert.frame = rect(0, 0, self.frame.w, max(120, self.frame.h // 3))
        self.add_child(alert)


down_in = None


def process_event(scene, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        global down_in
        down_in = scene.hit(event.pos)
        if down_in is not None and not isinstance(down_in, Scene):
            down_in.mouse_down(event.button,
                               down_in.from_window_point(event.pos))
    elif event.type == pygame.MOUSEBUTTONUP:
        up_in = scene.hit(event.pos)
        if down_in == up_in:
            down_in.mouse_up(event.button,
                             down_in.from_window_point(event.pos))
        down_in = None
    elif event.type == pygame.MOUSEMOTION:
        if down_in is not None and down_in.draggable:
            if down_in.parent is not None:
                down_in.parent.child_dragged(down_in, event.rel)
            down_in.dragged(event.rel)
    elif event.type == pygame.KEYDOWN:
        scene.key_down(event.key, event.unicode)
    elif event.type == pygame.KEYUP:
        scene.key_up(event.key)


def run(scene_cls, window_size=(450, 450)):
    pygame.init()
    pygame.key.set_repeat(200, 50)

    global window
    window = pygame.display.set_mode(window_size)

    global font, bold_font
    font = pygame.font.SysFont(font_name, font_size)
    bold_font = pygame.font.SysFont(font_name, font_size, bold=True)

    global large_font, large_bold_font
    large_font = pygame.font.SysFont(font_name, font_size * 2)
    large_bold_font = pygame.font.SysFont(font_name, font_size * 2, bold=True)

    scene = scene_cls()

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and
                 event.key == pygame.K_ESCAPE)):
                running = False
            else:
                process_event(scene, event)

        if not running:
            break

        scene.update(dt)
        window.blit(scene.draw(), (0, 0))
        pygame.display.flip()
