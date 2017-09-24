#!/usr/bin/python
'''
Created on 24 Sep 2017

@author: kamichal
'''
from bs4 import BeautifulSoup
import os

from yarap.yawrap import Yawrap


def test_1(out_dir):
    jarap = Yawrap('')
    assert jarap._get_body_render() == ''
    render = jarap._render_page()
    assert render == """\
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body></body>
</html>"""


YawrapWithCssStyle = '.some {margin: 2px;}'


class YawrapWithCss(Yawrap):
    css = YawrapWithCssStyle


def test_css(out_dir):
    jarap = YawrapWithCss('')

    assert jarap._get_body_render() == ''
    render = jarap._render_page()
    soup = BeautifulSoup(render)
    style = soup.html.head.style
    assert len(style) == 1
    assert style.text == YawrapWithCssStyle


def test_2(out_dir):
    the_file = os.path.join(out_dir, 'test_2.html')

    jawrap = Yawrap(the_file, 'ol rajt!')

    with jawrap.tag('div'):
        with jawrap.tag('p'):
            jawrap.text('Nothing much here.')

    assert jawrap._get_body_render() == """\
<div>
  <p>Nothing much here.</p>
</div>"""

    render = jawrap._render_page()
    jawrap.render()
    assert render == """\
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
    <title>ol rajt!</title>
  </head>
  <body>
    <div>
      <p>Nothing much here.</p>
    </div>
  </body>
</html>"""
    assert os.path.isfile(the_file)

