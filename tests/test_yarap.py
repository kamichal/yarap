#!/usr/bin/python
'''
Created on 24 Sep 2017

@author: kamichal
'''
from bs4 import BeautifulSoup
import os
import pytest

from yawrap import Yawrap


def test_linking_a_local_file(out_dir):
    dummy_file = os.path.join(out_dir, 'some.html')
    dummy_target = os.path.join(out_dir, 'anything', 'index.html')

    jarap = Yawrap(dummy_target)
    with jarap.local_link(dummy_file):
        jarap.text('the target')
    render = jarap._render_page()
    soup = BeautifulSoup(render, "lxml")
    link = soup.html.body.a
    assert link
    assert link['href'] == '../some.html'
    assert link.text == 'the target'


def test_basic(out_dir):
    the_file = os.path.join(out_dir, 'test_basic.html')

    jawrap = Yawrap(the_file, 'pleasure')
    with jawrap.tag('div'):
        with jawrap.tag('p'):
            jawrap.text('Nothing much here.')

    render = jawrap._render_page()
    assert render == """\
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
    <title>pleasure</title>
  </head>
  <body>
    <div>
      <p>Nothing much here.</p>
    </div>
  </body>
</html>"""
