import logging
logger = logging.getLogger(__name__)


view = None


def set(new_focus):
    global view

    prev_focus = view
    view = new_focus

    if view is not None:
        logger.debug('focus given to %s' % view)
        view.focused()
    else:
        logger.debug('focus cleared')

    if prev_focus and prev_focus != new_focus:
        prev_focus.blurred()
