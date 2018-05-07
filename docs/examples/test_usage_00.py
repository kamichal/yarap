from yawrap import Yawrap


def hello_yawrap():
    jawrap = Yawrap("not/revelant/path.html", "The title")

    with jawrap.tag("div", klass="main_content"):
        with jawrap.tag('h2'):
            jawrap.text('Hello yawrap!')

        with jawrap.tag('p'):
            jawrap.text('Could it be simpler?')
    jawrap.comment("that's it")
    return jawrap.getvalue()


def test_that():
    assert hello_yawrap() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>The title</title>
  </head>
  <body>
    <div class='main_content'>
      <h2>Hello yawrap!</h2>
      <p>Could it be simpler?</p>
    </div>
    <!-- that's it -->
  </body>
</html>"""
