view = None


def set(newfocus):
    global view

    prevfocus = view
    view = newfocus

    if view is not None:
        view.focused()

    if prevfocus and prevfocus != newfocus:
        prevfocus.blurred()
