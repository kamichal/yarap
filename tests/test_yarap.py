#!/usr/bin/python
'''
Created on 24 Sep 2017

@author: kamichal
'''
import os
import pytest
from yarap.yawrap import Yawrap, NavedYawrap


@pytest.fixture(scope='session')
def out_dir():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(tests_dir, 'out')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    return out_dir


def test_1(out_dir):
    jarap = Yawrap('')
    assert str(jarap) == ''
    render = jarap._render_page()
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

    jawrap = Yawrap(the_file, 'ol rajt!')
    jawrap.css("body {padding: 12px;}")

    with jawrap.tag('div'):
        with jawrap.tag('p'):
            jawrap.text('Nothing much here.')

    assert str(jawrap) == """\
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
    <style>body {padding: 12px;}</style>
  </head>
  <body>
    <div>
      <p>Nothing much here.</p>
    </div>
  </body>
</html>"""
    assert os.path.isfile(the_file)



def test_navigation(out_dir):

    def make_content(jarap_, text):
        with jarap_.tag('p'):
            jarap_.text(text)
        with jarap_.tag('p'):
            jarap_.text("And I'm enjoying the navigation.")

    index_file = os.path.join(out_dir, 'test_subs_index.html')
    parent = NavedYawrap(index_file, 'Index')
    make_content(parent, "I'm a parent")

    child_file0 = os.path.join(out_dir, 'test_subs_child0.html')
    child0 = parent.sub(child_file0, 'child 0')
    make_content(child0, "I'm a child 0")

    child_file1 = os.path.join(out_dir, 'test_subs_child1.html')
    child1 = parent.sub(child_file1, 'child 1')
    make_content(child1, "I'm a child 1")

    child_file2 = os.path.join(out_dir, 'test_subs_subdir', 'test_subs_child2.html')
    child2 = child1.sub(child_file2)
    make_content(child2, "I'm a child 2. No title")

    child_file3 = os.path.join(out_dir, 'test_subs_subdir', 'test_subs_child3.html')
    child3 = parent.sub(child_file3)
    make_content(child3, "I'm a child 3. I don't have a title.")

    parent.render_all_files()

    assert all(os.path.isfile(f) for f in (index_file, 
                                           child_file1,
                                           child_file2,
                                           child_file3))

    print child2._get_nav_structure()

    