Yawrap Documentation
====================


.. image:: https://travis-ci.org/kamichal/yarap.svg?branch=master
    :target: https://travis-ci.org/kamichal/yarap
    :alt: Build Status

.. image:: https://readthedocs.org/projects/yawrap/badge/?version=latest
    :target: http://yawrap.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/github/issues/kamichal/yarap.svg
    :target: https://github.com/kamichal/yarap/issues
    :alt: GitHub issues

.. image:: https://img.shields.io/pypi/pyversions/yawrap.svg
    :target: https://pypi.org/project/yawrap
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/status/yawrap.svg
    :target: https://pypi.org/project/yawrap
    :alt: PyPI - Development Status

.. image:: https://img.shields.io/pypi/format/yawrap.svg
    :target: https://pypi.org/project/yawrap
    :alt: PyPI - Package Format

.. image:: https://img.shields.io/pypi/v/yawrap.svg
    :target: https://pypi.org/project/yawrap
    :alt: PyPI

.. image:: https://img.shields.io/github/license/kamichal/yarap.svg
    :target: https://github.com/kamichal/yarap/blob/master/LICENSE
    :alt: GitHub license

Yawrap is a powerful, lightweight, pythonic `pseudo-static HTML` builder that works with:

    - ``python2.7``,
    - ``python3.4``-``python.3.6``
    - ``pypy``.

The name comes from something like `Yet Another Wrapper (of HTML code)`.


======== ======================================================
         link
======== ======================================================
Repo:    https://github.com/kamichal/yarap
OldRepo: https://bitbucket.org/gandowin/yarap (goes obsolete)
Docs:    http://yawrap.readthedocs.io
Pypi:    https://pypi.python.org/pypi/yawrap
Author:  Michał Kaczmarczyk from Poland
Email:   `michal.skaczmarczy.k at gmail.com`
======== ======================================================


Features
--------

* **Very nice syntax**

    No more headache caused by closing and indentation of HTML elements!
    Just write python code.

    Yawrap reflects python scopes in HTML perfectly - with no mistakes and indents it natively for free.

* :ref:`CSS <css-support>` & :ref:`JS <js-support>` support
    Handle it how you like. JS and CSS can be sourced either:

    - from local file
    - from url
    - from python string

    And it can be placed either:
    
    - as internal content
    - as external file
    - as linked resource.

    From single "All in one" HTML file to multi-page documents sharing CSS&JS resources. 
    Yawrap takes care for handling them properly.

* **SVG support**
    Don't care about defining SVG structure, just write its main contents. Yawrap will take care about the whole rest.
    Also typical SVG attributes which are problematic from python keyword-arguments point of view have it's
    convenience feature.

* **Linking local files**
    You can reference local files by passing its absolute path on python side and it will appear under links 
    relative to the current document. And you don't have to `calculate the paths`.  

* :ref:`Defining page style and scripts on python class level <css-class-level>`
    Page styles can be defined by deriving Yawrap classes. This makes possibility to get the styles 
    shared / inherited / override in well known `pythonic` way.

* :ref:`Multi-page structure <multi-page>`
    Define multiple pages (even in complex directory structure) and don't care about the paths. 
    Not existing directories will be automatically created, you just define the path of target file.

* **Automatic navigation**
    That's ultra-nice. **Probably the cutest yawrap's feature.** Create multiple pages and see how yawrap 
    joins them in navigation panel created for each generated page. Everything happens behind the curtains. 

    The only one thing you need to do is to care for the navigation's ``CSS`` style (if you don't like the
    default navigation style provided by Yawrap).

* **Bookmarking**
    Create intra-page bookmarks with just one command during document definition and see how they are inserted 
    in correct subsection of the page navigation.


Usage Examples
==============

Because a good example is worth more than thousand words.

.. toctree::
    :maxdepth: 1

    usage_00
    usage_01
    usage_03


Contents
========

.. toctree::
    :maxdepth: 2

    css_support
    js_support
    navrap
    examples


yattag's heritage
-----------------

Till ``Yawrap`` version 0.3.2 - its core was `yattag <https://pypi.python.org/pypi/yattag>`_. 
It used it as a library. But it's been decided to reimplement the XML-tag engine in own way. 
Yawrap requred more features and yattag was not able to provide it.
Since version 0.4. Yawrap has no external dependencies at all.

.. note::

    Yawrap is backward compatible with yattag. Vast functionality of ``yattag.SimpleDoc`` is supported.
    You can use yawrap in the same way as yattag or even just replace import statement in your existing code.
    Unfortunatelly I cannot guarantee 100% match, but I'm pretty sure it will work.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

