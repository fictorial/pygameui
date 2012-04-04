import re

import view


CENTER = 0
LEFT = 1
RIGHT = 2
TOP = 3
BOTTOM = 4

WORD_WRAP = 0
CLIP = 1


class Label(view.View):
    """Multi-line, word-wrappable, uneditable text view.


    Attributes:

        halign

            CENTER, LEFT, or RIGHT. Horizontal alignment of
            text.

        valign

            CENTER, TOP, or BOTTOM. Vertical alignment of text.

        wrap_mode

            WORD_WRAP or CLIP. Determines how text is wrapped to
            fit within the label's frame width-wise. Text that
            is wrapped to multiple rendered lines is clipped at
            the bottom of the frame. After setting the text
            attribute, the text_size attribute may be used to
            resize the label's frame; also see shrink_wrap.

            Changing wrap_mode forces a redraw of the label.

        text

            The text to render.

            Changing the text forces a redraw of the label.


    Style attributes:

        Changing a style attribute does not automatically redraw
        text in the new style given that you will likely change
        a number of style attributes.  Call 'layout' when you
        have finished changing style attributes.

        Using a new theme automatically restylizes and thus redraws
        the text using the new theme's style attributes.

        text_color

            The color of the text.

        text_shadow_color

            The color of the fake text-shadow.

        text_shadow_offset

            The offset of the fake text-shadow in the form
            (dx, dy).

        font

            The font used for rendering the text.

        padding

            Horizontal and vertical spacing from the label's
            interior edges where text is rendered.

    """

    def __init__(self, frame, text,
                 halign=CENTER, valign=CENTER,
                 wrap=CLIP):

        view.View.__init__(self, frame)
        self.halign = halign
        self.valign = valign
        self._wrap_mode = wrap
        self._text = text
        self._enabled = False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.render()

    @property
    def wrap_mode(self):
        return self._wrap_mode

    @property
    def wrap_mode(self, mode):
        self._wrap_mode = mode
        self.render()

    def layout(self):
        self.render()
        view.View.layout(self)

    def render(self):
        """Force (re)draw the text to cached surfaces.
        """
        self._render(self._text)

    def _render(self, text):
        self.text_surfaces, self.text_shadow_surfaces = [], []

        if text is None or len(text) == 0:
            self._text = None
            self.text_size = (0, 0)
            return

        text = text.replace("\r\n", "\n").replace("\r", "\n")
        wants_shadows = (self.text_shadow_color is not None and
                         self.text_shadow_offset is not None)

        if self._wrap_mode == CLIP:
            self._text = re.sub(r'[\n\t]{2, }', ' ', text)
            self.text_size = self._render_line(self._text, wants_shadows)
        elif self._wrap_mode == WORD_WRAP:
            self._render_word_wrapped(text, wants_shadows)

    def _render_line(self, line_text, wants_shadows):
        line_text = line_text.strip()
        text_surface = self.font.render(line_text, True, self.text_color)
        self.text_surfaces.append(text_surface)
        if wants_shadows:
            text_shadow_surface = self.font.render(
                line_text, True, self.text_shadow_color)
            self.text_shadow_surfaces.append(text_shadow_surface)
        return text_surface.get_size()

    def _render_word_wrapped(self, text, wants_shadows):
        self._text = text
        self.text_size = [0, 0]

        line_width = 0
        max_line_width = self.frame.w - self.padding[0] * 2

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

    def shrink_wrap(self):
        """Tightly bound the current text respecting current padding."""

        self.frame.size = (self.text_size[0] + self.padding[0] * 2,
                           self.text_size[1] + self.padding[1] * 2)

    def _determine_top(self):
        if self.valign == TOP:
            y = self.padding[1]
        elif self.valign == CENTER:
            y = self.frame.h // 2 - self.text_size[1] // 2
        elif self.valign == BOTTOM:
            y = self.frame.h - self.padding[1] - self.text_size[1]
        return y

    def _determine_left(self, text_surface):
        w = text_surface.get_size()[0]
        if self.halign == LEFT:
            x = self.padding[0]
        elif self.halign == CENTER:
            x = self.frame.w // 2 - w // 2
        elif self.halign == RIGHT:
            x = self.frame.w - 1 - self.padding[0] - w
        return x

    def draw(self):
        if not view.View.draw(self) or not self._text:
            return False

        wants_shadows = (self.text_shadow_color is not None and
                         self.text_shadow_offset is not None)

        y = self._determine_top()

        for index, text_surface in enumerate(self.text_surfaces):
            x = self._determine_left(text_surface)

            if wants_shadows:
                text_shadow_surface = self.text_shadow_surfaces[index]
                top_left = (x + self.text_shadow_offset[0],
                            y + self.text_shadow_offset[1])
                self.surface.blit(text_shadow_surface, top_left)

            self.surface.blit(text_surface, (x, y))
            y += text_surface.get_size()[1]

        return True

    def __repr__(self):
        if self._text is None:
            return ''
        return self._text
