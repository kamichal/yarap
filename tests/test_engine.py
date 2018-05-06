from yawrap._engine import Tag, Doc


def test_sorting_attributes():
    attrs = {
        "class": 1,
        "id": 2,
        "name": 3,
        "src": 4,
        "href": 5,
        "alt": 6,
        "style": 7,
        "something": None,
    }
    expected_result = " class=1 id=2 name=3 src=4 href=5 something alt=6 style=7"
    assert Tag._form_attributes(attrs) == expected_result


def test_empty_doc():

    doc = Doc()
    assert doc.getvalue() == ""
    assert str(doc) == ""

    doc.text("thing")
    assert doc.getvalue() == "thing"
    assert str(doc) == "thing"


def test_simple_doc():
    doc = Doc()
    doc.asis('<!doctype html>\n')
    with doc.tag("html"):
        doc.comment("HERE COMMES THE HEAD!")
        with doc.tag("head"):
            doc.line("style", "that\nstyle\ndefinition")

        doc.comment("HERE COMMES THE BODY!")
        with doc.tag("body", id="the_id", klass="A"):
            with doc.tag("p", klass="B"):
                doc.text("that text")
            with doc.tag("div", id="content"):
                with doc.tag("ul", ("id", "di"), klass="Cc", style="the_style"):
                    doc.comment("AND THE LIST!")
                    for k in range(2):
                        doc.line("li", "that %s" % k, style="u")
                doc.text("that's it")

    assert str(doc) == """\
<!doctype html>
<html>
  <!-- HERE COMMES THE HEAD! -->
  <head>
    <style>
      that
      style
      definition
    </style>
  </head>
  <!-- HERE COMMES THE BODY! -->
  <body class='A' id='the_id'>
    <p class='B'>that text</p>
    <div id='content'>
      <ul class='Cc' id='di' style='the_style'>
        <!-- AND THE LIST! -->
        <li style='u'>that 0</li>
        <li style='u'>that 1</li>
      </ul>
      that's it
    </div>
  </body>
</html>"""


def test_simple_doc_with_raw_texts():
    doc = Doc()
    with doc.tag("html"):
        with doc.tag("head"):
            doc.line("style", "that")
            doc.cdata("the cdata string\nwith\nbroken\nlines")

        with doc.tag("body", id="the_id", klass="A"):
            with doc.tag("p", klass="B"):
                doc.text("that text")
            doc.text("that's it")
            doc.asis("<h2>\n  some <b>raw</b> html\n</h2>")

    assert str(doc) == """\
<html>
  <head>
    <style>that</style>
<![CDATA[the cdata string
with
broken
lines]]>
  </head>
  <body class='A' id='the_id'>
    <p class='B'>that text</p>
    that's it
<h2>
  some <b>raw</b> html
</h2>
  </body>
</html>"""


def test_1():

    doc = Doc()

    with doc.tag('body', "some_things", ("class", "tak"), klass="content"):
        with doc.tag('div', klass="olrajt", number=23):
            with doc.tag('p'):
                doc.text("dupa\nand here we have\n a multilne\ncontent")
                doc.text("once again")

        with doc.tag('main', id=12):
            doc.text("nastepna")
            doc.text("dupaa")
            with doc.tag("ul"):
                for k in range(1, 3):
                    with doc.tag('li', klass="ok"):
                        doc.text("That is a text and that's my boy! " * k)
                        with doc.tag("b"), doc.tag("strong"), doc.tag("i"):
                            doc.text("short %s" % k)
                doc.stag("img", href="#", alt="that")
                doc.line("li", "that line text ", klass="thing")

        with doc.tag("empty"):
            pass

        doc.line("empty")

    assert str(doc) == """\
<body class='content' some_things>
  <div class='olrajt' number=23>
    <p>
      dupa
      and here we have
       a multilne
      content
      once again
    </p>
  </div>
  <main id=12>
    nastepna
    dupaa
    <ul>
      <li class='ok'>
        That is a text and that's my boy! 
        <b><strong><i>short 1</i></strong></b>
      </li>
      <li class='ok'>
        That is a text and that's my boy! That is a text and that's my boy! 
        <b><strong><i>short 2</i></strong></b>
      </li>
      <img href='#' alt='that' />
      <li class='thing'>that line text </li>
    </ul>
  </main>
  <empty></empty>
  <empty></empty>
</body>"""
