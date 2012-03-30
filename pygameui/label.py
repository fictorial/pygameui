import re

import view
import asset
import theme


CENTER = 0
LEFT = 1
RIGHT = 2
TOP = 3
BOTTOM = 4

WORDWRAP = 0
CLIP = 1


class Label(view.View):
    """Multi-line, word-wrappable uneditable text view.

    Text which can span wrap to multiple lines or whose font may be
    adjusted to fit a given width.

    halign -- CENTER, LEFT, or RIGHT. Horizontal alignment of text.
    valign -- CENTER, TOP, or BOTTOM. Vertical alignment of text.
    wrap_mode -- WORDWRAP or CLIP. Determines how text is wrapped to
                 fit within the label's frame width-wise. Text that is
                 wrapped to multiple rendered lines is clipped at the
                 bottom of the frame. After setting the text attribute,
                 the text_size attribute may be used to resize the
                 label's frame; also see shrink_wrap.
    auto_resize_font -- True means that the font is treated as a single
                        line and the label's font size is potentially
                        reduced such that the text is fit in the label's
                        frame width. The font will not be reduced to
                        a size smaller than min_font_size. When
                        auto_resize_font is True, the effective wrap_mode
                        is CLIP.
    min_font_size -- default 8
    padding -- a pair of internal horizontal and vertical space.

    """

    def __init__(self, frame, text,
                 text_color=theme.text_color,
                 text_shadow_color=theme.text_shadow_color,
                 font=theme.default_font,
                 padding=(theme.padding, theme.padding),
                 wrap_mode=CLIP):

        view.View.__init__(self, frame)
        self.font = font or theme.default_font
        self._padding = padding or theme.padding
        self.halign = CENTER
        self.valign = CENTER
        self.auto_resize_font = False
        self.wrap_mode = wrap_mode
        assert wrap_mode in (WORDWRAP, CLIP)
        self._text_color = text_color
        self.shadow_color = text_shadow_color
        self.shadow_offset = (0, 1)
        self.min_font_size = 8
        self.interactive = False
        self.background_color = theme.clear_color
        self.text = text

    def _resize_font_to_fit(self):
        current_font_size = self.font.get_height()
        while current_font_size > self.min_font_size:
            self.font = asset.getfont(current_font_size)
            size = self.font.size(self.text)
            padded_size = (size[0] + self._padding[0] * 2,
                           size[1] + self._padding[1] * 2)
            if padded_size[0] < self.frame.w:
                break
            current_font_size -= 1

    def _render_line(self, line_text, wants_shadows):
        line_text = line_text.strip()
        text_surface = self.font.render(line_text, True, self.text_color)
        self.text_surfaces.append(text_surface)
        if wants_shadows:
            text_shadow_surface = self.font.render(line_text, True,
                self.shadow_color)
            self.text_shadow_surfaces.append(text_shadow_surface)
        return text_surface.get_size()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._render(text)

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, color):
        self._text_color = color
        self._render(self._text)

    @property
    def padding(self):
        """(h,v) where h is horizontal internal padding and v is vertical"""
        return self._padding

    @padding.setter
    def padding(self, padding):
        self._padding = padding
        self._render(self._text)

    def _render_word_wrapped(self, text, wants_shadows):
        self._text = text
        self.text_size = [0, 0]

        line_width = 0
        max_line_width = self.frame.w - self._padding[0] * 2

        line_tokens = []
        tokens = re.split(r'(\s)', self._text)
        token_widths = {}

        for token in tokens:
            if len(token) == 0:
                continue

            token_width, _ = token_widths.setdefault(token,
                self.font.size(token))

            if token == '\n' or token_width + line_width >= max_line_width:
                line_size = self._render_line(''.join(line_tokens),
                    wants_shadows)
                self.text_size[0] = max(self.text_size[0], line_size[0])
                self.text_size[1] += line_size[1]

                if token == '\n':
                    line_tokens, line_width = [], 0
                else:
                    line_tokens, line_width = [token], token_width
            else:
                line_width += token_width
                line_tokens.append(token)

        if len(line_tokens) > 0:
            line_size = self._render_line(''.join(line_tokens),
                wants_shadows)
            self.text_size[0] = max(self.text_size[0], line_size[0])
            self.text_size[1] += line_size[1]

    def _render(self, text):
        self.text_surfaces, self.text_shadow_surfaces = [], []

        if text is None or len(text) == 0:
            self._text = None
            self.text_size = (0, 0)
            return

        text = text.replace("\r\n", "\n").replace("\r", "\n")
        wants_shadows = (self.shadow_color is not None and
                         self.shadow_offset is not None)

        if self.auto_resize_font or self.wrap_mode == CLIP:
            self._text = re.sub(r'[\n\t]{2, }', ' ', text)

            if self.auto_resize_font:
                self._resize_font_to_fit()

            self.text_size = self._render_line(self._text, wants_shadows)
        elif self.wrap_mode == WORDWRAP:
            self._render_word_wrapped(text, wants_shadows)

    def shrink_wrap(self):
        """Tightly bound the current text respecting current padding."""

        self.frame.size = (self.text_size[0] + self._padding[0],
                           self.text_size[1] + self._padding[1])

        self._update_surface()

    def _determine_top(self):
        if self.valign == CENTER:
            y = self.frame.h // 2 - self.text_size[1] // 2
        elif self.valign == TOP:
            y = self._padding[1]
        elif self.valign == BOTTOM:
            y = self.frame.h - self._padding[1] - self.text_size[1]
        return y
    
    def _determine_left(self, text_surface):
        w = text_surface.get_size()[0]
        if self.halign == CENTER:
            x = self.frame.w // 2 - w // 2
        elif self.halign == LEFT:
            x = self._padding[0]
        elif self.halign == RIGHT:
            x = self.frame.w - 1 - self._padding[0] - w
        return x

    def draw(self):
        if not view.View.draw(self) or not self.text:
            return False

        wants_shadows = (self.shadow_color is not None and
                         self.shadow_offset is not None)

        y = self._determine_top()

        for index, text_surface in enumerate(self.text_surfaces):
            x = self._determine_left(text_surface)

            if wants_shadows:
                text_shadow_surface = self.text_shadow_surfaces[index]
                topleft = (x + self.shadow_offset[0],
                           y + self.shadow_offset[1])
                self.surface.blit(text_shadow_surface, topleft)

            self.surface.blit(text_surface, (x, y))
            y += text_surface.get_size()[1]

        return True

    def __repr__(self):
        return self._text
