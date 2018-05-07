from yawrap import Ya4, Ya5


def test_clearap_v5():
    y = Ya5()
    with y.html():
        with y.body(style="color: #5f5;"):
            with y.div():
                with y.p(klass='ok'):
                    y.text("that's all")
                    y.br()
            y.img(href='12')

    assert y.getvalue() == """\
<html>
  <body style='color: #5f5;'>
    <div>
      <p class='ok'>
        that's all
        <br />
      </p>
    </div>
    <img href='12' />
  </body>
</html>"""


def test_clearap_v4():
    y = Ya4()
    with y.html():
        with y.body(style="color: #5f5;"):
            with y.div():
                with y.p(klass='ok'):
                    y.text("that's all")
                    y.br()
            y.img(href='12')

    assert y.getvalue() == """\
<html>
  <body style='color: #5f5;'>
    <div>
      <p class='ok'>
        that's all
        <br />
      </p>
    </div>
    <img href='12' />
  </body>
</html>"""
