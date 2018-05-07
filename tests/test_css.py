from bs4 import BeautifulSoup

import pytest

from yawrap import Yawrap, NavedYawrap, EmbedCss, LinkCss, ExternalCss


CssStyle1 = '.some {margin: 2px;}'
CssStyle2 = '.other {\n padding: 0;\n}'


class DerivedFromYawrap(Yawrap):
    def __init__(self, target_file):
        super(DerivedFromYawrap, self).__init__(target_file)


class DerivedFromNavedYawrap(NavedYawrap):
    css = ''


class DerivedFromDerivedFromYawrap(DerivedFromYawrap):
    pass


CLASSES_TO_TEST = [Yawrap, DerivedFromYawrap, DerivedFromDerivedFromYawrap]


@pytest.fixture(params=CLASSES_TO_TEST)
def yawrap_class(request):
    yield request.param


@pytest.fixture(params=CLASSES_TO_TEST + [DerivedFromNavedYawrap])
def yawrap_class_with_naved(request):
    yield request.param


def test_empty_body(yawrap_class):
    jarap = yawrap_class('')
    assert jarap.getvalue() == """\
<!doctype html><html lang='en-US'>
  <head><meta charset='UTF-8' /></head>
  <body></body>
</html>"""


def test_empty_doc(yawrap_class_with_naved):
    jarap = yawrap_class_with_naved('')
    render = jarap.getvalue()

    if yawrap_class_with_naved == DerivedFromNavedYawrap:
        assert render == """\
<!doctype html><html lang='en-US'>
  <head><meta charset='UTF-8' /></head>
  <body><main class='main_content_body'></main></body>
</html>"""
    else:
        assert render == """\
<!doctype html><html lang='en-US'>
  <head><meta charset='UTF-8' /></head>
  <body></body>
</html>"""


def test_class_defined_css(yawrap_class_with_naved):

    class JarapWCss(yawrap_class_with_naved):
        resources = [
            EmbedCss(CssStyle1)
        ]

    jarap = JarapWCss('')
    jarap.add(EmbedCss(CssStyle2))
    render = jarap._render_page()
    soup = BeautifulSoup(render, "html.parser")
    assert [c.text for c in soup.html.head.children if c.name == "style"] == [CssStyle1, CssStyle2]


def test_link_local_style(out_dir, yawrap_class_with_naved, mocker):
    from yawrap._sourcer import os, _Resource, _ExportToTargetFs
    dummy_css = os.path.join(out_dir, 'some.css')
    dummy_target = os.path.join(out_dir, 'anything', 'index.html')
    mocker.patch.object(os.path, "isfile", return_value=True)
    mocker.patch.object(os.path, "isdir", return_value=True)
    mocker.patch.object(_Resource, "_read_file")
    mocker.patch.object(_ExportToTargetFs, "_save_as_file")

    jarap = yawrap_class_with_naved(dummy_target)
    jarap.add(LinkCss.from_file(dummy_css))
    render = jarap._render_page()
    soup = BeautifulSoup(render, "html.parser")
    link = soup.html.head.link
    assert link
    assert link['href'] == 'resources/some.css'
    assert link['type'] == 'text/css'
    assert link['rel'] == ['stylesheet']  # list? wtf soup?


def test_link_ext_style(yawrap_class_with_naved):
    jarap = yawrap_class_with_naved('')
    jarap.add(ExternalCss('http://css.org/great.css'))
    render = jarap._render_page()
    soup = BeautifulSoup(render, "html.parser")
    link = soup.html.head.link
    assert link
    assert link['href'] == 'http://css.org/great.css'
    assert link['type'] == 'text/css'
    assert link['rel'] == ['stylesheet']  # list? wtf soup?
