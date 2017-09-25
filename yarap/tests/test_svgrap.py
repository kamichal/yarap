#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 25 wrz 2017

@author: kamichal
'''
from yarap.svgrap import  SvgHost
from bs4 import BeautifulSoup
import yattag
import pytest
import os

EXPECTED_TEST1_OUTPUT = """\
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
  <rect x="25" y="25" width="200" height="200" fill="lime" stroke-width="4" stroke="pink" />
  <circle cx="125" cy="125" r="75" fill="orange" />
  <polyline points="50,150 50,200 200,200 200,100" stroke="red" stroke-width="4" fill="none" />
  <line x1="50" y1="50" x2="200" y2="200" stroke="blue" stroke-width="4" />
</svg>"""


def painter_def_test1(smth):
    smth.stag('rect', x="25", y="25", width="200", height="200", fill="lime", stroke_width="4", stroke="pink")
    smth.stag('circle', cx="125", cy="125", r="75", fill="orange")
    smth.stag('polyline', ('stroke-width', 4),
              points="50,150 50,200 200,200 200,100", stroke="red", fill="none")
    smth.stag('line', x1="50", y1="50", x2="200", y2="200", stroke="blue", stroke_width="4")



def compare_htmls(render, expected):
    gotten_soup = BeautifulSoup(render, "lxml")
    expected_soup = BeautifulSoup(expected, "lxml")
    assert gotten_soup == expected_soup


def test_svg_as_a_tag_empty():

    doc = SvgHost()
    with doc.svg():
        pass
    assert doc.getvalue() == '<svg version="1.1" xmlns="http://www.w3.org/2000/svg"></svg>'


def test_svg_as_a_tag_1():

    doc = SvgHost()
    with doc.svg():
        painter_def_test1(doc)
    compare_htmls(yattag.indent(doc.getvalue()), EXPECTED_TEST1_OUTPUT)

