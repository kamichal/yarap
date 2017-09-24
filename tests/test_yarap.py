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

    the_file = os.path.join(out_dir, 'test_1.html')

    jawrap = Yawrap()

    with jawrap.tag('div'):
        with jawrap.tag('p'):
            jawrap.text('pozoga')

    jawrap.render(the_file)

    assert os.path.isfile(the_file)