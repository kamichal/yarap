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
    meta_d = [dict(charset='UTF-8')]

    def __init__(self):
        self.doc, self.tag, self.text, self.line = yattag.SimpleDoc().ttl()
        self.title = 'ol rajt'
        self.js = ['that script']
        self.css = ["body {padding: 12px;}"]
        self.body = ''

    @contextmanager
    def sub(self):
        sub_ = Yawrap()
        yield sub_
        self.body += yattag.indent(sub_.doc.getvalue())
        self.js.extend(sub_.js)
        self.css.extend(sub_.css)
        print self

    def __str__(self):
        body_render = yattag.indent(self.doc.getvalue())
        return body_render

    def render(self, target_file):
        doc, tag, text = yattag.SimpleDoc().tagtext()
        doc.asis('<!doctype html>')
        with tag('html', **self.html_d):
            with tag('head'):
                for meta in self.meta_d:
                    doc.stag('meta', **meta)

                with tag('title'):
                    text(self.title)
                for js in self.js:
                    with tag('script'):
                        text(js)

                for css in self.css:
                    with tag('style'):
                        text(css)

            with tag('body'):
                doc.asis(str(self))

        whole_page_render = yattag.indent(doc.getvalue())
        with open(target_file, 'wt') as ff:
            ff.write(whole_page_render)

        print '\nsaved file: {}\n'.format(target_file)
        print whole_page_render
