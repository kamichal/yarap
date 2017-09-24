#!/usr/bin/python
'''
Created on 24 Sep 2017

@author: kamichal
'''
import os
import pytest
import shutil


@pytest.fixture(scope='session')
def out_dir():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(tests_dir, 'out')
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    return out_dir
