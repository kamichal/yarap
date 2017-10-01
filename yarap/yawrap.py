#!/usr/bin/python
'''
Created on 23 Sep 2017

@author: kamichal
'''

from collections import namedtuple
from contextlib import contextmanager
import os
import weakref
import yattag

from utils import fix_yattag, dictionize_css, form_css
NavEntry = namedtuple('NavEntry', 'element, bookmarks, children')

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
                for id_, svg_def in svg_defs.iteritems():
                    with painter.tag('g', id=id_):
                        painter.asis(svg_def)
        yield


def assert_keys_not_in(keys, args, kwargs):
    keys = keys if isinstance(keys, (list, tuple)) else [keys]
    for key in keys:
        defined_keys = kwargs.keys() + map(lambda x: x[0], filter(lambda y: isinstance(y, tuple), args))
        if key in defined_keys:
            raise ValueError("Duplicated '{}' attribute.".format(key))


def make_place(target_file):
    dir_ = os.path.dirname(target_file)
    if not os.path.isdir(dir_):
        assert not os.path.isfile(dir_)
        os.makedirs(dir_)
    return target_file


class Yawrap(yattag.Doc):
    css = ''
    js = []
    html_d = dict(lang="en-US")
    meta_d = [dict(charset="UTF-8")]
    svg_d = DEFAULT_SVG_TAG_ATTRIBUTES

    def __init__(self, target_file, title='', parent=None, defaults=None, errors=None,
                 error_wrapper=('<span class="error">', '</span>'), stag_end=' />'):

        super(Yawrap, self).__init__(defaults, errors, error_wrapper, stag_end)
        self._target_file = target_file
        self.title = title
        self._parent = parent
        self._target_dir = os.path.dirname(target_file)
        self._additional_js = []
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
        with open(make_place(self._target_file), 'wt') as ff:
            ff.write(self._render_page())

    @contextmanager
    def svg(self, svg_styles_as_str='', *args, **svg_tag_attributes):
        svg_tag_attributes.update(self.svg_d)
        with svg_structure(self, svg_tag_attributes, svg_styles_as_str, *args, **svg_tag_attributes):
            yield

    def add_css(self, css_rules):
        if not isinstance(css_rules, dict):
            assert isinstance(css_rules, str)
            css_rules = dictionize_css(css_rules)
        self._additional_css.update(css_rules)

    def link_local_css_file(self, target_css_file_path):
        rel_location = os.path.relpath(os.path.abspath(target_css_file_path), self._target_dir)
        self.external_csss.add(rel_location)

    def link_external_css_file(self, target_css_url):
        self.external_csss.add(target_css_url)

    @contextmanager
    def _html_page_structure(self, page_doc):
        page_css = dictionize_css(self.css).copy()
        page_css.update(self._additional_css)
        page_js = self._additional_js + self.js

        page_doc.asis('<!doctype html>')
        with page_doc.tag('html', **self.html_d):
            with page_doc.tag('head'):
                for meta in self.meta_d:
                    page_doc.stag('meta', **meta)
                if self.title:
                    with page_doc.tag('title'):
                        page_doc.text(self.title)
                for js in page_js:
                    with page_doc.tag('script'):
                        page_doc.text(js)
                if page_css:
                    with page_doc.tag('style'):
                        page_doc.text(form_css(page_css, indent_level=3))
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


BASIC_NAV_CSS = """\
.nav_main_panel {
    padding: 6px;
}
.nav_group_div {
    padding: 0px 8px;
    margin: 6px;
}
.main_content_body {
    padding: 3px;
}
"""


class NavedYawrap(Yawrap):
    css = BASIC_NAV_CSS

    def __init__(self, target_file, title='', parent=None, nav_title='', defaults=None, errors=None,
                 error_wrapper=('<span class="error">', '</span>'), stag_end=' />'):
        super(NavedYawrap, self).__init__(target_file, title, parent, defaults, errors, error_wrapper, stag_end)
        self.nav_title = nav_title or title
        self._subs = []
        self._bookmarks = []

    def sub(self, target_file, title=''):
        sub_ = type(self)(target_file, title, weakref.ref(self))
        self._subs.append(sub_)
        return sub_

    @contextmanager
    def bookmark(self, id_, name_in_nav='', type_='div', *args, **kwargs):
        """ as regular doc.tag, but also manages navigation stuff """
        assert_keys_not_in('id', args, kwargs)
        assert id_ and isinstance(id_, (str, unicode)), "Invalid id: '%s'" % id_
        assert id_ not in map(lambda x: x[0], self._bookmarks), "Bookmark ids collision. '%s' is already defined" % id_
        name_in_nav = name_in_nav or id_
        id_ = id_.replace(' ', '_')
        self._bookmarks.append((id_, name_in_nav))
        with self.tag(type_, *args, id=id_, **kwargs):
            yield

    def _render_page(self):
        page_doc = yattag.SimpleDoc()
        with self._html_page_structure(page_doc):
            if self._subs or self._parent:
                self._insert_nav(page_doc)
            with page_doc.tag('div', klass='main_content_body'):
                page_doc.asis(self._get_body_render())
        return yattag.indent(page_doc.getvalue())

    def render_all_files(self):
        self.render()
        for sub in self._subs:
            sub.render_all_files()

    def _get_root(self):
        if self._parent:
            return self._parent()._get_root()
        return self

    def _insert_nav(self, doc):
        nav_structure = self._get_nav_structure()
        with doc.tag('nav', klass='nav_main_panel'):
            self._render_nav_subs(nav_structure, doc)

    def _get_nav_structure(self, sub=None):
        current = sub or self._get_root()
        its_children = tuple(child._get_nav_structure(child) for child in current._subs)
        return NavEntry(current, current._bookmarks, its_children)

    def _render_nav_subs(self, structure_element, doc):
        current = structure_element.element
        link = os.path.relpath(current._target_file, self._target_dir)

        with doc.tag('div', klass='nav_group_div'):
            if current == self:
                doc.attr(klass='nav_group_div active')

            with doc.tag('div', klass='nav_page'):
                with doc.tag('a', href=link, klass='nav_page_link'):
                    if current._target_file == self._target_file:
                        doc.attr(klass='active')
                    doc.text(current.nav_title or link)

                if current == self:
                    doc.attr(klass='nav_page with_bookmarks')
                    for bookmark, bookmark_name in structure_element.bookmarks:
                        bookmark_link = "%s#%s" % (link, bookmark)
                        with doc.tag('a', klass='nav_bookmark_link', href=bookmark_link):
                            doc.text(bookmark_name)

            for sub in structure_element.children:
                self._render_nav_subs(sub, doc)
