import pytest

from yawrap._engine import Tag, Doc


class TestTag:

    def test_sorting_attributes(self):
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

    def test_badly_typed(self):
        with pytest.raises(ValueError, match="Attribute argument must be tuple of 2 elements \(name, value\)."):
            Tag("name", ("bad", "number", "of elements"))

    def test_bad_types(self):
        with pytest.raises(ValueError, match="Couldn't make an attribute & value pair out of <object object"):
            Tag("name", object())


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
            doc.line("style", '#that {\ncss: style;\ndefinition: 1px;\n}')

        doc.nl()
        doc.comment("HERE COMMES THE BODY!")
        with doc.tag("body", "optional", id="the_id", klass="A"):
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
      #that {
      css: style;
      definition: 1px;
      }
    </style>
  </head>

  <!-- HERE COMMES THE BODY! -->
  <body class='A' id='the_id' optional>
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
    with doc.tag("doc"):
        doc.cdata("the cdata string\nwith\nbroken\nlines")

        with doc.tag("body", id="the_id", klass="A"):
            doc.asis("<h2>\n  some <b>raw</b> html\n</h2>")
            doc.text("that's it")
    assert str(doc) == """\
<doc>
<![CDATA[the cdata string
with
broken
lines]]>
  <body class='A' id='the_id'>
<h2>
  some <b>raw</b> html
</h2>
    that's it
  </body>
</doc>"""


class TestClassesHandling():
    def test_classes_handling(self):
        doc = Doc()

        with doc.tag("main", klass="bad_class primary light"):
            with doc.tag("div", id="c", klass="inside", style="B"):
                with doc.tag('p', klass="paragraph"):
                    doc.text("some")
                    doc.text("text")
                    doc.discard_class("paragraph")
                doc.toggle_class("option")

            doc.add_class("secondary")
            doc.discard_class("bad_class")
            doc.toggle_class("light")

        assert str(doc) == """\
<main class='primary secondary'>
  <div class='inside option' id='c' style='B'>
    <p>
      some
      text
    </p>
  </div>
</main>"""

    def test_operations_on_root_level(self):
        with pytest.raises(AssertionError, match="Root element has no classes."):
            Doc().add_class("root level")
        with pytest.raises(AssertionError, match="Root element has no classes."):
            Doc().toggle_class("root level")
        with pytest.raises(AssertionError, match="Root element has no classes."):
            Doc().discard_class("root level")

    def test_toggling(self):
        doc = Doc()
        with doc.tag("one", klass="B A C"):
            doc.text("text")
            doc.toggle_class("B B D")
        assert str(doc) == "<one class='A C D'>text</one>"

    def test_discarding(self):
        doc = Doc()
        with doc.tag("one", klass="B  A C"):
            doc.discard_class("B N D")
        assert str(doc) == "<one class='A C'></one>"
