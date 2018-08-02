"""This module lets you set/get attribute values by walking
a "key path" from a root or start object.

A key path is a string with path part specs delimited by period '.'.
Multiple path part specs are concatenated together to form the
entire path spec.

Each path part spec takes one of two forms:

- identifier
- identifier[integer]

Walks proceed by evaluating each path part spec against the
current object, starting with the given object.

Path part specs work against objects, lists, tuples, and dicts.

Note that a KeyError or IndexError encountered while walking a
key path part spec is not caught. You have to know that the a
walk of the given key path on the given object will work.

An example walk:

    class A(object):
        def __init__(self):
            self.x = dict(y=['hello', 'world'])

    class B(object):
        def __init__(self):
            self.a = A()

    b = B()
    print value_for_keypath(b, 'a.x.y[1]')  # prints 'world'

    # part spec    context
    # ---------    -------
    # 'a'          b.a
    # 'x'          b.a.x
    # 'y[1]'       b.a.x.y[1]
"""

AUTHOR = 'Brian Hammond <brian@fictorial.com>'
LICENSE = 'MIT'

__version__ = '0.1.0'

import re

list_index_re = re.compile(r'([^\[]+)\[(\d+)\]')


def _extract(val, key):
    if isinstance(val, dict):
        return val[key]
    return getattr(val, key, None)


def value_for_keypath(obj, path):
    """Get value from walking key path with start object obj.
    """
    val = obj
    for part in path.split('.'):
        match = re.match(list_index_re, part)
        if match is not None:
            val = _extract(val, match.group(1))
            if not isinstance(val, list) and not isinstance(val, tuple):
                raise TypeError('expected list/tuple')
            index = int(match.group(2))
            val = val[index]
        else:
            val = _extract(val, part)
        if val is None:
            return None
    return val


def set_value_for_keypath(obj, path, new_value, preserve_child = False):
    """Set attribute value new_value at key path of start object obj.
    """
    parts = path.split('.')
    last_part = len(parts) - 1
    dst = obj
    for i, part in enumerate(parts):
        match = re.match(list_index_re, part)
        if match is not None:
            dst = _extract(dst, match.group(1))
            if not isinstance(dst, list) and not isinstance(dst, tuple):
                raise TypeError('expected list/tuple')
            index = int(match.group(2))
            if i == last_part:
                dst[index] = new_value
            else:
                dst = dst[index]
        else:
            if i != last_part:
                dst = _extract(dst, part)
            else:
                if isinstance(dst, dict):
                    dst[part] = new_value
                else:
                    if not preserve_child:
                        setattr(dst, part, new_value)
                    else:
                        try:
                            v = getattr(dst, part)
                        except AttributeError:
                            setattr(dst, part, new_value)


if __name__ == '__main__':
    class A(object):
        def __init__(self):
            self.x = dict(y=['hello', 'world'])

    class B(object):
        def __init__(self):
            self.a = A()

    b = B()
    assert value_for_keypath(b, 'a.x.y[1]') == 'world'

    set_value_for_keypath(b, 'a.x.y[1]', 2)
    assert value_for_keypath(b, 'a.x.y[1]') == 2
