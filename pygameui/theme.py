from itertools import chain

import resource
from colors import *


class Theme(object):
    """A theme is a hierarchical set of view style attributes.

    Each view may have a set of attributes that control its
    visual style when rendered.  These style attributes are stored
    in a Theme.

    Style attributes are hierarchical in that a view class
    may override the style attribute of a parent view class.
    Also, a view class need not override all style attributes
    of a parent view class.

    For instance, let's say we define the default view background
    color to be gray and the border color to be black.

        a_theme.set(class_name='View',
                    state='normal',
                    key='background_color',
                    value=(128, 128, 128))

        a_theme.set(class_name='View',
                    state='normal',
                    key='border_color',
                    value=(0, 0, 0))

    Let's assume this is the only style information defined for View.
    Now, let's override the background color for a Button, add a
    style attribute for the text color, and leave the border color.

        a_theme.set(class_name='Button',
                    state='normal',
                    key='background_color',
                    value=(64, 64, 64))

        a_theme.set(class_name='Button',
                    state='normal',
                    key='text_color',
                    value=(128, 0, 0))

    When a view is stylized (see View.stylize), style attributes and
    values are queried in the current Theme and set on the view instance.

        b = Button()
        b.state = 'normal'
        b.stylize()

    The style attributes set on 'b' would be:

        background_color: (64, 64, 64)  from Button
        border_color: (0, 0, 0)         from View
        text_color: (128, 0, 0)         from Button

    Note that the 'key' is really a 'key path' which would allow you
    to style views contained in other views. For instance, an AlertView
    has a `title_label` which is a Label.  You may wish to style
    AlertView titles differently than other labels, and you can.  See
    the `light_theme` entry for `title_label`. Also see the `kvc` module
    for a simple form of Apple's Key-Value Coding for Python.

    """

    def __init__(self):
        self._styles = {}

    def set(self, class_name, state, key, value):
        """Set a single style value for a view class and state.

        class_name

            The name of the class to be styled; do not
            include the package name; e.g. 'Button'.

        state

            The name of the state to be stylized. One of the
            following: 'normal', 'focused', 'selected', 'disabled'
            is common.

        key

            The style attribute name; e.g. 'background_color'.

        value

            The value of the style attribute; colors are either
            a 3-tuple for RGB, a 4-tuple for RGBA, or a pair
            thereof for a linear gradient.

        """
        self._styles.setdefault(class_name, {}).setdefault(state, {})
        self._styles[class_name][state][key] = value

    def get_dict_for_class(self, class_name, state=None, base_name='View'):
        """The style dict for a given class and state.

        This collects the style attributes from parent classes
        and the class of the given object and gives precedence
        to values thereof to the children.

        The state attribute of the view instance is taken as
        the current state if state is None.

        If the state is not 'normal' then the style definitions
        for the 'normal' state are mixed-in from the given state
        style definitions, giving precedence to the non-'normal'
        style definitions.

        """
        classes = []
        klass = class_name

        while True:
            classes.append(klass)
            if klass.__name__ == base_name:
                break
            klass = klass.__bases__[0]

        if state is None:
            state = 'normal'

        style = {}

        for klass in classes:
            class_name = klass.__name__

            try:
                state_styles = self._styles[class_name][state]
            except KeyError:
                state_styles = {}

            if state != 'normal':
                try:
                    normal_styles = self._styles[class_name]['normal']
                except KeyError:
                    normal_styles = {}

                state_styles = dict(chain(normal_styles.iteritems(),
                                          state_styles.iteritems()))

            style = dict(chain(state_styles.iteritems(),
                               style.iteritems()))

        return style

    def get_dict(self, obj, state=None, base_name='View'):
        """The style dict for a view instance.

        """
        return self.get_dict_for_class(class_name=obj.__class__,
                                       state=obj.state,
                                       base_name=base_name)

    def get_value(self, class_name, attr, default_value=None,
                  state='normal', base_name='View'):
        """Get a single style attribute value for the given class.

        """
        styles = self.get_dict_for_class(class_name, state, base_name)
        try:
            return styles[attr]
        except KeyError:
            return default_value


current = None
light_theme = Theme()
dark_theme = Theme()


def use_theme(theme):
    """Make the given theme current.

    There are two included themes: light_theme, dark_theme.
    """
    global current
    current = theme
    import scene
    if scene.current is not None:
        scene.current.stylize()


def init_light_theme():
    color1 = (227, 227, 159)    # a light yellow
    color2 = (173, 222, 78)     # a light green
    color3 = (77, 148, 83)      # a dark green
    color4 = white_color
    color5 = near_white_color
    color6 = light_gray_color
    color7 = gray_color
    color8 = dark_gray_color
    color9 = black_color

    light_theme.set(class_name='View',
                    state='normal',
                    key='background_color',
                    value=(color4, color5))
    light_theme.set(class_name='View',
                    state='focused',
                    key='background_color',
                    value=(color1, color2))
    light_theme.set(class_name='View',
                    state='selected',
                    key='background_color',
                    value=(color1, color2))
    light_theme.set(class_name='View',
                    state='normal',
                    key='border_color',
                    value=color6)
    light_theme.set(class_name='View',
                    state='normal',
                    key='border_widths',
                    value=0)
    light_theme.set(class_name='View',
                    state='normal',
                    key='margin',
                    value=(6, 6))
    light_theme.set(class_name='View',
                    state='normal',
                    key='padding',
                    value=(0, 0))
    light_theme.set(class_name='View',
                    state='normal',
                    key='shadowed',
                    value=False)

    light_theme.set(class_name='Scene',
                    state='normal',
                    key='background_color',
                    value=(color5, color4))

    light_theme.set(class_name='Label',
                    state='normal',
                    key='text_color',
                    value=color8)
    light_theme.set(class_name='Label',
                    state='selected',
                    key='text_color',
                    value=color3)
    light_theme.set(class_name='Label',
                    state='normal',
                    key='text_shadow_color',
                    value=color4)
    light_theme.set(class_name='Label',
                    state='normal',
                    key='text_shadow_offset',
                    value=(0, 1))
    light_theme.set(class_name='Label',
                    state='normal',
                    key='padding',
                    value=(6, 6))
    light_theme.set(class_name='Label',
                    state='normal',
                    key='border_widths',
                    value=None)
    light_theme.set(class_name='Label',
                    state='normal',
                    key='font',
                    value=resource.get_font(16))

    light_theme.label_height = 16 + 6 * 2  # font size + padding above/below

    light_theme.set(class_name='Button',
                    state='normal',
                    key='background_color',
                    value=(color4, color6))
    light_theme.set(class_name='Button',
                    state='focused',
                    key='background_color',
                    value=color1)
    light_theme.set(class_name='Button',
                    state='normal',
                    key='text_color',
                    value=color8)
    light_theme.set(class_name='Button',
                    state='normal',
                    key='font',
                    value=resource.get_font(16, use_bold=True))
    light_theme.set(class_name='Button',
                    state='normal',
                    key='border_widths',
                    value=1)
    light_theme.set(class_name='Button',
                    state='normal',
                    key='border_color',
                    value=color6)

    light_theme.button_height = 16 + 6 * 2  # font size + padding above/below

    light_theme.set(class_name='ImageButton',
                    state='normal',
                    key='background_color',
                    value=(color4, color6))
    light_theme.set(class_name='ImageButton',
                    state='focused',
                    key='background_color',
                    value=color1)
    light_theme.set(class_name='ImageButton',
                    state='normal',
                    key='border_color',
                    value=color6)
    light_theme.set(class_name='ImageButton',
                    state='normal',
                    key='border_widths',
                    value=1)
    light_theme.set(class_name='ImageButton',
                    state='normal',
                    key='padding',
                    value=(6, 6))

    light_theme.set(class_name='ScrollbarThumbView',
                    state='normal',
                    key='background_color',
                    value=(color4, color6))
    light_theme.set(class_name='ScrollbarThumbView',
                    state='focused',
                    key='background_color',
                    value=(color1, color2))
    light_theme.set(class_name='ScrollbarThumbView',
                    state='normal',
                    key='border_widths',
                    value=1)

    light_theme.set(class_name='ScrollbarView',
                    state='normal',
                    key='background_color',
                    value=color5)
    light_theme.set(class_name='ScrollbarView',
                    state='normal',
                    key='border_widths',
                    value=(1, 1, 0, 0))   # t l b r

    light_theme.set(class_name='ScrollView',
                    state='normal',
                    key='hole_color',
                    value=whites_twin_color)
    light_theme.set(class_name='ScrollView',
                    state='normal',
                    key='border_widths',
                    value=1)

    light_theme.set(class_name='SliderTrackView',
                    state='normal',
                    key='background_color',
                    value=(color5, color4))
    light_theme.set(class_name='SliderTrackView',
                    state='normal',
                    key='value_color',
                    value=(color1, color2))
    light_theme.set(class_name='SliderTrackView',
                    state='normal',
                    key='border_widths',
                    value=1)

    light_theme.set(class_name='SliderView',
                    state='normal',
                    key='background_color',
                    value=clear_color)
    light_theme.set(class_name='SliderView',
                    state='normal',
                    key='border_widths',
                    value=None)

    light_theme.set(class_name='ImageView',
                    state='normal',
                    key='background_color',
                    value=None)
    light_theme.set(class_name='ImageView',
                    state='normal',
                    key='padding',
                    value=(0, 0))

    light_theme.set(class_name='Checkbox',
                    state='normal',
                    key='background_color',
                    value=clear_color)
    light_theme.set(class_name='Checkbox',
                    state='normal',
                    key='padding',
                    value=(0, 0))

    light_theme.set(class_name='Checkbox',
                    state='focused',
                    key='check_label.background_color',
                    value=(color1, color2))
    light_theme.set(class_name='Checkbox',
                    state='normal',
                    key='check_label.border_widths',
                    value=1)

    light_theme.set(class_name='Checkbox',
                    state='normal',
                    key='label.background_color',
                    value=clear_color)

    light_theme.set(class_name='SpinnerView',
                    state='normal',
                    key='border_widths',
                    value=None)

    light_theme.set(class_name='DialogView',
                    state='normal',
                    key='background_color',
                    value=(color4, color6))
    light_theme.set(class_name='DialogView',
                    state='normal',
                    key='shadowed',
                    value=True)

    light_theme.shadow_size = 140

    light_theme.set(class_name='AlertView',
                    state='normal',
                    key='title_label.background_color',
                    value=color7)
    light_theme.set(class_name='AlertView',
                    state='normal',
                    key='title_label.text_color',
                    value=color4)
    light_theme.set(class_name='AlertView',
                    state='normal',
                    key='title_label.text_shadow_offset',
                    value=None)
    light_theme.set(class_name='AlertView',
                    state='normal',
                    key='message_label.background_color',
                    value=clear_color)
    light_theme.set(class_name='AlertView',
                    state='normal',
                    key='font',
                    value=resource.get_font(16))
    light_theme.set(class_name='AlertView',
                    state='normal',
                    key='padding',
                    value=(6, 6))

    light_theme.set(class_name='NotificationView',
                    state='normal',
                    key='background_color',
                    value=(color1, color2))
    light_theme.set(class_name='NotificationView',
                    state='normal',
                    key='border_color',
                    value=color3)
    light_theme.set(class_name='NotificationView',
                    state='normal',
                    key='border_widths',
                    value=(0, 2, 2, 2))
    light_theme.set(class_name='NotificationView',
                    state='normal',
                    key='padding',
                    value=(0, 0))
    light_theme.set(class_name='NotificationView',
                    state='normal',
                    key='message_label.background_color',
                    value=clear_color)

    light_theme.set(class_name='SelectView',
                    state='normal',
                    key='disclosure_triangle_color',
                    value=color8)
    light_theme.set(class_name='SelectView',
                    state='normal',
                    key='border_widths',
                    value=1)
    light_theme.set(class_name='SelectView',
                    state='normal',
                    key='top_label.focusable',
                    value=False)

    light_theme.set(class_name='TextField',
                    state='focused',
                    key='label.background_color',
                    value=(color1, color2))
    light_theme.set(class_name='TextField',
                    state='normal',
                    key='placeholder_text_color',
                    value=color6)
    light_theme.set(class_name='TextField',
                    state='normal',
                    key='border_widths',
                    value=1)
    light_theme.set(class_name='TextField',
                    state='normal',
                    key='text_color',
                    value=color9)
    light_theme.set(class_name='TextField',
                    state='disabled',
                    key='text_color',
                    value=color6)
    light_theme.set(class_name='TextField',
                    state='normal',
                    key='blink_cursor',
                    value=True)
    light_theme.set(class_name='TextField',
                    state='normal',
                    key='cursor_blink_duration',
                    value=450)

    light_theme.set(class_name='GridView',
                    state='normal',
                    key='background_color',
                    value=color4)
    light_theme.set(class_name='GridView',
                    state='normal',
                    key='line_color',
                    value=color6)


def init_dark_theme():
    # TODO
    pass


def init():
    """Initialize theme support."""
    init_light_theme()
    init_dark_theme()
    use_theme(light_theme)
