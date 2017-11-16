Usage
=====

This is a tiny example. Such a code is sufficient to generate an html page:

.. doctest::

    >>> from yawrap import Yawrap
    >>> out_file = '/tmp/example_0.html'

    >>> jawrap = Yawrap(out_file)             # passing target file location is mandatory

    >>> with jawrap.tag('p'):                 # add a paragraph
    ...     jawrap.text('Hello yawrap!')      # and its content

    >>> jawrap.render()                       # creates the /tmp/example_0.html file

    >>> print(open(out_file, 'rt').read())    # view the created file
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
