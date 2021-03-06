import os


# doc_start_here
def test_naved_yawrap():

    from exampling_tools import get_output_file_path
    from yawrap import NavedYawrap, EmbedCss

    class MyPage(NavedYawrap):
        resources = [EmbedCss("""\
        body {
            margin: 16;
            font-family: Verdana, sans-serif;
        }""")
                     ]

    out_file_1 = get_output_file_path("nav01a.html")
    home = MyPage(out_file_1, title="Title Force One")

    # fill content of root document
    with home.tag('p'):
        home.text("I'm home")

    # create a sub-document
    out_file_2 = get_output_file_path(os.path.join("some", "deep", "nonexistent", "path", "nav01b.html"))
    about = home.sub(out_file_2, 'Abouting')

    with about.tag('div'):
        about.text('Always do the abouting!')

    home.render_all_files()

    # at this point files are generated

    # doc end_here

    with open(out_file_1, "rt") as f:
        assert f.read() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>Title Force One</title>
    <style>
        body {
            margin: 16;
            font-family: Verdana, sans-serif;
        }
    </style>
  </head>
  <body>
    <nav class='nav_main_panel'>
      <div class='nav_group_div active'>
        <div class='nav_page with_bookmarks'><a class='active' href='nav01a.html'>Title Force One</a></div>
        <div class='nav_group_div'>
          <div class='nav_page'>
            <a class='nav_page_link' href='some/deep/nonexistent/path/nav01b.html'>Abouting</a>
          </div>
        </div>
      </div>
    </nav>
    <main class='main_content_body'><p>I'm home</p></main>
  </body>
</html>"""

    with open(out_file_2, "rt") as f:
        assert f.read() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>Abouting</title>
    <style>
        body {
            margin: 16;
            font-family: Verdana, sans-serif;
        }
    </style>
  </head>
  <body>
    <nav class='nav_main_panel'>
      <div class='nav_group_div'>
        <div class='nav_page'>
          <a class='nav_page_link' href='../../../../nav01a.html'>Title Force One</a>
        </div>
        <div class='nav_group_div active'>
          <div class='nav_page with_bookmarks'><a class='active' href='nav01b.html'>Abouting</a></div>
        </div>
      </div>
    </nav>
    <main class='main_content_body'><div>Always do the abouting!</div></main>
  </body>
</html>"""
