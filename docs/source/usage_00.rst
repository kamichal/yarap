Basic Usage
===========

This is a tiny basic example. Such a code is sufficient to generate an html page.

Passing target file location to Yawrap constructor is mandatory, although the file 
will be not generated until ``Yawrap.render()`` is called. Title is optional.


.. literalinclude:: ../examples/test_usage_00.py
    :language: python
    :end-before: def test_that

Will create such an page:

.. literalinclude:: _static/test_usage_00.html
    :language: html

Which looks like this:

.. raw:: html

    <iframe src="_static/test_usage_00.html"></iframe>
