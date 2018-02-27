from yawrap import Yawrap


def hello_yawrap(out_file_path):

    jawrap = Yawrap(out_file_path, "The title")

    with jawrap.tag('h2'):                       # add a header
        jawrap.text('Hello yawrap!')

    with jawrap.tag('p'):                        # add a paragraph
        jawrap.text('Could it be simpler?')      # and its content

    jawrap.render()                              # that creates html file (under out_file_path)


def test_that():
    from exampling_tools import get_output_file_path
    from tests._test_utils import assert_html_equal

    output_file_path = get_output_file_path("test_usage_00.html")

    hello_yawrap(output_file_path)
    assert_html_equal(output_file_path, """
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
    <title>The title</title>
  </head>
  <body>
    <h2>Hello yawrap!</h2>
    <p>Could it be simpler?</p>
  </body>
</html>""")
