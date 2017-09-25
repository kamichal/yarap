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


class Svgrap(yattag.SimpleDoc):
    svg_d = dict(xmlns="http://www.w3.org/2000/svg", version="1.1")
    svg_style_def = ''

    def __init__(self, stag_end=' />', *args, **kwargs):
        super(Svgrap, self).__init__(stag_end)
        self.args = args
        self.kwargs = kwargs

    def save_to_file(self, target_file):
        dir_ = os.path.dirname(target_file)
        if not os.path.isdir(dir_):
            assert not os.path.isfile(dir_)
            os.makedirs(dir_)

        with open(target_file, 'wt') as ff:
            ff.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            ff.write(self._render_svg())

    def _render_svg(self, parent_doc=None):
        parent_doc = parent_doc or yattag.SimpleDoc()
        if not isinstance(parent_doc, yattag.SimpleDoc):
            raise ValueError('Expected yattag.SimpleDoc instance.')

        with self._svg_structure(parent_doc, *self.args, **self.kwargs):
            parent_doc.asis(self.getvalue())
        return yattag.indent(parent_doc.getvalue())

    @contextmanager
    def _svg_structure(self, parent_doc, *args, **kwargs):
        kwargs.update(self.svg_d)
        with parent_doc.tag('svg', *args, **kwargs):
            if self.svg_style_def:
                with parent_doc.tag('style', type="text/css"):
                    parent_doc.cdata(self.svg_style_def)
            yield
