#!/usr/bin/python
'''
Created on 23 Sep 2017

@author: kamichal
'''

from contextlib import contextmanager
import yattag
import os
import weakref


class Yawrap(object):
    html_d = dict(lang="en-US")
    meta_d = [dict(charset="UTF-8")]

    def __init__(self, target_file, title='', parent=None):
        self.target_file = target_file
        self.title = title
        self._parent = parent
        self.doc, self.tag, self.text, self.line = yattag.SimpleDoc().ttl()
        self._js = []
        self._css = []

    def css(self, *css_defs):
        self._css.extend(css_defs)

    def __str__(self):
        body_render = yattag.indent(self.doc.getvalue())
        return body_render

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

                for css in self._css:
                    with page_doc.tag('style'):
                        page_doc.text(css)
            with page_doc.tag('body'):
                yield

    def _render_page(self):
        page_doc = yattag.SimpleDoc()
        with self._page_structure(page_doc):
            page_doc.asis(str(self))
        return yattag.indent(page_doc.getvalue())

    def render(self):
        dir_ = os.path.dirname(self.target_file)
        if not os.path.isdir(dir_):
            assert not os.path.isfile(self.target_file)
            os.makedirs(dir_)

        with open(self.target_file, 'wt') as ff:
            ff.write(self._render_page())


class NavedYawrap(Yawrap):

    def __init__(self, target_file, title='', parent=None, nav_title=''):
        super(NavedYawrap, self).__init__(target_file, title, parent)
        self.nav_title = nav_title or title
        self._separate_subs = []

    def sub(self, target_file, title=''):
        sub_ = NavedYawrap(target_file, title, weakref.ref(self))
        self._separate_subs.append(sub_)
        return sub_

    def _render_page(self):
        page_doc = yattag.SimpleDoc()
        with self._page_structure(page_doc):
            if self._separate_subs or self._parent:
                self._insert_nav(page_doc)
            page_doc.asis(str(self))
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
        its_children = [child._get_nav_structure(child) for child in root._separate_subs]
        return (root, its_children)

    def _insert_nav(self, doc):
        nav_structure = self._get_nav_structure()
        curr_dir = os.path.dirname(self.target_file)

        def render_subs_of(structure_element):
            current, subs = structure_element
            with doc.tag('div', klass='nav_group_div'):
                link = os.path.relpath(current.target_file, curr_dir)
                with doc.tag('a', href=link):
                    doc.text(current.nav_title or link.replace('.html', ''))
                for sub in subs:
                    render_subs_of(sub)

        with doc.tag('div', klass='nav_main_panel'), doc.tag('nav'):
            render_subs_of(nav_structure)
