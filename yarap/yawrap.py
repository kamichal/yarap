#!/usr/bin/python
'''
Created on 23 Sep 2017

@author: kamichal
'''

from contextlib import contextmanager
import os
import yattag


class Yawrap(object):
    html_d = dict(lang="en-US")
    meta_d = [dict(charset="UTF-8")]

    def __init__(self, title=''):
        self.doc, self.tag, self.text, self.line = yattag.SimpleDoc().ttl()
        self.title = title
        self._js = []
        self._css = []
        self.body = ''

    @contextmanager
    def sub(self):
        sub_ = Yawrap()
        yield sub_
        self.doc.asis(yattag.indent(sub_.doc.getvalue()))
        self._js.extend(sub_._js)
        self._css.extend(sub_._css)
        print self

    def css(self, *css_defs):
        self._css.extend(css_defs)

    def __str__(self):
        body_render = yattag.indent(self.doc.getvalue())
        return body_render

    def render(self):
        doc, tag, text = yattag.SimpleDoc().tagtext()
        doc.asis('<!doctype html>')
        with tag('html', **self.html_d):
            with tag('head'):
                for meta in self.meta_d:
                    doc.stag('meta', **meta)

                if self.title:
                    with tag('title'):
                        text(self.title)
                for js in self._js:
                    with tag('script'):
                        text(js)

                for css in self._css:
                    with tag('style'):
                        text(css)

            with tag('body'):
                doc.asis(str(self))

        return yattag.indent(doc.getvalue())

    def render_to_file(self, target_file):
        with open(target_file, 'wt') as ff:
            ff.write(self.render())
