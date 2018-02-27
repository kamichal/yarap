.. _js_fade:

Basic JS usage
--------------

More realistic usage. 

It's an adaptation of following example: 
https://www.w3schools.com/jquery/tryit.asp?filename=tryjquery_fadetoggle

.. literalinclude:: ../examples/test_usage_01.py
    :language: python
    :end-before: end section A

Will create a page as below. Note that the ``placement=BODY_END`` in ``EmbedJs`` call caused the script to 
be placed at the end. Withouth that argument it would get into ``head`` section. 

.. literalinclude:: _static/test_usage_01.html
    :language: html

That looks like this:

.. raw:: html

    <iframe src="_static/test_usage_01.html" height="285px" width="45%"></iframe>
