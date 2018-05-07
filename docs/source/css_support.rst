.. _css-support:

CSS Support
===========

.. testsetup:: *

   import os, sys
   root_dir = os.path.dirname(os.path.abspath('.'))
   sys.path.insert(0, root_dir)

Yawrap has it's basic support of cascade style sheets. During creation of html page you can 
append styles definition as strings or dictionaries. It will appear in ``/html/head/style`` section 
of current yawrap document. Also linking CSS as external file is possible. 

.. note ::
    
    The ``class`` keyword, widely used in ``html/css`` will cause python's syntax error if used as keyword argument, 
    so you can define it by typing ``klass`` instead. Yattag will convert it to ``class`` automatically. 

Internal CSS as str
-------------------

.. testcode::

    from yawrap import Yawrap, EmbedCss
    out_file = '/tmp/css_1.html'
    jawrap = Yawrap(out_file)

    with jawrap.tag('div', klass='content'):
        with jawrap.tag('span'):    
            jawrap.text('CSS in yawrap.')

    jawrap.add(EmbedCss('''
    .content { margin: 2px; }
    .content:hover {
       background-color: #DAF;
    }'''))
    jawrap.render()

    print(open(out_file, 'rt').read())

That outputs: 

.. testoutput::

    <!doctype html><html lang='en-US'>
      <head>
        <meta charset='UTF-8' />
        <style>
    .content { margin: 2px; }
    .content:hover {
       background-color: #DAF;
    }</style>
      </head>
      <body><div class='content'><span>CSS in yawrap.</span></div></body>
    </html>


The method :func:`add` called with action :func:`EmbedCss` appends CSS definitions to page head section.
It can be called several times, output CSS will be sorted and nicely joined.

The passed CSS can be a string without any formatting. It will be reformatted during page generation.

Internal CSS as python's dict
-----------------------------

The argument passed to :func:`add_css` can be a regular python dictionary definins css.  

.. testcode::

    css_dict = {
      '.content': {
        'color': '#321',
        'padding': '1px 16px'
      },
      'span': {
        'border': '1px solid black'
      }
    }
    # reusing jawrap instance from subsection above.
    jawrap.add(EmbedCss(css_dict))
    jawrap.render()

    print(open(out_file, 'rt').read())

Will give:

.. testoutput::

    <!doctype html><html lang='en-US'>
      <head>
        <meta charset='UTF-8' />
        <style>
    .content { margin: 2px; }
    .content:hover {
       background-color: #DAF;
    }</style>
        <style>

      .content {
        color: #321;
        padding: 1px 16px;
      }
      span {
        border: 1px solid black;
      }
        </style>
      </head>
      <body><div class='content'><span>CSS in yawrap.</span></div></body>
    </html>


Note the previous ``.content`` selector's definition is overwritten with new one.

External CSS from local file
----------------------------

It's also possible to link style sheet from local file. It's source can be placed anywhere as long as 
it's accessible for build process. Yawrap will copy it and place in default ``resources`` directory, next to 
target file (or next to root document)::

    from yawrap import Yawrap, LinkCss
    out_file = '/tmp/css_2.html'

    jawrap = Yawrap(out_file)
    jawrap.text('CSS from local file.')
    jawrap.add(LinkCss.from_file('/tmp/files/my.css'))
    jawrap.render()


External CSS from web
---------------------

Using global CSS from some resources can be obtained by calling :func:`add` with ``ExternalCss`` object.

.. testcode::

    from yawrap import Yawrap, ExternalCss
    out_file = '/tmp/css_3.html'
    
    jawrap = Yawrap(out_file)
    jawrap.text('CSS from web.')
    jawrap.add(ExternalCss("https://www.w3schools.com/w3css/4/w3.css"))
    
    html = jawrap.getvalue()
    print(html)

.. testoutput::

    <!doctype html><html lang='en-US'>
      <head>
        <meta charset='UTF-8' />
        <link type='text/css' href='https://www.w3schools.com/w3css/4/w3.css' rel='stylesheet' />
      </head>
      <body>CSS from web.</body>
    </html>



CSS defined on class level
--------------------------

You can derive own class from ``Yawrap`` or ``Navrap`` class and define its CSS that will be inherited 
in its subclasses. You have to define `css` class attribute either as a string or a dictionary.

.. testcode::

    from yawrap import Yawrap, EmbedCss
    out_file = '/tmp/css_4.html'

    class MyStyledPage(Yawrap):
        resources = [EmbedCss('''\
            body { 
              margin: 0px;
              padding: 13px 14px;
            }
            .content {
               color: #BAC;
               margin: 2px;
            }''')
    ]

    myStyled = MyStyledPage(out_file)
    with myStyled.tag('div', klass='content'):
        myStyled.text('Deriving CSS.')

    myStyled.render()

    print(open(out_file, 'rt').read())

Should give:

.. testoutput::

    <!doctype html><html lang='en-US'>
      <head>
        <meta charset='UTF-8' />
        <style>
            body {
              margin: 0px;
              padding: 13px 14px;
            }
            .content {
               color: #BAC;
               margin: 2px;
            }
        </style>
      </head>
      <body><div class='content'>Deriving CSS.</div></body>
    </html>



Adding CSS is still possible, but to instance of the derived class (to ``myStyled`` above), not 
to the class definition (here ``MyStyledPage``), so the appended CSS will not be inherited.

