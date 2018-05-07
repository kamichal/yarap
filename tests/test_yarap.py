#!/usr/bin/python
'''
Created on 24 Sep 2017

@author: kamichal
'''
from bs4 import BeautifulSoup
import os

from yawrap import Yawrap, ExternalJs, EmbedCss, EmbedJs


def test_linking_a_local_file(out_dir):
    dummy_file = os.path.join(out_dir, 'some.html')
    dummy_target = os.path.join(out_dir, 'anything', 'index.html')

    jarap = Yawrap(dummy_target)
    with jarap.local_link(dummy_file):
        jarap.text('the target')

    render = jarap._render_page()
    soup = BeautifulSoup(render, "html.parser")
    link = soup.html.body.a
    assert link
    assert link['href'] == '../some.html'
    assert link.text.strip() == 'the target'


def test_basic(out_dir):
    the_file = os.path.join(out_dir, 'test_basic.html')
    jawrap = Yawrap(the_file, 'pleasure')
    with jawrap.tag('div'):
        with jawrap.tag('p'):
            jawrap.text('Nothing much here.')

    assert jawrap._render_page() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>pleasure</title>
  </head>
  <body><div><p>Nothing much here.</p></div></body>
</html>"""


def test_overloading(tmpdir):

    class MyRap(Yawrap):
        resources = [EmbedCss({'.content': {'color': '#daf'}})]

        def __init__(self, target_file):
            title = 'MyWrap'
            Yawrap.__init__(self, target_file, title)

            with self.tag('p'):
                self.text("that's my wrap")

    out_file = tmpdir.join('myRap.html')

    a = MyRap(str(out_file))
    a.render()

    assert out_file.read() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>MyWrap</title>
    <style>
  .content {
    color: #daf;
  }</style>
  </head>
  <body><p>that's my wrap</p></body>
</html>"""


def test_overloading_2(tmpdir):

    class MyJsPage(Yawrap):
        resources = [
            ExternalJs("https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"),
            EmbedCss("""
          .box {
            width:80px;
            height: 80px;
          }"""),
            EmbedJs("""\
          $(document).ready(function(){
              $("button").click(function(){
                  $("#div1").fadeToggle();
                  $("#div2").fadeToggle("slow");
                  $("#div3").fadeToggle(3000);
              });
          });""")]

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

    out_file = tmpdir.join('myRap.html')

    MyJsPage(str(out_file)).render()

    expected_page = """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>jQuery W3 example, js defined as class attribute.</title>
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
    <style>
          .box {
            width:80px;
            height: 80px;
          }</style>
    <script type='text/javascript'>
          $(document).ready(function(){
              $("button").click(function(){
                  $("#div1").fadeToggle();
                  $("#div2").fadeToggle("slow");
                  $("#div3").fadeToggle(3000);
              });
          });
    </script>
  </head>
  <body>
    <p>Demonstrate fadeToggle() with different speed parameters.</p>
    <button>Click to fade in/out boxes</button>
    <div class='box' id='div1' style='background-color:red;'></div>
    <br />
    <div class='box' id='div2' style='background-color:green;'></div>
    <br />
    <div class='box' id='div3' style='background-color:blue;'></div>
    <br />
  </body>
</html>"""

    assert out_file.read() == expected_page
