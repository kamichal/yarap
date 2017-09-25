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


class Svgrap(yattag.SimpleDoc):
    svg_d = DEFAULT_SVG_TAG_ATTRIBUTES
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

    def render_impl(self, painter):
        pass

    def _render_svg(self, parent_doc=None):
        target_doc = parent_doc or yattag.SimpleDoc()
        if not isinstance(target_doc, yattag.SimpleDoc):
            raise ValueError('Expected yattag.SimpleDoc instance.')

        with self._svg_structure(target_doc, *self.args, **self.kwargs):
            target_doc.asis(self.getvalue())

        if parent_doc:
            " make it happen "
            pass
        else:
            return yattag.indent(target_doc.getvalue())

    @contextmanager
    def _svg_structure(self, parent_doc, *args, **kwargs):
        kwargs.update(self.svg_d)
        with parent_doc.tag('svg', *args, **kwargs):
            if self.svg_style_def:
                with parent_doc.tag('style', type="text/css"):
                    parent_doc.cdata(self.svg_style_def)
            yield


def assert_it_is_yattag(obj, yattag_type=yattag.SimpleDoc):
    if not isinstance(obj, yattag_type):
        raise ValueError('Expected yattag.SimpleDoc instance.')


def assert_it_is_yattag_or_none(obj, yattag_type=yattag.SimpleDoc):
    assert_it_is_yattag(obj, (yattag_type, None))


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


class SvgClassBase(object):
    svg_standalone_xml_header = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    svg_d = DEFAULT_SVG_TAG_ATTRIBUTES
    svg_style_def = ''

    def __init__(self, parent_doc):
        assert_it_is_yattag(parent_doc)
        self._parent_doc = parent_doc

    def save_to_file(self, target_file, *args, **kwargs):
        empty_doc = yattag.SimpleDoc()
        empty_doc.asis(self.__class__.svg_standalone_xml_header)
        svg_code = self._create_svg_code(empty_doc, *args, **kwargs)
        with open(make_place(target_file), 'wt') as ff:
            ff.write(svg_code)

    def _create_svg_code(self, target_doc, *args, **kwargs):
        with svg_structure(target_doc, svg_tag_attributes=self.__class__.svg_d):
            self.render_impl(target_doc)
        return yattag.indent(target_doc.getvalue())

    def render_impl(self, painter, *args, **kwargs):
        " embed implement it in a derived class "
        pass

    @classmethod
    def embed_svg(cls, target_doc):
        assert_it_is_yattag(target_doc)
        cls._create_svg_code(target_doc)
