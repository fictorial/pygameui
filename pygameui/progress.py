import slider
import theme


class ProgressView(slider.SliderView):
    """A progress bar."""

    def __init__(self, frame):
        slider.SliderView.__init__(
            self, frame, slider.HORIZONTAL,
            0.0, 1.0, show_thumb=False)
        self.interactive = False
        self.progress = 0
        self.track.value_color = theme.progress_value_color

    @property
    def progress(self):
        """progress is in the range [0, 1]"""
        return self._value

    @progress.setter
    def progress(self, value):
        assert 0.0 <= value <= 1.0
        self.value = value
