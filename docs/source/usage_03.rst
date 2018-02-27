Ways to feed it with CSS / JS resources
---------------------------------------

There are several possibilities to place a CSS and JS in html page. Each has some advantages.
Yawrap helps handling probably all of them.

.. literalinclude:: ../examples/test_usage_03_css.py
    :language: python
    :end-before: end of section A

Will create a page that has no style sheet (and no content) defined. It's just to show the `Tabula rasa` case, when 
the resources list is empty.

.. literalinclude:: _static/test_usage_03a.html
    :language: html

OK, but of course you would like to use the styles and scripts.

External resources
^^^^^^^^^^^^^^^^^^

This is how to reference resources hosted on external server.

.. literalinclude:: ../examples/test_usage_03_css.py
    :language: python
    :start-after: end of section A
    :end-before: end of section B

That gives:

.. literalinclude:: _static/test_usage_03b.html
    :language: html

Disadvantage of such approach is of course - dependency on other web resource, 
...but Yawrap doesn't care it's your business.

Auto-Linked resources
^^^^^^^^^^^^^^^^^^^^^

Yawrap can download the sheet or script given by URL (while page build), save it 
as a local file and manage its relative path calculation.

Just replace ``ExternalCss`` with ``LinkCss`` and ``ExternalJs`` with ``LinkJs`` like this:

.. literalinclude:: ../examples/test_usage_03_css.py
    :language: python
    :start-after: end of section B
    :end-before: end of section C

With such a result:

.. literalinclude:: _static/test_usage_03c.html
    :language: html

See how these link point to local files in ``resources`` directory?
It's a default location, next to output html file. Yawrap created it while build.

Let's say it once again *Yawrap downloads and saves the files with each run.*

If you allways want to get a fresh copy from these urls, it's ok. But it's probably eaiser to download it manually,
save it close to your yawrap generator code. While each run, yawrap will source its contents from local files,
instead of the web. Rest (i.e. saving to target resources dir) is the same as before.

Such a code will source the linked code from given files:

.. literalinclude:: ../examples/test_usage_03_css.py
    :language: python
    :start-after: end of section C
    :end-before: end of section D


Changing default resources path
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default ``resources`` output directory can be changed like this:

.. literalinclude:: ../examples/test_usage_03_css.py
    :language: python
    :start-after: end of section D
    :end-before: end of section E

This code will generate exactly the same HTML, just paths differ.

.. literalinclude:: _static/test_usage_03d.html
    :language: html

Note that JS and CSS will go to separate dirs.

.. note::
    Relative path management makes sense when several pages from different paths share same CSS/JS file. 
    E.g. when ``NavedYawrap`` is in use. Then the ``resources`` directory path is threated as relative to 
    the top level of output directory structure (relative to root, the first page).



Defining CSS / JS in python code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sometimes you would like to keep definition of the CSS or JS inside a python module. Especially if you use
python for generating it (e.g. calculate CSS colors, margin sizes, etc..)

Then there are 

If you are interested with getting single-file page (all-in-one, no linked CSS nor JS), where everything 
is embedded in single html, then use such an pattern: 

Replacing a `resource sourcer` ``LinkCss`` with ``EmbedCss`` as here::

    LinkCss.from_url("https://www.w3schools.com/w3css/4/w3.css")   # with
    EmbedCss.from_url("https://www.w3schools.com/w3css/4/w3.css") 

will cause downloading the w3 style sheet and placing it directly to the ``/html/head/style`` section.
The download happens with each call of ``Yawrap.render()``.

It also embeds additional style for body defined as a python string.

The most useful in my opinion is to
create own class derived from ``Yawrap`` (or ``NavedYawrap`` or whatever from the family).