import pygame

import view
import asset


class ImageView(view.View):
    """Displays an image.

    The only content scaling mode currently supported is 'scale-to-fill'.

    """

    def __init__(self, frame, image):
        """Use a frame.size of (0, 0) to have it resized to
        the image's size

        """

        assert image is not None
        if frame.w == 0 and frame.h == 0:
            frame.size = image.get_size()
        view.View.__init__(self, frame)
        self.set_image(image)
        self.interactive = False
        self.background_color = None

    @staticmethod
    def view_for_image_named(image_name):
        """The view's frame size will match that of the given image"""

        image = asset.get_image(image_name)
        if not image:
            return None
        return ImageView(pygame.Rect((0, 0), image.get_size()), image)

    def set_image(self, image):
        """Sets the image displayed, scaling it to fit
        in the current frame.

        """

        self.surface = asset.scale_image(image, self.frame.size)
