## TO BE DONE

- better theming support; perhaps lookup by classname and state
- gui builder tool that reads / writes pickles (versioning?)
- distribution on PyPi; where does one include images / sounds / etc.?
- github repo
- support autoresize child views; springs and struts? 

## KNOWN ISSUES

- CPU utilization is bit high since all controls are redrawn every frame.
  Doing lazy updates is "hard" so I haven't bothered yet. Patches welcome!
- No support for text selection and editing; no cursor
    - No support for copy / paste
- No support for layouts; everything is placed in parent-relative coordinates
- No high-level animation support (bounce, slide, fade, etc.)
- The only image view content scale mode supported is 'scale to fill'
- When a list view is in a scroll view and the list view fits, the selected
  item does not extend to where the scrollbars are (hidden). For now, I am
  simply never hiding vertical scrollbars.
- shadow size is not one size fits all

