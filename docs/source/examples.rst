Examples
========

.. testsetup:: *

   import os, sys
   root_dir = os.path.dirname(os.path.abspath('.'))
   sys.path.insert(0, root_dir)


This is a tiny example. Such a code is sufficient to generate an html page:

.. doctest::

    >>> from yawrap import Yawrap

    >>> jawrap = Yawrap('/tmp/example_1.html', 'the title')
    >>> with jawrap.tag('div'):
    ...     with jawrap.tag('p'):
    ...         jawrap.text('Nothing much here.')


After executing that - calling `render()` function will store the 
page in a target file specified in `Yawrap` constructor:

.. doctest::

   >>> jawrap.render()
   >>> print(open('/tmp/example_1.html', 'rt').read())
   <!doctype html>
   <html lang="en-US">
     <head>
       <meta charset="UTF-8" />
       <title>the title</title>
     </head>
     <body>
       <div>
         <p>Nothing much here.</p>
       </div>
     </body>
   </html>

.. note::
    That
   