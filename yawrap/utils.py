#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 30 wrz 2017

@author: kamichal
'''
import os
import re
from yattag.simpledoc import ATTR_NO_VALUE

from .six import str_types


KNOWN_SUBSTITUTES = {
    'klass': 'class',
    'Class': 'class',
    'class_': 'class',
    'fill_opacity': 'fill-opacity',
    'stroke_width': 'stroke-width',
    'stroke_dasharray': ' stroke-dasharray',
    "stroke_opacity": "stroke-opacity",
    "stroke_dashoffset": "stroke-dashoffset",
    "stroke_linejoin": "stroke-linejoin",
    "stroke_miterlimit": "stroke-miterlimit",
}


def _attributes2(args, kwargs):

    def tr(arg):
        if isinstance(arg, tuple):
            return arg
        elif isinstance(arg, str_types):
            return (arg, ATTR_NO_VALUE)
        else:
            raise ValueError("Couldn't make a XML or HTML attribute/value pair out of %s." % repr(arg))

    result = dict(map(tr, args))
    result.update({KNOWN_SUBSTITUTES.get(k, k): v for k, v in kwargs.items()})
    return result


def fix_yattag(yattag_module):
    yattag_module.simpledoc._attributes = _attributes2


def make_place(target_file):
    dir_ = os.path.dirname(target_file)
    if not os.path.isdir(dir_):
        assert not os.path.isfile(dir_)
        os.makedirs(dir_)
    return target_file


def assert_keys_not_in(keys, args, kwargs):
    keys = keys if isinstance(keys, (list, tuple)) else [keys]
    for key in keys:
        defined_keys = list(kwargs.keys()) + [x[0] for x in args if isinstance(x, tuple)]
        if key in defined_keys:
            raise ValueError("Duplicated '{}' attribute.".format(key))


def form_css(structured_css, indent_level=1):
    if isinstance(structured_css, str_types):
        return structured_css

    assert isinstance(structured_css, dict), "Input CSS is supposed to "\
        "be string or dict, got %s" % type(structured_css).__name__
    base_indent = ' ' * 2
    indent = base_indent * indent_level

    template = "\n{ind}{selector} {{{definitions}}}"
    def_tpl = "{ind}{bind}{property}: {value};"

    def rules():
        for selector, definitions in sorted(structured_css.items()):
            defs = '\n'.join(def_tpl.format(ind=indent, bind=base_indent, property=prop, value=val)
                             for prop, val in sorted(definitions.items()))
            if defs:
                defs = "\n{}\n{ind}".format(defs, ind=indent)
            yield template.format(ind=indent, selector=selector, definitions=defs)

    return ''.join(rules())


def error(text):
    print(text)


def warn_(text):
    print(text)


DJANGO_URL_VALIDATION_PROG = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_url(text):
    return isinstance(text, str) and DJANGO_URL_VALIDATION_PROG.match(text) is not None
