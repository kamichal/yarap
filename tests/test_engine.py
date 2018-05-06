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
    expected_order = " class=1 id=2 name=3 src=4 href=5 something alt=6 style=7"
    assert Tag._form_attributes(attrs) == expected_order


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
        <b>
          <strong>
            <i>short 1</i>
          </strong>
        </b>
      </li>
      <li class='ok'>
        That is a text and that's my boy! That is a text and that's my boy! 
        <b>
          <strong>
            <i>short 2</i>
          </strong>
        </b>
      </li>
      <img href='#' alt='that' />
      <li class='thing'>
        that line text 
      </li>
    </ul>
  </main>
  <empty></empty>
  <empty></empty>
</body>"""
