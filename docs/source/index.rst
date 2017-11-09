.. yawrap documentation master file, created by
   sphinx-quickstart on Wed Nov  8 22:51:37 2017.

yawrap - yet another wrapper
============================

Yawrap is a pseudo static html (actually a xml) builder.


yattag
------

Yawrap core is `yattag <https://pypi.python.org/pypi/yattag>`_  library written by Benjamin Le Forestier.

The yattag is very well documented and I strongly recommend reading its `quick reference <http://www.yattag.org/>`_.

Unfortunately when I asked Benjamin for extending yattag functionality,
he suggested to make it a separate package, so that's how the yawrap was born.



Usage
=====

This is a tiny example. Such a code is sufficient to generate an html page:

.. doctest::

    >>> from yawrap import Yawrap

    >>> jawrap = Yawrap('/tmp/example_0.html')

    >>> with jawrap.tag('p'):
    ...     jawrap.text('Hello yawrap!')

    >>> jawrap.render()

    >>> print open('/tmp/example_0.html', 'rt').read()
    <!doctype html>
    <html lang="en-US">
      <head>
        <meta charset="UTF-8" />
      </head>
      <body>
        <p>Hello yawrap!</p>
      </body>
    </html>

After executing that - calling `render()` function will store the 
page in a target file specified in `Yawrap` constructor ``/tmp/example_0.html``:

Yawrap Parameters
=================

The basic object is :class:`yawrap.Yawrap`. Its constuctor is called by::

    Yawrap(target_file, title='', parent=None, defaults=None, errors=None,
           error_wrapper=('<span class="error">', '</span>'), stag_end=' />')


target_tile : str
    Path to the file that is supposed to be writen with html contents. Its directory will be created if is not existing.

parent : <yawrap.Yawrap object>
    Optional reference to another Yawrap class instance. It's parent object in documents tree.
    Is used only in derived classes.


Parameters inherited from ``yattag.Doc()``
------------------------------------------

defaults : dict
    Optional dictionnary of values used to fill yattag's html forms.

errors : dict
    Optional dictionnary of errors used to fill yattag's html forms.

error_wrapper : tuple(str, str)
    Couple of openning and clossing tags that will wrap errors occured during yattag's form generation. 
    The default is: ``<span class="error">`` and ``</span>``.

stag_end : str
    Empty tag closing style. One of:  ``' />'``, ``'/>'``, or ``'>'``. 
    E.g. for ``br`` will result: ``'<br />'`` by default, you can change it to ``'<br/>'`` or ``'<br>'``.

for more info, please visit: `Yattag - HTML forms rendering <http://www.yattag.org/#html-forms-rendering>`_.



Contents:

.. toctree::
   :maxdepth: 2
   
   examples


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

