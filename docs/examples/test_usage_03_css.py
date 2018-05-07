
from yawrap import Yawrap


class PlainPage(Yawrap):
    resources = []


doc = PlainPage("/tmp/test.html")
doc.render()

# end of section A


from yawrap import ExternalCss, ExternalJs


class PageWithExternalCss(Yawrap):
    resources = [
        ExternalCss.from_url("https://www.w3schools.com/w3css/4/w3.css"),
        ExternalJs.from_url("https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
    ]

# end of section B


from yawrap import LinkCss, LinkJs


class LinkedCssPage(Yawrap):
    resources = [
        LinkCss.from_url("https://www.w3schools.com/w3css/4/w3.css"),
        LinkJs.from_url("https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
    ]

# end of section C


class LocalSources(Yawrap):
    resources = [
        LinkCss.from_file("path/to/source_of/w3.css"),
        LinkJs.from_file("path/to/source_of/jquery.min.js"),
    ]

# end of section D


class LinkCssInMyStyle(LinkCss):
    resource_subdir = "the_super_directory"
    # for nested structure, do:
#   # resource_subdir = os.path.join("the", "super", "directory")


class LinkJsInMyStyle(LinkJs):
    resource_subdir = ""
    # empty string will same dir, as parent html


class MyStyleOfLinking(Yawrap):
    resources = [
        LinkCssInMyStyle.from_url("https://www.w3schools.com/w3css/4/w3.css"),
        LinkJsInMyStyle.from_url("https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
    ]

# end of section E


def test_that(mocker):
    from yawrap import _sourcer
    from exampling_tools import get_output_file_path  # need it to make this docs building

    _sourcer.RAISE_ON_DOWNLOAD_FAIL = False
    mocker.patch.object(_sourcer._Resource, "_download", return_value="")

    plain_file_path = get_output_file_path("test_usage_03a.html")
    PlainPage(plain_file_path).render()
    PageWithExternalCss(get_output_file_path("test_usage_03b.html")).render()
    LinkedCssPage(get_output_file_path("test_usage_03c.html")).render()
    MyStyleOfLinking(get_output_file_path("test_usage_03e.html")).render()
    with open(plain_file_path, "rt") as f:
        assert f.read() == """\
<!doctype html><html lang='en-US'>
  <head><meta charset='UTF-8' /></head>
  <body></body>
</html>"""
