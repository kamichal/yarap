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
        self._subs = []
        self._bookmarks = []

    def sub(self, target_file, title=''):
        sub_ = type(self)(target_file, title, weakref.ref(self))
        self._subs.append(sub_)
        return sub_

    @contextmanager
    def bookmark(self, id_, name_in_nav='', type_='div', *args, **kwargs):
        """ as regular doc.tag, but also manages navigation stuff """
        assert 'id' not in kwargs, 'Duplicated id attribute.'
        name_in_nav = name_in_nav or id_
        id_ = id_.replace(' ', '_')
        self._bookmarks.append((id_, name_in_nav))
        with self.tag(type_, *args, id=id_, **kwargs):
            yield

    def _render_page(self):
        page_doc = yattag.SimpleDoc()
        with self._page_structure(page_doc):
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
        curr_dir = os.path.dirname(self.target_file)
        current = structure_element.element
        link = os.path.relpath(current.target_file, curr_dir)

        with doc.tag('div', klass='nav_group_div'):
            if current == self:
                doc.attr(klass='nav_group_div active')

            with doc.tag('div', klass='nav_page'):
                with doc.tag('a', href=link, klass='nav_page_link'):
                    if current.target_file == self.target_file:
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
