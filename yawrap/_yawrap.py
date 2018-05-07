#!/usr/bin/python
'''
Created on 23 Sep 2017

@author: kamichal
'''

from contextlib import contextmanager
import os

from yawrap._engine import Doc
from yawrap._sourcer import HEAD, BODY_BEGIN, BODY_END, _Resource
from yawrap.utils import assert_keys_not_in, make_place


DEFAULT_SVG_TAG_ATTRIBUTES = dict(xmlns="http://www.w3.org/2000/svg", version="1.1")


@contextmanager
def svg_structure(painter,
                  svg_tag_attributes=DEFAULT_SVG_TAG_ATTRIBUTES,
                  svg_styles_as_str="",
                  *args,
                  **kwargs):

    kwargs.update(svg_tag_attributes)
    with painter.tag('svg', *args, **kwargs):
        if svg_styles_as_str:
            with painter.tag('style', type="text/css"):
                painter.cdata(svg_styles_as_str)
        yield


class Yawrap(Doc):
    resources = []
    html_d = dict(lang="en-US")
    meta_d = [dict(charset="UTF-8")]
    svg_d = DEFAULT_SVG_TAG_ATTRIBUTES

    def __init__(self, target_file, title='', parent=None):

        super(Yawrap, self).__init__()
        self._target_file = target_file
        self.title = title
        self._parent = parent
        self._target_dir = os.path.dirname(target_file)
        self._additional_resources = []

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

    def getvalue(self):
        return self._render_page()

    @contextmanager
    def svg(self, svg_styles_as_str='', *args, **svg_tag_attributes):
        svg_tag_attributes.update(self.svg_d)
        with svg_structure(self, svg_tag_attributes, svg_styles_as_str, *args, **svg_tag_attributes):
            yield

    def add(self, js_or_css_resource):
        assert isinstance(js_or_css_resource, _Resource), "Bad ussage, expected CSS or JS"\
            " resource definition, got %s." % type(js_or_css_resource).__name__
        self._additional_resources.append(js_or_css_resource)

    def _get_rel_path(self, target_local_file):
        return os.path.relpath(os.path.abspath(target_local_file), self._target_dir)

    @contextmanager
    def _html_page_structure(self, page_doc):

        page_doc.asis('<!doctype html>')
        with page_doc.tag('html', **self.html_d):
            with page_doc.tag('head'):
                for meta in self.meta_d:
                    page_doc.stag('meta', **meta)
                if self.title:
                    with page_doc.tag('title'):
                        page_doc.text(self.title)

                for resource in self.resources + self._additional_resources:
                    resource.visit(page_doc, self, HEAD)

            with page_doc.tag('body'):
                for resource in self.resources + self._additional_resources:
                    resource.visit(page_doc, self, BODY_BEGIN)
                """ at this moment yawrap will place its html here """
                yield
                for resource in self.resources + self._additional_resources:
                    resource.visit(page_doc, self, BODY_END)

    def _render_page(self):
        page_doc = Doc()
        with self._html_page_structure(page_doc):
            page_doc._clone_children(self)
        return page_doc.getvalue()

    def _get_root(self):
        return self

    def get_root_dir(self):
        return self._get_root()._target_dir
