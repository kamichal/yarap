
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

Please reffer to :ref:`FadeExample <js_fade>`. It shows jQuerry usage.


.. _css-class-level:

Sharing scripts and styles across multiple pages
------------------------------------------------

Similar effect as above but with reusable java scripts and CSS can be obtained by defining them 
as class level attributes like this:

.. testcode::

    from bs4 import BeautifulSoup
    from yawrap import Yawrap, ExternalJs
 
    out_file1 = '/tmp/js_2a.html'
    out_file2 = '/tmp/js_2b.html'

    class MyJsPage(Yawrap):
        Resources = [
            ExternalJs("https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js")
        ]
        css = """
          .box { 
            width:80px;
            height: 80px;
          }"""
        js = ["""
          $(document).ready(function(){
              $("button").click(function(){
                  $("#div1").fadeToggle();
                  $("#div2").fadeToggle("slow");
                  $("#div3").fadeToggle(3000);
              });
          });
        """]

        def __init__(self, out_file):
            title = 'jQuery W3 example, js defined as class attribute.'
            Yawrap.__init__(self, out_file, title)

            with self.tag('p'):
                self.text("Demonstrate fadeToggle() with different speed parameters.")

            with self.tag('button'):
                self.text("Click to fade in/out boxes")

            self.create_box2('div1', "background-color:red;")
            self.create_box2('div2', "background-color:green;")
            self.create_box2('div3', "background-color:blue;")

        def create_box2(self, name, add_style):
            with self.tag('div', id=name, klass="box", style=add_style):
                pass
            self.stag('br')
       

    MyJsPage(out_file1).render()
    MyJsPage(out_file2).render()
   
    # helper function for assertions
    def soup(html_page):
        return BeautifulSoup(html_page, "lxml")

    expected = soup("""\
    <!doctype html>
    <html lang="en-US">
      <head>
        <meta charset="UTF-8" />
        <title>jQuery W3 example, js defined as class attribute.</title>
        <script>
          $(document).ready(function(){
              $("button").click(function(){
                  $("#div1").fadeToggle();
                  $("#div2").fadeToggle("slow");
                  $("#div3").fadeToggle(3000);
              });
          });
        </script>
        <style>
          .box {
            height: 80px;
            width: 80px;
          }</style>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
      </head>
      <body>
        <p>Demonstrate fadeToggle() with different speed parameters.</p>
        <button>Click to fade in/out boxes</button>
        <div style="background-color:red;" id="div1" class="box"></div>
        <br />
        <div style="background-color:green;" id="div2" class="box"></div>
        <br />
        <div style="background-color:blue;" id="div3" class="box"></div>
        <br />
      </body>
    </html>""")
    
    
    print(soup(open(out_file1, 'rt').read()) == expected, 
          soup(open(out_file2, 'rt').read()) == expected)

.. testoutput::

   (True, True)

Such a overloading of class attributes is useful using ``Navrap`` class. Some of its methods creates sub-pages 
being an instances of parent class, giving them the same JS and CSS.