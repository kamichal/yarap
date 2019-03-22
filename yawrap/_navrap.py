import os
import weakref
from collections import namedtuple
from contextlib import contextmanager

from ._engine import Doc
from ._yawrap import Yawrap
from .six import str_types
from .utils import assert_keys_not_in

NavEntry = namedtuple('NavEntry', 'element, bookmarks, children')

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

    def calc_rel_path(self, path_part, *path_parts):
        """ returns path relative to target file of this instance """
        target_dir = os.path.dirname(os.path.abspath(self._target_file))
        return os.path.join(target_dir, path_part, *path_parts)

    @contextmanager
    def bookmark(self, id_, name_in_nav='', type_='div', *args, **kwargs):
        """ as regular doc.tag, but also manages navigation stuff """
        assert_keys_not_in('id', args, kwargs)
        assert id_ and isinstance(id_, str_types), "Invalid id: '%s'" % id_
        assert id_ not in map(lambda x: x[0], self._bookmarks), "Bookmark ids collision. '%s' is already defined" % id_
        name_in_nav = name_in_nav or id_
        id_ = id_.replace(' ', '_')
        self._bookmarks.append((id_, name_in_nav))
        with self.tag(type_, *args, id=id_, **kwargs):
            yield

    def render_all_files(self):
        self.render()
        for sub in self._subs:
            sub.render_all_files()

    def _render_page(self):
        page_doc = Doc()
        with self._html_page_structure(page_doc):
            if self._subs or self._parent:
                self._insert_nav(page_doc)
            with page_doc.tag('main', klass='main_content_body'):
                page_doc._clone_children(self)
        return page_doc.getvalue()

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
