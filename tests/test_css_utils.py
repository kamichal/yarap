#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 30 wrz 2017

@author: kamichal
'''
import pytest

from yawrap.utils import dictionize_css, form_css


RAW_CSSs = """\
      .a_div a {
        color: #000;
        display: block;
        padding: 8px 16px;
        text-decoration: none;
      }
      .a_div a.active {
        background-color: #4CAF50;
        color: white;
      }
      .a_div a:hover:not(.active) {
        background-color: #555;
        color: white;
      }
      .a_div.active {
        background-color: #fdf8fa;
        color: white;
      }
      .a_div_b.with_bookmarks {
        background: #DDD;
      }
      .main_content_body {
        height: 1000px;
        margin-left: 25%;
        padding: 1px 16px;
      }""", """\
.a_div a /* !@# comment */{  display:  block; color: #000; padding: 8px 16px;text-decoration: none;}
.a_div a.active {background-color: #4CAF50;color:white;}
.a_div.active{background-color: #fdf8fa;/* !@# comment */color: white;}.a_div_b.with_bookmarks{background: #DDD;}
.a_div a:hover:not(.active){background-color:#555;color: white;}
.main_content_body{margin-left:25%;padding:1px 16px;height:1000px;}
"""

STRUCTURIZED_CSS = {
    '.main_content_body': {
        'height': '1000px',
        'margin-left': '25%',
        'padding': '1px 16px'
    },
    '.a_div a': {
        'color': '#000',
        'display': 'block',
        'padding': '8px 16px',
        'text-decoration': 'none'
    },
    '.a_div a.active': {
        'background-color': '#4CAF50',
        'color': 'white'
    },
    '.a_div a:hover:not(.active)': {
        'background-color': '#555',
        'color': 'white'
    },
    '.a_div.active': {
        'background-color': '#fdf8fa',
        'color': 'white'
    },
    '.a_div_b.with_bookmarks': {
        'background': '#DDD'
    }
}


def test_analyzing_empty_css():
    assert {} == dictionize_css('')


def test_forming_empty_css():
    assert '' == form_css({})


def test_forming_css_with_empty_rule():
    assert '  selector {}' == form_css({'selector': {}})


@pytest.mark.parametrize('input_css', RAW_CSSs, ids=map(str, range(len(RAW_CSSs))))
def test_analyzing_css(input_css):
    assert STRUCTURIZED_CSS == dictionize_css(input_css)


@pytest.mark.parametrize('input_css', RAW_CSSs, ids=map(str, range(len(RAW_CSSs))))
def test_forming_css(input_css):
    structured_css = dictionize_css(input_css)

    result = form_css(structured_css, indent_level=3)
    assert result == RAW_CSSs[0]
    restructured_css = dictionize_css(result)
    assert restructured_css == structured_css
