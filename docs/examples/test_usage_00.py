from yawrap import Yawrap


def hello_yawrap():
    doc = Yawrap("not/revelant/path.html", "The super title")

    with doc.tag("div", id="content", klass="main"):
        with doc.tag('h2'):
            doc.text('Hello yawrap!')

        with doc.tag('p'):
            doc.text('Could it be simpler?')

    doc.comment("that's it")
    result = doc.getvalue()

    assert result == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>The super title</title>
  </head>
  <body>
    <div class='main'>
      <h2>Hello yawrap!</h2>
      <p>Could it be simpler?</p>
    </div>
    <!-- that's it -->
  </body>
</html>"""
