.. _multi-page:

Multiple-page structure with navigation
=======================================

It's easy to navigate between several files in different paths, using ``sub()`` method of NavedYawrap instance.
Each call of ``sub()`` returns instance of given NavedYawrap class, with same styles and scripts as the parent one.
Each page will be rendered with navigation section, with relative paths. See the hrefs in the example below.

The first document (``home`` in this example) will be the the `root` of the document structure. 

.. testcode::

    def is_html_equal(html_file, expected_html):
        from bs4 import BeautifulSoup
        got = BeautifulSoup(open(html_file, 'r').read(), "lxml")
        exp = BeautifulSoup(expected_html, "lxml")
        return got == exp

    from yawrap import NavedYawrap

    class MyPage(NavedYawrap):
        css = """
            body {
                margin: 16;
                font-family: Verdana, sans-serif;
            }"""

    out_file_1 = "/tmp/nav01a.html"
    home = MyPage(out_file_1, title="Title Force One")

    with home.tag('p'):
        home.text("I'm home")

    out_file_2 = "/tmp/some/deep/nonexistent/path/nav01b.html"
    about = home.sub(out_file_2, 'Abouting')

    with about.tag('div'):
        about.text('Always do the abouting!')

    home.render_all_files()


    print(is_html_equal(out_file_1, """\
    <!doctype html>
    <html lang="en-US">
      <head>
        <meta charset="UTF-8" />
        <title>Title Force One</title>
        <style>
          body {
            font-family: Verdana, sans-serif;
            margin: 16;
          }</style>
      </head>
      <body>
        <nav class="nav_main_panel">
          <div class="nav_group_div active">
            <div class="nav_page with_bookmarks">
              <a href="nav01a.html" class="active">Title Force One</a>
            </div>
            <div class="nav_group_div">
              <div class="nav_page">
                <a href="some/deep/nonexistent/path/nav01b.html" class="nav_page_link">Abouting</a>
              </div>
            </div>
          </div>
        </nav>
        <main class="main_content_body">
          <p>I'm home</p>
        </main>
      </body>
    </html>"""))

    print(is_html_equal(out_file_2, """\
    <!doctype html>
    <html lang="en-US">
      <head>
        <meta charset="UTF-8" />
        <title>Abouting</title>
        <style>
          body {
            font-family: Verdana, sans-serif;
            margin: 16;
          }</style>
      </head>
      <body>
        <nav class="nav_main_panel">
          <div class="nav_group_div">
            <div class="nav_page">
              <a href="../../../../nav01a.html" class="nav_page_link">Title Force One</a>
            </div>
            <div class="nav_group_div active">
              <div class="nav_page with_bookmarks">
                <a href="nav01b.html" class="active">Abouting</a>
              </div>
            </div>
          </div>
        </nav>
        <main class="main_content_body">
          <div>Always do the abouting!</div>
        </main>
      </body>
    </html>"""))

gives:

.. testoutput::

    True
    True
