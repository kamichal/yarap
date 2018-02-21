
import pytest

from yawrap import Yawrap, ExtenalJs, ExtenalCss, EmbedCss, LinkJs, BODY_BEGIN, BODY_END
from yawrap import _sourcer
from yawrap._sourcer import EmbedJs, os, LinkCss, PLACEMENT_OPTIONS, _Gainer
from _test_utils import assert_html_equal
from itertools import product


@pytest.fixture
def mocked_urlopen(mocker):

    class MockedUrlopen(object):
        def __init__(self, url, *_, **__):
            self.url = url

        def read(self, *_):
            return "Dummy response to {}".format(self.url)

        def close(self, *_):
            pass

    mocker.patch.object(_sourcer, "urlopen", side_effect=lambda *p: MockedUrlopen(*p))


@pytest.fixture
def mocked_read_file(mocker):
    def read_file_stub(file_path):
        return "That's a dummy content of %s file." % file_path

    mocker.patch.object(os.path, "isfile", return_value=True)
    mocker.patch.object(os.path, "isdir", return_value=True)
    mocker.patch.object(_sourcer._Gainer, "_read_file", side_effect=read_file_stub)


@pytest.fixture
def mocked_save_file(mocker):
    m = mocker.patch.object(_sourcer._Gainer, "_save_as_file")
    return m


def test_linking_external_resources_in_head():

    class MyRap(Yawrap):
        resources = [
            ExtenalCss("https://www.css.com/css.css"),
            ExtenalJs("https://www.js.com/js.js"),
        ]

    doc = MyRap("that_file.html")
    with doc.tag("p"):
        doc.text("The body content")
    assert_html_equal(doc._render_page(), """<!doctype html>
        <html lang="en-US">
          <head>
            <meta charset="UTF-8" />
            <link href="https://www.css.com/css.css" type="text/css" rel="stylesheet" />
            <script src="https://www.js.com/js.js"></script>
          </head>
          <body>
            <p>The body content</p>
          </body>
        </html>""")


def test_embedding_in_head(mocked_urlopen, mocked_read_file, mocked_save_file, tmpdir):

    class MyRap(Yawrap):
        resources = [
            EmbedCss.from_str("head { background: #DAD; }"),
            EmbedJs.from_str('console.log("alles klar in the head")'),

            EmbedCss.from_url("http://www.css.in/da.house.css"),
            EmbedJs.from_url('http://www.js.in/the.head.js'),

            EmbedCss.from_file("/path/to/style_to_embed.css"),
            EmbedJs.from_file("/path/to/script_to_embed.js"),
        ]

    doc = MyRap(str(tmpdir.join("that_file.html")))
    with doc.tag("p"):
        doc.text("The body content")

    assert_html_equal(doc._render_page(), """<!doctype html>
        <html lang="en-US">
          <head>
            <meta charset="UTF-8" />
            <style>head { background: #DAD; }</style>
            <script type="text/javascript">console.log("alles klar in the head")</script>
            <style>Dummy response to http://www.css.in/da.house.css</style>
            <script type="text/javascript">Dummy response to http://www.js.in/the.head.js</script>
            <style>That's a dummy content of /path/to/style_to_embed.css file.</style>
            <script type="text/javascript">That's a dummy content of /path/to/script_to_embed.js file.</script>
          </head>
          <body>
            <p>The body content</p>
          </body>
        </html>""")


def test_linking_local_files_in_head(mocked_urlopen, mocked_read_file, mocked_save_file, tmpdir):

    class MyRap(Yawrap):
        resources = [
            LinkCss.from_str("Store that style to the file.css", file_name="that_new_style.css"),
            LinkJs.from_str("Store that script to the file.js", file_name="that_new_script.js"),

            LinkCss.from_url("https://want.to/have/it/in/my/head.css"),
            LinkJs.from_url("https://want.to/have/it/in/my/head.js"),

            LinkCss.from_file("/link/to/local_style.css"),
            LinkJs.from_file("link/to/local_script.js"),
        ]

    doc = MyRap(str(tmpdir.join("that_file.html")))

    with doc.tag("p"):
        doc.text("The body content")

    assert_html_equal(doc._render_page(), """<!doctype html>
        <html lang="en-US">
          <head>
            <meta charset="UTF-8" />
            <link href="resources/that_new_style.css" type="text/css" rel="stylesheet" />
            <script src="resources/that_new_script.js"></script>
            <link href="resources/head.css" type="text/css" rel="stylesheet" />
            <script src="resources/head.js"></script>
            <link href="resources/local_style.css" type="text/css" rel="stylesheet" />
            <script src="resources/local_script.js"></script>
          </head>
          <body>
            <p>The body content</p>
          </body>
        </html>""")


def test_linking_local_files_in_head_custom_loc(mocked_urlopen, mocked_read_file, mocked_save_file, tmpdir):

    LinkCss.resource_subdir = "custom/css/dir"
    LinkJs.resource_subdir = "custom/js/dir"

    class MyRap(Yawrap):

        resources = [
            LinkCss.from_str("Store that style to the file.css", file_name="that_new_style.css"),
            LinkCss.from_url("https://want.to/have/it/from_web.css"),
            LinkCss.from_file("/link/to/local_style.css"),

            LinkJs.from_str("Store that script to the file.js", file_name="that_new_script.js"),
            LinkJs.from_url("https://want.to/have/it/from_web.js"),
            LinkJs.from_file("link/to/local_script.js"),
        ]

    doc = MyRap(str(tmpdir.join("that_file.html")))

    with doc.tag("p"):
        doc.text("The body content")

    assert_html_equal(doc._render_page(), """<!doctype html>
        <html lang="en-US">
          <head>
            <meta charset="UTF-8" />
            <link href="custom/css/dir/that_new_style.css" type="text/css" rel="stylesheet" />
            <link href="custom/css/dir/from_web.css" type="text/css" rel="stylesheet" />
            <link href="custom/css/dir/local_style.css" type="text/css" rel="stylesheet" />

            <script src="custom/js/dir/that_new_script.js"></script>
            <script src="custom/js/dir/from_web.js"></script>
            <script src="custom/js/dir/local_script.js"></script>
          </head>
          <body>
            <p>The body content</p>
          </body>
        </html>""")


@pytest.mark.parametrize("Operation, placement", product([EmbedCss, LinkCss], [BODY_BEGIN, BODY_END]))
def test_cannot_put_css_in_body(Operation, placement):
    with pytest.raises(TypeError) as e:
        class MyRap(Yawrap):
            resources = [
                Operation.from_str("head { background: #DAD; }", placement=placement, file_name="some.css"),
            ]
    assert ('Cannot place CSS out of head section (%s)' % placement) in str(e.value)


@pytest.mark.parametrize("placement", [BODY_BEGIN, BODY_END])
def test_cannot_link_css_in_body(placement):
    with pytest.raises(AssertionError) as e:
        class MyRap(Yawrap):
            resources = [ExtenalCss("http://the.org/file.css", placement=placement)]
        MyRap("that_file.html")._render_page()
    assert "CSS can be placed only in head section" in str(e.value)


@pytest.mark.parametrize("placement", [BODY_BEGIN, BODY_END])
def test_cannot_link_css_in_body2(placement):
    with pytest.raises(AssertionError) as e:
        class MyRap(Yawrap):
            resources = [ExtenalCss.from_url("http://the.org/file.css", placement=placement)]
        MyRap("that_file.html")._render_page()
    assert "CSS can be placed only in head section" in str(e.value)


@pytest.mark.parametrize("placement", PLACEMENT_OPTIONS)
def test_have_to_provide_file_name(placement):
    with pytest.raises(ValueError) as e:
        class MyRap(Yawrap):
            resources = [LinkJs.from_str("script content", placement=placement)]
        MyRap("file.html")._render_page()
    assert "You need to provide filename in order to store the content for LinkJs operation." in str(e.value)


@pytest.mark.parametrize("Operation", [ExtenalCss, ExtenalJs])
def test_silly_definitions(Operation):
    with pytest.raises(TypeError) as e:
        Operation.from_str("anything")
    assert "Cannot reference remote/external file by string content." in str(e.value)


@pytest.mark.parametrize("Operation", [ExtenalCss, ExtenalJs])
def test_silly_definitions_2(Operation):
    with pytest.raises(TypeError) as e:
        Operation.from_file("anything")
    assert "Cannot reference remote/external file by local file content." in str(e.value)


def test_sourcing_to_body_begin(mocked_urlopen, tmpdir):

    class MyRap(Yawrap):
        resources = [
            ExtenalCss("https://www.css.com/w3.css"),
            ExtenalJs("https://jquery.com/jquery.head.min.js"),

            EmbedCss.from_str("head { background: #DAD; }"),
            EmbedJs.from_str('console.log("alles klar in the head")'),
            EmbedJs.from_str('console.log("alles klar the body")', BODY_BEGIN),
            EmbedJs.from_str('console.log("body ends clearly as well")', BODY_END),

            EmbedCss.from_url("http://www.css.in/da.house.css"),
            EmbedJs.from_url('http://www.js.in/the.head.js'),
            EmbedJs.from_url('http://body.pl/starts.js', BODY_BEGIN),
            EmbedJs.from_url('https://www.see.you/body.js', BODY_END),

            LinkJs.from_url("https://invalid.address.com/want/to/have/it/in/head.js"),
            LinkJs.from_url("https://invalid.address.com/want/to/have/it/at_body_beggining.js", BODY_BEGIN),
            LinkJs.from_url("https://invalid.address.com/want/to/have/it/at_body_end.js", BODY_END),
        ]

    doc = MyRap(str(tmpdir.join("that_file.html")))
    with doc.tag("p"):
        doc.text("The body content")

    print(doc._render_page())


def test_read_file(tmpdir):
    the_file = tmpdir.join("that.file")
    the_file.write("sentinel\n")
    result = _Gainer._read_file(str(the_file))
    assert result == "sentinel\n"
