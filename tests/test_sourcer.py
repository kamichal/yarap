
from bs4 import BeautifulSoup
from itertools import product
import posixpath
import pytest

from yawrap import Yawrap, NavedYawrap, ExternalJs, ExternalCss, EmbedJs, EmbedCss, LinkJs, LinkCss, BODY_BEGIN, \
    BODY_END, _sourcer
from yawrap._sourcer import os, PLACEMENT_OPTIONS


@pytest.fixture
def mocked_urlopen(mocker):

    class MockedUrlopen(object):
        def __init__(self, url, *_, **__):
            self.url = url

        def read(self, *_):
            basename = posixpath.basename(self.url)

            if basename.endswith(".css"):
                return " #%s {color: #BAD;}" % basename
            return "Dummy response to {}".format(self.url)

        def close(self, *_):
            pass

    mocker.patch.object(_sourcer, "urlopen", side_effect=lambda *p, **k: MockedUrlopen(*p, **k))


@pytest.fixture
def mocked_read_file(mocker):
    def read_file_stub(file_path):
        basename = os.path.basename(file_path)
        if basename.endswith(".css"):
            return " #%s {background: #AFE;}" % basename
        return "That's a dummy content of %s file." % file_path

    mocker.patch.object(os.path, "isfile", return_value=True)
    mocker.patch.object(os.path, "isdir", return_value=True)
    mocker.patch.object(_sourcer._Resource, "_read_file", side_effect=read_file_stub)


@pytest.fixture
def mocked_save_file(mocker):
    m = mocker.patch.object(_sourcer._ExportToTargetFs, "_save_as_file")
    return m


def test_linking_external_resources_in_head():

    class MyRap(Yawrap):
        resources = [
            ExternalCss("https://www.css.com/css.css"),
            ExternalJs("https://www.js.com/js.js"),
        ]

    doc = MyRap("that_file.html")
    with doc.tag("p"):
        doc.text("The body content")
    assert doc.getvalue() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <link type='text/css' href='https://www.css.com/css.css' rel='stylesheet' />
    <script src='https://www.js.com/js.js'></script>
  </head>
  <body><p>The body content</p></body>
</html>"""


def test_embedding_in_head(mocked_urlopen, mocked_read_file, mocked_save_file, tmpdir):

    class MyRap(Yawrap):
        resources = [
            EmbedCss("head { background: #DAD; }"),
            EmbedJs('console.log("alles klar in the head")'),

            EmbedCss.from_url("http://www.css.in/da.house.css"),
            EmbedJs.from_url('http://www.js.in/the.head.js'),

            EmbedCss.from_file("/path/to/style_to_embed.css"),
            EmbedJs.from_file("/path/to/script_to_embed.js"),
        ]

    doc = MyRap(str(tmpdir.join("that_file.html")))
    with doc.tag("p"):
        doc.text("The body content")

    assert doc.getvalue() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <style>head { background: #DAD; }</style>
    <script type='text/javascript'>console.log("alles klar in the head")</script>
    <style> #da.house.css {color: #BAD;}</style>
    <script type='text/javascript'>Dummy response to http://www.js.in/the.head.js</script>
    <style> #style_to_embed.css {background: #AFE;}</style>
    <script type='text/javascript'>That's a dummy content of /path/to/script_to_embed.js file.</script>
  </head>
  <body><p>The body content</p></body>
</html>"""


def test_embedding_in_body(mocked_urlopen, mocked_read_file, mocked_save_file, tmpdir):

    class MyRap(Yawrap):
        resources = [
            EmbedJs('console.log("alles klar in the body")', placement=BODY_BEGIN),
            EmbedJs.from_url('http://www.js.in/the.body.js', placement=BODY_BEGIN),
            EmbedJs.from_file("/path/to/script_to_embed.js", placement=BODY_END),
        ]

    doc = MyRap(str(tmpdir.join("that_file.html")))
    with doc.tag("p"):
        doc.text("The body content")

    assert doc.getvalue() == """\
<!doctype html><html lang='en-US'>
  <head><meta charset='UTF-8' /></head>
  <body>
    <script type='text/javascript'>console.log("alles klar in the body")</script>
    <script type='text/javascript'>Dummy response to http://www.js.in/the.body.js</script>
    <p>The body content</p>
    <script type='text/javascript'>That's a dummy content of /path/to/script_to_embed.js file.</script>
  </body>
</html>"""


def test_linking_local_files_in_head(mocked_urlopen, mocked_read_file, mocked_save_file, tmpdir):

    class MyRap(Yawrap):
        resources = [
            LinkCss("#nothing {}", file_name="that_new_style.css"),
            LinkJs("Store that script to the file.js", file_name="that_new_script.js", placement=BODY_END),

            LinkCss.from_url("https://want.to/have/it/in/my/head.css"),
            LinkJs.from_url("https://want.to/have/it/in/my/head.js"),

            LinkCss.from_file("/link/to/local_style.css"),
            LinkJs.from_file("link/to/local_script.js"),
        ]

    doc = MyRap(str(tmpdir.join("that_file.html")))

    with doc.tag("p"):
        doc.text("The body content")

    assert doc.getvalue() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <link type='text/css' href='resources/that_new_style.css' rel='stylesheet' />
    <link type='text/css' href='resources/head.css' rel='stylesheet' />
    <script src='resources/head.js'></script>
    <link type='text/css' href='resources/local_style.css' rel='stylesheet' />
    <script src='resources/local_script.js'></script>
  </head>
  <body>
    <p>The body content</p>
    <script src='resources/that_new_script.js'></script>
  </body>
</html>"""


def test_saving_files(tmpdir):
    css_definition = "#selector { color: #BAC; margin: 0;}"
    css_file_name = "that_new_style.css"
    css_rel_path = posixpath.join(LinkCss.resource_subdir, css_file_name)
    out_file = tmpdir.join("test_saving_files.html")
    css_file = tmpdir.join(LinkCss.resource_subdir, css_file_name)

    class MyRap(Yawrap):
        resources = [
            LinkCss(css_definition, file_name=css_file_name),
        ]

    doc = MyRap(str(out_file))
    assert BeautifulSoup(doc._render_page(), "html.parser").html.head.link['href'] == css_rel_path
    assert css_file.read() == css_definition


@pytest.fixture
def custom_link_dir():
    previous_value = LinkCss.resource_subdir
    LinkCss.resource_subdir = "custom/css/dir"
    LinkJs.resource_subdir = "custom/js/dir"
    yield
    LinkCss.resource_subdir = previous_value
    LinkJs.resource_subdir = previous_value


def test_linking_local_files_in_head_custom_loc(mocked_urlopen, mocked_read_file, mocked_save_file, tmpdir,
                                                custom_link_dir):

    class MyRap(Yawrap):

        resources = [
            LinkCss("#nothing {}", file_name="that_new_style.css"),
            LinkCss.from_url("https://want.to/have/it/from_web.css"),
            LinkCss.from_file("/link/to/local_style.css"),

            LinkJs("Store that script to the file.js", file_name="that_new_script.js"),
            LinkJs.from_url("https://want.to/have/it/from_web.js"),
            LinkJs.from_file("link/to/local_script.js"),
        ]

    doc = MyRap(str(tmpdir.join("that_file.html")))

    with doc.tag("p"):
        doc.text("The body content")

    assert doc.getvalue() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <link type='text/css' href='custom/css/dir/that_new_style.css' rel='stylesheet' />
    <link type='text/css' href='custom/css/dir/from_web.css' rel='stylesheet' />
    <link type='text/css' href='custom/css/dir/local_style.css' rel='stylesheet' />
    <script src='custom/js/dir/that_new_script.js'></script>
    <script src='custom/js/dir/from_web.js'></script>
    <script src='custom/js/dir/local_script.js'></script>
  </head>
  <body><p>The body content</p></body>
</html>"""


@pytest.mark.parametrize("Operation, placement", product([EmbedCss, LinkCss], [BODY_BEGIN, BODY_END]))
def test_cannot_put_css_in_body(Operation, placement, mocked_save_file):
    with pytest.raises(TypeError) as e:
        class MyRap(Yawrap):
            resources = [
                Operation("head { background: #DAD; }", placement=placement, file_name="some.css"),
            ]
    assert ('Cannot place CSS out of head section (%s)' % placement) in str(e.value)


@pytest.mark.parametrize("placement", [BODY_BEGIN, BODY_END])
def test_cannot_link_css_in_body(placement):
    with pytest.raises(TypeError) as e:
        class MyRap(Yawrap):
            resources = [ExternalCss("http://the.org/file.css", placement=placement)]
        MyRap("that_file.html")._render_page()
    assert "Cannot place CSS out of head section" in str(e.value)


@pytest.mark.parametrize("placement", [BODY_BEGIN, BODY_END])
def test_cannot_link_css_in_body2(placement):
    with pytest.raises(TypeError) as e:
        class MyRap(Yawrap):
            resources = [ExternalCss.from_url("http://the.org/file.css", placement=placement)]
        MyRap("that_file.html")._render_page()
    assert "Cannot place CSS out of head section" in str(e.value)


@pytest.mark.parametrize("placement", PLACEMENT_OPTIONS)
def test_have_to_provide_file_name(placement, mocked_save_file):
    with pytest.raises(ValueError) as e:
        class MyRap(Yawrap):
            resources = [LinkJs("script content", placement=placement)]
        MyRap("file.html")._render_page()
    assert "You need to provide filename in order to store the content for LinkJs operation." in str(e.value)


@pytest.mark.parametrize("Operation", [ExternalCss, ExternalJs])
def test_silly_definitions_2(Operation):
    with pytest.raises(TypeError) as e:
        Operation.from_file("anything")
    assert "Cannot reference remote/external file by local file content." in str(e.value)


def test_read_file(tmpdir):
    the_file = tmpdir.join("that.file")
    the_file.write("sentinel\n")
    result = _sourcer._Resource._read_file(str(the_file))
    assert result == "sentinel\n"


def test_inheriting_local_files_linkage(mocked_urlopen, mocked_read_file, mocked_save_file, tmpdir):

    class Root(NavedYawrap):
        resources = [
            LinkCss("body { background: #DAD; }", file_name="common_style.css"),
            LinkJs('console.log("all right!");', file_name="common_script.js"),
        ]

    root_file = tmpdir.join("that_file.html")
    sub_file = tmpdir.join("somewhere", "else", "page.html")

    root_doc = Root(str(root_file))

    with root_doc.tag("p"):
        root_doc.text("The root body content")

    sub_doc = root_doc.sub(str(sub_file), "sub_name")

    root_soup = BeautifulSoup(root_doc._render_page(), "html.parser")

    assert root_soup.html.head.script['src'] == "resources/common_script.js"
    assert root_soup.html.head.link['href'] == "resources/common_style.css"

    sub_soup = BeautifulSoup(sub_doc._render_page(), "html.parser")
    assert sub_soup.html.head.script['src'] == "../../resources/common_script.js"
    assert sub_soup.html.head.link['href'] == "../../resources/common_style.css"


def test_defining_css_as_a_dict(mocked_save_file):
    class Root(NavedYawrap):
        resources = [
            EmbedCss({"body": {"background": "#DAD"}}),
            LinkCss({"#that": {"color": "#DAD"}}, file_name="common_style.css"),
        ]
    root_doc = Root("one.html")
    root_doc.add(EmbedCss("div {padding: 0px;}"))

    sub_doc = root_doc.sub("two.html")
    sub_doc.add(EmbedCss("#id {margin: 10px 12px;}"))
    sub_doc.add(LinkCss("a {width: 90%;}", file_name="sub.css"))

    root_soup = BeautifulSoup(root_doc._render_page(), "html.parser")
    sub_soup = BeautifulSoup(sub_doc._render_page(), "html.parser")

    expected_root_styles = [
        "body { background: #DAD; }".split(),
        "div {padding: 0px;}".split()
    ]
    expected_sub_styles = [
        "body { background: #DAD; }".split(),
        "#id {margin: 10px 12px;}".split()
    ]

    root_styles = [style.text.split() for style in root_soup.html.head.find_all("style")]
    assert all([style in root_styles for style in expected_root_styles])

    sub_styles = [style.text.split() for style in sub_soup.html.head.find_all("style")]
    assert all([style in sub_styles for style in expected_sub_styles])

    root_links = [link["href"] for link in root_soup.html.head.find_all("link")]
    assert root_links == ['resources/common_style.css']

    sub_links = [link["href"] for link in sub_soup.html.head.find_all("link")]
    assert sub_links == ['resources/common_style.css', 'resources/sub.css']
