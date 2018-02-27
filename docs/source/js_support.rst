
.. testsetup:: *

   import os, sys
   root_dir = os.path.dirname(os.path.abspath('.'))
   sys.path.insert(0, root_dir)


.. _js-support:

JavaScript support
==================

Yattag does not modify nor even analyze added ``js`` sources. You provide them as strings and these are rendered in
``/html/head/script`` section. Each addition places the content in separate ``<script>`` section.

Of course there is also possibility to link external ``js`` source file.


Internal JS
-----------

Appending js to ``Yawrap`` or ``Navrap`` instances can be done appending string-code to Class 

.. note::

    Yawrap has a class-level atribute being a list named ``js``. It is supposed to contain JavaScript code as strings.
    Similary as with CSS, you can derive from ``Yawrap`` class and also define the class-level JS that will be 
    inherited by its subclasses unless you override it.


Using jQuery
-------------

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


Sharing scripts and styles across multiple pages
------------------------------------------------

Similar effect as above but with reusable java scripts and CSS can be obtained by defining them 
as class level attributes like this:

.. literalinclude:: ../examples/test_usage_01.py
    :language: python
    :start-after: end section A
    :end-before: end section B

Which produces the page:

.. literalinclude:: _static/test_usage_01_linked.html
    :language: html

..and the script ``resources/common_linked.js``:

.. literalinclude:: _static/resources/common_linked.js
    :language: js

..and the style ``resources/common_linked.css``:

.. literalinclude:: _static/resources/common_linked.css
    :language: css
