import pytest

from ._test_utils import walk_html, get_soup, assert_html_equal, minify


SAMPLE_HTML_PRETTY = """\
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Title One</title>
    <style>
body {
  font-family: Verdana, sans-serif;
  margin: 16;
}</style>
  </head>
  <body style="color: #5f5; background: #FFD">
    <div class="thing" id="id1">
      <p id="pak" class="ok">
        that\'s all<br>
        new line

      </p>
    </div>
    <img href="12">
  </body>
  </html>"""


def test_walk():

    assert walk_html(get_soup(SAMPLE_HTML_PRETTY)) == (
        u'[document]', {}, [
            ('html', {}, [
                ('head', {}, [
                    ('meta', {'charset': u'UTF-8'}, []),
                    ('title', {}, [u'Title One']),
                    ('style', {}, [u'body {\n  font-family: Verdana, sans-serif;\n  margin: 16;\n}']),
                ]),
                ('body', {'style': 'color: #5f5; background: #FFD'}, [
                    ('div', {'class': ['thing'], 'id': 'id1'}, [
                        ('p', {'id': 'pak', 'class': ['ok']}, [
                            u"that's all",
                            ('br', {}, []),
                            u'new line'
                        ])
                    ]),
                    ('img', {'href': '12'}, [])
                ])
            ])
        ])


COMPARE_TEST = [
    SAMPLE_HTML_PRETTY,
    "\n\n" + SAMPLE_HTML_PRETTY + "\n\n",
    SAMPLE_HTML_PRETTY.replace('class="thing" id="id1"', 'id="id1" class="thing"'),
    SAMPLE_HTML_PRETTY.replace('class="thing" id="id1"', 'id = "id1"  class ="thing"'),
    minify(SAMPLE_HTML_PRETTY),
]


@pytest.mark.parametrize("other", COMPARE_TEST, ids=[str(i) for i, _ in enumerate(COMPARE_TEST)])
def test_compare_same(other):
    assert_html_equal(SAMPLE_HTML_PRETTY, other)


COMPARE_DIFFERING_TEST = [
    '',
    "<html><head></head><body></body></html>",
    """<html>
  <head>
    <meta charset="UTF-8" />
    <title>Different text value</title>
    <style>
body {
  font-family: Verdana, sans-serif;
  margin: 16;
}</style>
  </head>
  <body style="color: #5f5; background: #FFD">
    <div class="thing" id="id1">
      <p id="pak" class="ok">
        that\'s all<br>
        new line

      </p>
    </div>
    <img href="12">
  </body>
  </html>""", """\
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Title One</title>
    <style>
body {
  font-family: Verdana, sans-serif;
  margin: 16;
}</style>
  </head>
  <body style="color: #5f5; background: #FFD">
    <div class="thing" id="different id">
      <p id="pak" class="ok">
        that\'s all<br>
        new line

      </p>
    </div>
    <img href="12">
  </body>
  </html>""",
]


@pytest.mark.parametrize("other", COMPARE_DIFFERING_TEST, ids=[str(i) for i, _ in enumerate(COMPARE_DIFFERING_TEST)])
def test_compare_differing(other):
    with pytest.raises(AssertionError) as err:
        assert_html_equal(SAMPLE_HTML_PRETTY, other)
    assert err
