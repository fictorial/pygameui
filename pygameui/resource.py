import pygame
import pkg_resources

import weakref
import logging


logger = logging.getLogger(__name__)


font_cache = weakref.WeakValueDictionary()
image_cache = weakref.WeakValueDictionary()
sound_cache = weakref.WeakValueDictionary()


package_name = 'pygameui'


def get_font(size, use_bold=False):
    filename = 'regular'
    if use_bold:
        filename = 'bold'
    key = '%s:%d' % (filename, size)
    try:
        font = font_cache[key]
    except KeyError:
        path = 'resources/fonts/%s.ttf' % filename
        path = pkg_resources.resource_filename(package_name, path)
        try:
            logger.debug('loading font %s' % path)
            font = pygame.font.Font(path, size)
        except pygame.error, e:
            logger.warn('failed to load font: %s: %s' % (path, e))
            backup_fonts = 'helvetica,arial'
            font = pygame.font.SysFont(backup_fonts, size, use_bold)
        else:
            font_cache[key] = font
    return font


def get_image(name):
    try:
        img = image_cache[name]
    except KeyError:
        path = 'resources/images/%s.png' % name
        path = pkg_resources.resource_filename(package_name, path)
        try:
            logger.debug('loading image %s' % path)
            img = pygame.image.load(path)
        except pygame.error, e:
            logger.warn('failed to load image: %s: %s' % (path, e))
            img = None
        else:
            img = img.convert_alpha()
            image_cache[path] = img
    return img


def scale_image(image, size):
    return pygame.transform.smoothscale(image, size)


def get_sound(name):
    class NoSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoSound()

    try:
        sound = sound_cache[name]
    except KeyError:
        path = 'resources/sounds/%s.ogg' % name
        path = pkg_resources.resource_filename(package_name, path)
        try:
            sound = pygame.mixer.Sound(path)
        except pygame.error, e:
            logger.warn('failed to load sound: %s: %s' % (path, e))
            sound = NoSound()
        else:
            sound_cache[path] = sound
    return sound
