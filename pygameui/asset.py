import os
import weakref
import pygame


fonts = weakref.WeakValueDictionary()
images = weakref.WeakValueDictionary()
sounds = weakref.WeakValueDictionary()


root = os.path.join('..', 'assets')


def get_font(size, usebold=False):
    regular_path = os.path.join(root, 'fonts', 'regular.ttf')
    bold_path = os.path.join(root, 'fonts', 'bold.ttf')

    path = regular_path
    if usebold:
        path = bold_path

    key = '%s:%d' % (path, size)
    try:
        font = fonts[key]
    except KeyError:
        try:
            font = pygame.font.Font(path, size)
        except pygame.error, e:
            print 'WARNING: failed to load font', path, e
            font = pygame.font.SysFont('helvetica,arial', size, usebold)
        else:
            fonts[key] = font
    return font


def get_image(name):
    path = os.path.join(root, 'images', '%s.png' % name)
    try:
        img = images[path]
    except KeyError:
        img = pygame.image.load(path)
        if not img:
            print 'WARNING: failed to load image', path
        img = img.convert_alpha()
        images[path] = img
    return img


def scale_image(image, size):
    return pygame.transform.smoothscale(image, size)


def get_sound(name):
    class NoSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoSound()

    path = os.path.join(root, 'sounds', '%s.wav' % name)

    try:
        sound = sounds[path]
    except KeyError:
        if os.path.exists(path):
            sound = pygame.mixer.Sound(path)
            sounds[path] = sound
        else:
            print 'WARNING: failed to load sound', path
            sound = NoSound()
    return sound
