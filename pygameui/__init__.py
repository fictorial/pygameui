"""A simple GUI framework for Pygame.

This framework is not meant as a competitor to PyQt or other, perhaps more
formal, GUI frameworks. Instead, pygameui is but a simple framework for game
prototypes.

The app is comprised of a stack of scenes; the top-most or current scene is
what is displayed in the window. Scenes are comprised of Views which are
comprised of other Views. pygameui contains view classes for things like
labels, buttons, and scrollbars.

pygameui is a framework, not a library. While you write view controllers in the
form of scenes, pygameui will run the overall application by running a loop
that receives device events (mouse button clicks, keyboard presses, etc.) and
dispatches the events to the relevant view(s) in your scene(s).

Each view in pygameui is rectangular in shape and whose dimensions are
determined by the view's "frame". A view is backed by a Pygame surface.
Altering a view's frame requires that you call 'relayout' which will resize the
view's backing surface and give each child view a chance to reposition and/or
resize itself in response.

Events on views can trigger response code that you control. For instance, when
a button is clicked, your code can be called back. The click is a "signal" and
your code is a "slot". The view classes define various signals to which you
connect zero or more slots.

    a_button.on_clicked.connect(click_callback)

"""

AUTHOR = 'Brian Hammond <brian@fictorial.com>'
COPYRIGHT = 'Copyright (C) 2012 Fictorial LLC.'
LICENSE = 'MIT'

__version__ = '0.1.1'


import pygame

from alert import *
from button import *
from callback import *
from checkbox import *
from dialog import *
from flipbook import *
from grid import *
from imagebutton import *
from imageview import *
from label import *
from listview import *
from notification import *
from progress import *
from render import *
from resource import *
from scroll import *
from select import *
from slider import *
from spinner import *
from textfield import *
from view import *

import focus
import window
import scene
import theme

from scene import Scene


import logging
logger = logging.getLogger(__name__)


Rect = pygame.Rect
window_surface = None


def init(name='', window_size=(640, 480)):
    logger.debug('init %s %s' % (__name__, __version__))
    pygame.init()
    logger.debug('pygame %s' % pygame.__version__)
    pygame.key.set_repeat(200, 50)
    global window_surface
    window_surface = pygame.display.set_mode(window_size)
    pygame.display.set_caption(name)
    window.rect = pygame.Rect((0, 0), window_size)
    theme.init()


def run():
    assert len(scene.stack) > 0

    clock = pygame.time.Clock()
    down_in_view = None

    elapsed = 0

    while True:
        dt = clock.tick(60)

        elapsed += dt
        if elapsed > 5000:
            elapsed = 0
            logger.debug('%d FPS', clock.get_fps())

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()

            mousepoint = pygame.mouse.get_pos()

            if e.type == pygame.MOUSEBUTTONDOWN:
                hit_view = scene.current.hit(mousepoint)
                if hit_view is not None:
                    focus.set(hit_view)
                    down_in_view = hit_view
                    pt = hit_view.from_window(mousepoint)
                    hit_view.mouse_down(e.button, pt)
            elif e.type == pygame.MOUSEBUTTONUP:
                hit_view = scene.current.hit(mousepoint)
                if hit_view is not None:
                    if down_in_view and hit_view != down_in_view:
                        down_in_view.blurred()
                        focus.set(None)
                    pt = hit_view.from_window(mousepoint)
                    hit_view.mouse_up(e.button, pt)
                down_in_view = None
            elif e.type == pygame.MOUSEMOTION:
                if down_in_view and down_in_view.draggable:
                    pt = down_in_view.from_window(mousepoint)
                    down_in_view.mouse_drag(pt, e.rel)
                else:
                    scene.current.mouse_motion(mousepoint)
            elif e.type == pygame.KEYDOWN:
                if focus.view:
                    focus.view.key_down(e.key, e.unicode)
                else:
                    scene.current.key_down(e.key, e.unicode)
            elif e.type == pygame.KEYUP:
                if focus.view:
                    focus.view.key_up(e.key)
                else:
                    scene.current.key_up(e.key)

        scene.current.update(dt / 1000.0)
        scene.current.draw()
        window_surface.blit(scene.current.surface, (0, 0))
        pygame.display.flip()
