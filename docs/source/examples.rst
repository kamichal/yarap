Examples
========

.. testsetup:: *

   import os, sys
   root_dir = os.path.dirname(os.path.abspath('.'))
   sys.path.insert(0, root_dir)

   
This is a tiny example. Such a code is sufficient to generate a html page:

.. doctest::

    >>> from yawrap import Yawrap

    >>> jawrap = Yawrap('/tmp/example_1.html', 'pleasure')
    >>> with jawrap.tag('div'):
    ...     with jawrap.tag('p'):
    ...         jawrap.text('Nothing much here.')


After executing that - calling `render()` function will store the 
page in a target file specified in `Yawrap` constructor:

.. doctest::

   >>> jawrap.render()
   >>> with open('/tmp/example_1.html', 'rt') as page:
   ...     print page.read()
   <!doctype html>
   <html lang="en-US">
     <head>
       <meta charset="UTF-8" />
       <title>pleasure</title>
     </head>
     <body>
       <div>
         <p>Nothing much here.</p>
       </div>
     </body>
   </html>
