#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 25 wrz 2017

@author: kamichal
'''
from yarap.svgrap import Svgrap
from bs4 import BeautifulSoup
import yattag

EXPECTED_TEST1_INLINE_OUTPUT = """\
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
  <rect x="25" y="25" width="200" height="200" fill="lime" stroke-width="4" stroke="pink" />
  <circle cx="125" cy="125" r="75" fill="orange" />
  <polyline points="50,150 50,200 200,200 200,100" stroke="red" stroke-width="4" fill="none" />
  <line x1="50" y1="50" x2="200" y2="200" stroke="blue" stroke-width="4" />
</svg>"""


EXPECTED_TEST1_STANDALONE_OUTPUT = '<?xml version="1.0" encoding="UTF-8" ?>\n' + EXPECTED_TEST1_INLINE_OUTPUT


def test_1_inline_version():

    svg = Svgrap()

    svg.stag('rect', x="25", y="25", width="200", height="200", fill="lime", stroke_width="4", stroke="pink")
    svg.stag('circle', cx="125", cy="125", r="75", fill="orange")
    svg.stag('polyline', ('stroke-width', 4), points="50,150 50,200 200,200 200,100", stroke="red", fill="none")
    svg.stag('line', x1="50", y1="50", x2="200", y2="200", stroke="blue", stroke_width="4")

    render = svg._render_svg()
    print ''
    print render

    gotten_soup = BeautifulSoup(render, "lxml")
    expected_soup = BeautifulSoup(EXPECTED_TEST1_INLINE_OUTPUT, "lxml")

    assert gotten_soup == expected_soup


def test_1_child_version():

    empty_doc = yattag.SimpleDoc()

    svg = Svgrap()

    svg.stag('rect', x="25", y="25", width="200", height="200", fill="lime", stroke_width="4", stroke="pink")
    svg.stag('circle', cx="125", cy="125", r="75", fill="orange")
    svg.stag('polyline', ('stroke-width', 4), points="50,150 50,200 200,200 200,100", stroke="red", fill="none")
    svg.stag('line', x1="50", y1="50", x2="200", y2="200", stroke="blue", stroke_width="4")

    svg._render_svg(empty_doc)
    render = yattag.indent(empty_doc.getvalue())

    print ''
    print render

    gotten_soup = BeautifulSoup(render, "lxml")
    expected_soup = BeautifulSoup(EXPECTED_TEST1_INLINE_OUTPUT, "lxml")

    assert gotten_soup == expected_soup


def test_1_static_version():

    class SvgTest1(Svgrap):
        pass

    svg = SvgTest1()

    svg.stag('rect', x="25", y="25", width="200", height="200", fill="lime", stroke_width="4", stroke="pink")
    svg.stag('circle', cx="125", cy="125", r="75", fill="orange")
    svg.stag('polyline', ('stroke-width', 4), points="50,150 50,200 200,200 200,100", stroke="red", fill="none")
    svg.stag('line', x1="50", y1="50", x2="200", y2="200", stroke="blue", stroke_width="4")

    render = svg._render_svg()
    print ''
    print render

    gotten_soup = BeautifulSoup(render, "lxml")
    expected_soup = BeautifulSoup(EXPECTED_TEST1_INLINE_OUTPUT, "lxml")

    assert gotten_soup == expected_soup


