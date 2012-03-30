import slider
import theme


class ProgressView(slider.SliderView):
    """A progress bar whose progress is in range [0, 1]"""

    def __init__(self, frame):
        slider.SliderView.__init__(self, frame, slider.HORIZONTAL,
            0.0, 1.0, show_thumb=False)
        self.interactive = False
        self.set_progress(0)
        self.track.value_color = theme.progress_value_color

    def progress(self):
        return self._value

    def set_progress(self, value):
        assert 0.0 <= value <= 1.0
        self.set_value(value)
