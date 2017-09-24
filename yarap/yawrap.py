#!/usr/bin/python
'''
Created on 23 Sep 2017

@author: kamichal
'''

from contextlib import contextmanager
import yattag
import os
import weakref
from collections import namedtuple

NavEntry = namedtuple('NavEntry', 'element, bookmarks, children')


class Yawrap(object):
    html_d = dict(lang="en-US")
    meta_d = [dict(charset="UTF-8")]
    _js = []
    css = ''

    def __init__(self, target_file, title='', parent=None):
        self.target_file = target_file
        self.title = title
        self._parent = parent
        self.doc, self.tag, self.text, self.line = yattag.SimpleDoc().ttl()

    def _get_body_render(self):
        return yattag.indent(self.doc.getvalue())

    @contextmanager
    def _page_structure(self, page_doc):
        page_doc.asis('<!doctype html>')
        with page_doc.tag('html', **self.html_d):
            with page_doc.tag('head'):
                for meta in self.meta_d:
                    page_doc.stag('meta', **meta)
                if self.title:
                    with page_doc.tag('title'):
                        page_doc.text(self.title)
                for js in self._js:
                    with page_doc.tag('script'):
                        page_doc.text(js)
                if self.css:
                    with page_doc.tag('style'):
                        page_doc.text(self.css)
            with page_doc.tag('body'):
                yield

    def _render_page(self):
        page_doc = yattag.SimpleDoc()
        with self._page_structure(page_doc):
            page_doc.asis(self._get_body_render())
        return yattag.indent(page_doc.getvalue())

    def render(self):
        """ Saves page in current state to target file. """
        dir_ = os.path.dirname(self.target_file)
        if not os.path.isdir(dir_):
            assert not os.path.isfile(self.target_file)
            os.makedirs(dir_)

        with open(self.target_file, 'wt') as ff:
            ff.write(self._render_page())


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

    def __init__(self, target_file, title='', parent=None, nav_title=''):
        super(NavedYawrap, self).__init__(target_file, title, parent)
        self.nav_title = nav_title or title
        self._separate_subs = []
        self._bookmarks = []

    def sub(self, target_file, title=''):
        sub_ = type(self)(target_file, title, weakref.ref(self))
        self._separate_subs.append(sub_)
        return sub_

    @contextmanager
    def bookmark(self, id_, nav_name='', type_='div'):
        nav_name = nav_name or id_
        id_ = id_.replace(' ', '_')
        self._bookmarks.append((id_, nav_name))
        with self.tag(type_, id=id_):
            yield

    def _render_page(self):
        page_doc = yattag.SimpleDoc()
        with self._page_structure(page_doc):
            if self._separate_subs or self._parent:
                self._insert_nav(page_doc)
            with page_doc.tag('div', klass='main_content_body'):
                page_doc.asis(self._get_body_render())
        return yattag.indent(page_doc.getvalue())

    def render_all_files(self):
        self.render()
        for sub in self._separate_subs:
            sub.render_all_files()

    def _get_root(self):
        if self._parent:
            return self._parent()._get_root()
        return self

    def _get_nav_structure(self, sub=None):
        root = sub or self._get_root()
        its_children = tuple(child._get_nav_structure(child) for child in root._separate_subs)
        return NavEntry(root, root._bookmarks, its_children)

    def _insert_nav(self, doc):
        nav_structure = self._get_nav_structure()
        curr_dir = os.path.dirname(self.target_file)

        def render_subs_of(structure_element):
            current, bookmarks, subs = structure_element
            with doc.tag('div', klass='nav_group_div'):
                if current == self:
                    doc.attr(klass='nav_group_div active')
                link = os.path.relpath(current.target_file, curr_dir)
                with doc.tag('a', href=link):
                    if current.target_file == self.target_file:
                        doc.attr(klass='nav_group_div active')
                    doc.text(current.nav_title or link)
                for bookmark, bookmark_name in bookmarks:
                    bookmark_link = "%s#%s" % (link, bookmark)
                    with doc.tag('a', href=bookmark_link):
                        doc.text(bookmark_name)

                for sub in subs:
                    render_subs_of(sub)

        with doc.tag('nav', klass='nav_main_panel'):
            render_subs_of(nav_structure)
