.. yawrap documentation master file, created by
   sphinx-quickstart on Wed Nov  8 22:51:37 2017.


Yawrap Documentation
====================

Yawrap is a powerful, lightweight  `pseudo-static HTML` builder working in ``python2.7``,
``python3.4`` and ``python.3.5``.

The name comes from something like `Yet Another Wrapper (of HTML tags)` and has its coincidence to yattag package.


======== ======================================================
resource link
======== ======================================================
Repo:    https://bitbucket.org/gandowin/yarap
Docs:    http://yawrap.readthedocs.io
Pypi:    https://pypi.python.org/pypi/yawrap
email:   `Michał Kaczmarczyk <mailto:michal.skaczmarczy.k@gmail.com?Subject=Yawrap>`_
======== ======================================================



.. image:: https://readthedocs.org/projects/yawrap/badge/?version=latest
    :target: http://yawrap.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


yattag's heritage
-----------------

Yawrap's core is `yattag <https://pypi.python.org/pypi/yattag>`_ . It's a ultra-lightweight library written 
by `Benjamin Le Forestier <http://leforestier.org/python-developer>`_. 
Yattags's main functionality is care of proper opening and closing HTML (actually XML) tags.
However if you use `yattag` you probably noticed that in order to create a nice HTML page, you have to write a lot 
of code that is not exactly the content of your page and each time you have to care for the same aspects of the page 
- such as proper ``html head/body`` structure, links, navigation ect...
Yawrap extends yattag's functionality `(and adds some more)`. 

.. note::

    Yawrap classes are derived from 
    Yattag's ``Doc()`` class. So you can use e.g. its ``tag``, ``line``, ``text``, methods in the same way.
    Yattag is well documented and its strongly recommend to read its awesome 
    `quick reference <http://www.yattag.org/>`_.


Yawrap features
---------------

Here is a list of things that ``yawrap`` offers:

* :ref:`CSS <css-support>` & :ref:`JS <js-support>` support
   Append internal CSS styles or JS at any point of document definition. Allows for conditional additions of CSS or JS. 
   ...and you don't have to care about when to insert its definition. Even if you already finished defining the body
   and you define JS after that - it will be placed in ``/html/head/``.
   
   You can also easily link style sheet or java script from external file (local or from web).

* **SVG support**
   Don't care about defining SVG structure, just write its main contents. Yawrap will take care about the whole rest.
   Also typical SVG attributes which are problematic from python keyword-arguments point of view have it's
   convenience feature.

* **Linking local files**
   You can reference local files by passing its absolute path on python side and it will appear under links 
   relative to the current document. And you don't have to `calculate the paths`.  

* :ref:`Defining page style and scripts on python class level <css-class-level>`
   Page styles can be defined by deriving Yawrap classes. This makes possibility to get the styles 
   shared / inherited / override in well known `pythonic` way.

* :ref:`Multi-page structure <multi-page>`
   Define multiple pages in complex directory structure and don't care about the paths. 
   Not existing directories will be automatically created, you just define the path of target file.

* **Automatic navigation**
   That's ultra-nice. **Probably the cutest yawrap's feature.** Create multiple pages and see how yawrap 
   joins them in navigation panel created for each generated page. Everything happens behind the curtains. 

   The only one thing you need to do is to care for the navigation's ``CSS`` style (if you don't like the
   default navigation style provided by Yawrap).

* **Bookmarking**
   Create intra-page bookmarks with just one command during document definition and see how they are inserted 
   in correct subsection of the page navigation.


Usage Examples
==============

Because a good example is worth more than thousand words.

.. toctree::
   :maxdepth: 1

   usage_00
   usage_01
   usage_02
   usage_03


Contents
========

.. toctree::
   :maxdepth: 2

   css_support
   js_support
   navrap
   examples


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

