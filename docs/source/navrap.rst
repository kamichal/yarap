.. _multi-page:

Multiple-page structure with navigation
=======================================

It's easy to navigate between several files in different paths, using ``sub()`` method of NavedYawrap instance.
Each call of ``sub()`` returns instance of given NavedYawrap class, with same styles and scripts as the parent one.
Each page will be rendered with navigation section, with relative paths. See the hrefs in the example below.

The first document (``home`` in this example) will be the `root` of the document structure. 

.. literalinclude:: ../examples/test_navrap.py
    :language: python
    :end-before: doc end_here

Generates two html pages:

.. literalinclude:: _static/nav01a.html
    :language: html

Notice, how the href is calculated.

.. literalinclude:: _static/some/deep/nonexistent/path/nav01b.html
    :language: html

Here's the page:

.. raw:: html

    <iframe src="_static/nav01a.html" height="225px" width="100%"></iframe>
