import pygame

import view
import resource


class ImageView(view.View):
    """A view for displaying an image.

    The only 'content scaling mode' currently supported is 'scale-to-fill'.

    """

    def __init__(self, frame, image):
        """Create an image view from an image.

        frame.topleft -- where to position the view.
        frame.size -- if (0, 0) the frame.size is set to the image's size;
                      otherwise, the image is scaled to this size.

        """

        assert image is not None
        if frame.w == 0 and frame.h == 0:
            frame.size = image.get_size()
        view.View.__init__(self, frame)
        self.image = image
        self.interactive = False
        self.background_color = None

    @property
    def image(self):
        return self.surface

    @image.setter
    def image(self, image):
        self.surface = resource.scale_image(image, self.frame.size)


def view_for_image_named(image_name):
    """Create an ImageView for the given image."""

    image = resource.get_image(image_name)
    if not image:
        return None
    return ImageView(pygame.Rect((0, 0), image.get_size()), image)
