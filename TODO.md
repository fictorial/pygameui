# TO DO

## Priority 1

I really hate that I have to setup subviews in init then lay them out in layout;
better would be autoresizing support; or do not take frame as arg to ctors;
just set frame in layout.

## Enhancements

- Make a dark theme
- The only image view content scale mode supported is 'scale to fill'

## Views to create

- color picker (RGB, HSV; see `colorsys` module)
- modal dialogs
- file picker

## Bugs

- Alerts with message text that contains words that are too wide to be 
  wrapped cause layout problems. If a word is wider than the label's width
  and word wrap is enabled, do a character wrap for that word?
- Is scroll view showing all of content view? far right?
- When a list view is in a scroll view and the list view fits, the selected
  item does not extend to where the scrollbars are (hidden). For now, I am
  simply never hiding vertical scrollbars.

## Larger sub-projects

- Flipbook should not use resource.`get_image()` since that is for
  packaged images; or make `get_image` generic
- ScrollbarView should be decoupled from ScrollView; delegate
- No support for layouts; everything is placed in parent-relative coordinates;
  Add support for springs and struts auto-resizing ala UIKit.
- No high-level animation support (bounce, slide, fade, etc.)
- GUI builder tool that reads / writes pickles (versioning?)
- CPU utilization is bit high since all controls are redrawn every frame.
  I don't really care because this is really just for game prototypes.
- Support multiple windows
- Support resizable main window (after autoresizing is in place)

### Text Manipulation

- No support for text selection
- No cursor
- No support for copy / paste
- No key-bindings other than backspace and key input
