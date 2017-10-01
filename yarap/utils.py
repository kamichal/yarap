#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 30 wrz 2017

@author: kamichal
'''


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


def fix_yattag(yattag_module):
    def fix_keys(dict_):
        return {KNOWN_SUBSTITUTES.get(k, k): v for k, v in dict_.iteritems()}

    def _attributes2(args, kwargs):

        def tr(arg):
            if isinstance(arg, tuple):
                return arg
            elif isinstance(arg, str):
                return (arg, yattag_module.simpledoc.ATTR_NO_VALUE)
            else:
                raise ValueError("Couldn't make a XML or HTML attribute/value pair out of %s." % repr(arg))

        result = dict(map(tr, args))
        result.update({KNOWN_SUBSTITUTES.get(k, k): v for k, v in kwargs.iteritems()})
        return result

    yattag_module.simpledoc._attributes = _attributes2


def dictionize_css(input_css):
    if isinstance(input_css, dict):
        return input_css
    assert isinstance(input_css, str)

    def iterate_rules(in_css):
        while in_css:
            decl_start = in_css.find('{')
            decl_end = in_css.find('}')
            if any(o == -1 for o in (decl_start, decl_end)):
                break
            selectors = in_css[0:decl_start].strip()
            declarations = in_css[decl_start + 1: decl_end].strip()
            yield selectors, declarations
            in_css = in_css[decl_end + 1:]

    def iterate_declarations(declarations):
        for decl in declarations.split(';'):
            if decl:
                first_colon = decl.find(':')
                if first_colon:
                    property_ = decl[:first_colon].strip()
                    value = decl[first_colon + 1:].strip()
                    yield property_, value
                else:
                    yield decl.strip(), None

    return {selector: {prop: val for prop, val in iterate_declarations(declarations)}
            for selector, declarations in iterate_rules(input_css)}


def form_css(structured_css, indent_level=1):
    assert isinstance(structured_css, dict)
    base_indent = ' ' * 2
    indent = base_indent * indent_level

    template = "{ind}{selector} {{{definitions}}}"
    def_tpl = "{ind}{bind}{property}: {value};"

    def rules():
        for selector, definitions in sorted(structured_css.iteritems()):
            defs = '\n'.join(def_tpl.format(ind=indent, bind=base_indent, property=prop, value=val)
                             for prop, val in sorted(definitions.iteritems()))
            if defs:
                defs = "\n{}\n{ind}".format(defs, ind=indent)
            yield template.format(ind=indent, selector=selector, definitions=defs)

    return '\n'.join(rules())
