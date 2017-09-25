#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 25 wrz 2017

@author: kamichal
'''
import yattag
import os
from contextlib import contextmanager
from yattag.simpledoc import ATTR_NO_VALUE


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


def make_place(target_file):
    dir_ = os.path.dirname(target_file)
    if not os.path.isdir(dir_):
        assert not os.path.isfile(dir_)
        os.makedirs(dir_)
    return target_file


def fix_keys(dict_):
    return {KNOWN_SUBSTITUTES.get(k, k): v for k, v in dict_.iteritems()}


def _attributes2(args, kwargs):

    def tr(arg):
        if isinstance(arg, tuple):
            return arg
        elif isinstance(arg, str):
            return (arg, ATTR_NO_VALUE)
        else:
            raise ValueError("Couldn't make a XML or HTML attribute/value pair out of %s." % repr(arg))

    result = dict(map(tr, args))
    result.update({KNOWN_SUBSTITUTES.get(k, k): v for k, v in kwargs.iteritems()})
    return result


yattag.simpledoc._attributes = _attributes2

DEFAULT_SVG_TAG_ATTRIBUTES = dict(xmlns="http://www.w3.org/2000/svg", version="1.1")


@contextmanager
def svg_structure(painter,
                  svg_tag_attributes=DEFAULT_SVG_TAG_ATTRIBUTES,
                  svg_styles_as_str=None,
                  *args,
                  **kwargs):

    kwargs.update(svg_tag_attributes)
    svg_defs = None
    with painter.tag('svg', *args, **kwargs):
        if svg_styles_as_str:
            with painter.tag('style', type="text/css"):
                painter.cdata(svg_styles_as_str)
        if svg_defs:
            with painter.tag('defs', type="text/css"):
                painter.text(svg_styles_as_str)
        yield


class SvgHost(yattag.SimpleDoc):
    svg_d = DEFAULT_SVG_TAG_ATTRIBUTES

    def __init__(self, *args, **kwargs):
        super(SvgHost, self).__init__(*args, **kwargs)

    @contextmanager
    def svg(self, svg_styles_as_str='', *args, **svg_tag_attributes):
        svg_tag_attributes.update(self.svg_d)
        with svg_structure(self, svg_tag_attributes, svg_styles_as_str, *args, **svg_tag_attributes):
            yield
