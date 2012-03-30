import flipbook


class SpinnerView(flipbook.FlipbookView):
    size = 24

    def __init__(self, frame):
        frame.size = (SpinnerView.size, SpinnerView.size)
        flipbook.FlipbookView.__init__(self, frame, 'spinner')
