#!/usr/bin/python
'''
Created on 23 Sep 2017

@author: kamichal
'''

from contextlib import contextmanager
import os
import yattag

from .utils import fix_yattag, dictionize_css, form_css, assert_keys_not_in, make_place
from .six import str_types


DEFAULT_SVG_TAG_ATTRIBUTES = dict(xmlns="http://www.w3.org/2000/svg", version="1.1")

fix_yattag(yattag)


@contextmanager
def svg_structure(painter,
                  svg_tag_attributes=DEFAULT_SVG_TAG_ATTRIBUTES,
                  svg_styles_as_str="",
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
                for id_, svg_def in svg_defs.items():
                    with painter.tag('g', id=id_):
                        painter.asis(svg_def)
        yield


class Yawrap(yattag.Doc):
    css = ''
    js = []
    linked_js = []
    linked_css = []
    html_d = dict(lang="en-US")
    meta_d = [dict(charset="UTF-8")]
    svg_d = DEFAULT_SVG_TAG_ATTRIBUTES

    def __init__(self, target_file, title='', parent=None, defaults=None, errors=None,
                 error_wrapper=('<span class="error">', '</span>'), stag_end='/>'):

        super(Yawrap, self).__init__(defaults, errors, error_wrapper, stag_end)
        self._target_file = target_file
        self.title = title
        self._parent = parent
        self._target_dir = os.path.dirname(target_file)
        self._additional_js = []
        self._additional_linked_js = []
        self._additional_css = {}
        self.external_csss = set()

    @contextmanager
    def local_link(self, target, *args, **kwargs):
        rel_location = os.path.relpath(target, self._target_dir)
        assert_keys_not_in('href', args, kwargs)
        with self.tag('a', href=rel_location, *args, **kwargs):
            yield rel_location

    def render(self):
        """ Saves page in current state to target file. """
        raw_html = self._render_page()
        with open(make_place(self._target_file), 'wt') as ff:
            ff.write(raw_html)

    @contextmanager
    def svg(self, svg_styles_as_str='', *args, **svg_tag_attributes):
        svg_tag_attributes.update(self.svg_d)
        with svg_structure(self, svg_tag_attributes, svg_styles_as_str, *args, **svg_tag_attributes):
            yield

    def add_css(self, css_rules):
        if not isinstance(css_rules, dict):
            assert isinstance(css_rules, str_types)
            css_rules = dictionize_css(css_rules)
        self._additional_css.update(css_rules)

    def add_js(self, js_script):
        assert isinstance(js_script, str_types)
        self._additional_js.append(js_script)

    def _get_rel_path(self, target_local_file):
        return os.path.relpath(os.path.abspath(target_local_file), self._target_dir)

    def link_local_css_file(self, target_css_file_path):
        self.external_csss.add(self._get_rel_path(target_css_file_path))

    def link_local_js_file(self, target_js_file_path):
        self._additional_linked_js.add(self._get_rel_path(target_js_file_path))

    def link_external_js_file(self, target_js_url):
        self._additional_linked_js.append(target_js_url)

    def link_external_css_file(self, target_css_url):
        self.external_csss.add(target_css_url)

    @contextmanager
    def _html_page_structure(self, page_doc):
        page_css = dictionize_css(self.css).copy()
        page_css.update(self._additional_css)
        page_js = self._additional_js + self.js
        linked_js = self._additional_linked_js + self.linked_js

        page_doc.asis('<!doctype html>')
        with page_doc.tag('html', **self.html_d):
            with page_doc.tag('head'):
                for meta in self.meta_d:
                    page_doc.stag('meta', **meta)
                if self.title:
                    with page_doc.tag('title'):
                        page_doc.text(self.title)
                for js_link in linked_js:
                    with page_doc.tag("script", src=js_link):
                        pass
                for js in page_js:
                    with page_doc.tag('script'):
                        page_doc.asis(js)
                if page_css:
                    with page_doc.tag('style'):
                        page_doc.asis(form_css(page_css, indent_level=3))
                for ext_css in self.external_csss:
                    page_doc.stag("link", rel="stylesheet", type="text/css", href=ext_css)
            with page_doc.tag('body'):
                yield

    def _render_page(self):
        page_doc = yattag.SimpleDoc()
        with self._html_page_structure(page_doc):
            page_doc.asis(self._get_body_render())
        return yattag.indent(page_doc.getvalue())

    def _get_body_render(self):
        return yattag.indent(self.getvalue())

