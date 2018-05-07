Basic Usage
===========

Passing target file location to Yawrap constructor is mandatory, although the file 
will be not generated until ``Yawrap.render()`` is called. Title is optional.


.. literalinclude:: ../examples/test_usage_00.py
    :language: python

Will create a page that looks like this:

.. raw:: html

    <iframe src="_static/test_usage_00.html"></iframe>
