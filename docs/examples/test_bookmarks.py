import os

from exampling_tools import get_output_file_path
from yawrap import NavedYawrap, EmbedCss

OUT_FILE_PATH_1 = get_output_file_path("bookmarked.html")
OUT_FILE_PATH_2 = get_output_file_path(os.path.join("bookmarked_sub.html"))


def test_naved_yawrap():

    class MyPage(NavedYawrap):
        resources = [
            EmbedCss("""\
        body {
            margin: 16;
            font-family: Verdana, sans-serif;
        }""")
        ]

    home = MyPage(OUT_FILE_PATH_1)

    with home.tag('p'):
        home.text("I'm home")

    with home.bookmark("bookmark_1", "A Bookmark (#1)"):
        with home.tag('p'):
            home.text("A paragraph")

    with home.bookmark("bookmark_2", "Another Bookmark (#2)", type_='p'):
        home.text("Paragraph with bookmark")

    sub = home.sub(OUT_FILE_PATH_2, "Second page")

    with sub.tag('h2'):
        sub.text("Header in sub page")

    with sub.bookmark("bookmark_3", "Another Bookmark (#3)", style="color: #323436"):
        sub.text("Div with bookmark 3")

    with sub.tag('div'):
        sub.text('Always do the abouting!')

    home.render_all_files()

    with open(OUT_FILE_PATH_1, "rt") as f:
        assert f.read() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
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
        <div class='nav_page with_bookmarks'>
          <a class='active' href='bookmarked.html'>bookmarked.html</a>
          <a class='nav_bookmark_link' href='bookmarked.html#bookmark_1'>A Bookmark (#1)</a>
          <a class='nav_bookmark_link' href='bookmarked.html#bookmark_2'>Another Bookmark (#2)</a>
        </div>
        <div class='nav_group_div'>
          <div class='nav_page'><a class='nav_page_link' href='bookmarked_sub.html'>Second page</a></div>
        </div>
      </div>
    </nav>
    <main class='main_content_body'>
      <p>I'm home</p>
      <div id='bookmark_1'><p>A paragraph</p></div>
      <p id='bookmark_2'>Paragraph with bookmark</p>
    </main>
  </body>
</html>"""

    with open(OUT_FILE_PATH_2, "rt") as f:
        assert f.read() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>Second page</title>
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
        <div class='nav_page'><a class='nav_page_link' href='bookmarked.html'>bookmarked.html</a></div>
        <div class='nav_group_div active'>
          <div class='nav_page with_bookmarks'>
            <a class='active' href='bookmarked_sub.html'>Second page</a>
            <a class='nav_bookmark_link' href='bookmarked_sub.html#bookmark_3'>Another Bookmark (#3)</a>
          </div>
        </div>
      </div>
    </nav>
    <main class='main_content_body'>
      <h2>Header in sub page</h2>
      <div id='bookmark_3' style='color: #323436'>Div with bookmark 3</div>
      <div>Always do the abouting!</div>
    </main>
  </body>
</html>"""
