import flipbook
import resource


class SpinnerView(flipbook.FlipbookView):
    size = 24

    def __init__(self, frame):
        frame.size = (SpinnerView.size, SpinnerView.size)
        image = resource.get_image('spinner')
        flipbook.FlipbookView.__init__(self, frame, image)
