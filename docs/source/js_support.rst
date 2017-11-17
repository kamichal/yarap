
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