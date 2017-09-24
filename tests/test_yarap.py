#!/usr/bin/python
'''
Created on 24 Sep 2017

@author: kamichal
'''
import os
import pytest
from yarap.yawrap import Yawrap


@pytest.fixture(scope='session')
def out_dir():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(tests_dir, 'out')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    return out_dir


def test_1(out_dir):
    assert str(Yawrap()) == ''
    render = Yawrap().render()
    assert render == """\
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body></body>
</html>"""


def test_2(out_dir):
    the_file = os.path.join(out_dir, 'test_2.html')

    jawrap = Yawrap('ol rajt!')
    jawrap.css("body {padding: 12px;}")

    with jawrap.tag('div'):
        with jawrap.tag('p'):
            jawrap.text('Nothing much here.')

    assert str(jawrap) == """\
<div>
  <p>Nothing much here.</p>
</div>"""

    render = jawrap.render()
    jawrap.render_to_file(the_file)
    assert render == """\
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
    <title>ol rajt!</title>
    <style>body {padding: 12px;}</style>
  </head>
  <body>
    <div>
      <p>Nothing much here.</p>
    </div>
  </body>
</html>"""
    assert os.path.isfile(the_file)
