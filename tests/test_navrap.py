#!/usr/bin/python
'''
Created on 24 Sep 2017

@author: kamichal
'''
from bs4 import BeautifulSoup
from contextlib import contextmanager
import os
import pytest

from yawrap import NavedYawrap, EmbedCss, Doc


def flatten(nav_entry):
    yield nav_entry.element
    for i in nav_entry.children:
        for j in flatten(i):
            yield j


class StyledNavrap(NavedYawrap):
    css = """
body {
    margin: 0;
    padding: 0px;
    background: #fdfafa;
    font-family: Verdana, sans-serif;
}
.nav_main_panel {
    margin : 0;
    padding: 0px 2px 0px 0px;
    list-style-type: none;
    width: 320px;
    background-color: #fdfafa;
    position: fixed;
    height: 100%;
    overflow: auto;
}
.nav_group_div {
    margin: 0px 0px 0px 10px;
    padding: 0px;
}
.nav_group_div.active {
    background: #fdf8fa;
    border: 1px solid #ddd;
    border-radius: 6px;
    -moz-box-shadow: 0 0 4px 1px #BBB;
    -webkit-box-shadow: 0 0 4px 1px #BBB;
}
.nav_page.with_bookmarks {
    border-radius: 6px;
    background: #eee;
}

.nav_page.with_bookmarks a.nav_bookmark_link:hover{
    background: #fafafa;
    color: #000;
}
a.nav_bookmark_link {
    margin: 0px 3px;
}
.nav_group_div a {
    padding: 5px 10px;
    display: block;
    color: #000;
    text-decoration: none;
}
.nav_group_div a.active {
    border-radius: 4px;
    background-color: #4CAF50;
    color: #000;
    -moz-box-shadow: 0 0 13px 0px #282 inset;
    -webkit-box-shadow: 0 0 13px 0px #282 inset;
}
.nav_group_div a:hover:not(.active) {
    border-radius: 4px;
    background-color: #777;
    color: white;
}
.main_content_body {
    margin: 0px 16px 0px 335px;
    padding:6px 16px;
}
"""


class W3StyledNavrap(NavedYawrap):
    css = """
body {
    margin: 0;
    font-family: Verdana, sans-serif;
}
.nav_main_panel {
    list-style-type: none;
    margin: 0;
    padding: 0;
    width: 25%;
    background-color: #f1f1f1;
    position: fixed;
    height: 100%;
    overflow: auto;
}
.nav_group_div a {
    display: block;
    color: #000;
    padding: 8px 16px;
    text-decoration: none;
}

.nav_group_div a.active {
    background-color: #4CAF50;
    color: white;
}
.nav_group_div.active {
    background-color: #fdf8fa;
    color: white;
}
.nav_page.with_bookmarks {
    background: #DDD;
}
.nav_group_div a:hover:not(.active) {
    background-color: #555;
    color: white;
}
.main_content_body {
    margin-left:25%;
    padding:1px 16px;
    height:1000px;
}
"""


plain_info = "Minimal version. No CSS has been used (besides what's comming from plugin)."
styled_info = 'Manually styled navigation, without referencing external CSS.'
w3_info = 'W3 styled page.'

NAV_TEST_PARAMS = [(NavedYawrap, plain_info, 'subs_plain'),
                   (StyledNavrap, styled_info, 'subs_StyledNavrap'),
                   (W3StyledNavrap, w3_info, 'subs_W3StyledNavrap')]


def draw_sample_svg(painter_doc, points="50,150 50,200 200,200 200,100"):
    painter_doc.stag('rect', x="25", y="25", width="200", height="200", klass='the_rect')
    painter_doc.stag('circle', cx="125", cy="125", r="75", fill="orange")
    painter_doc.stag('polyline', points=points, stroke="red", fill="none", stroke_width=4)
    painter_doc.stag('line', x1="50", y1="50", x2="200", y2="200", stroke="blue", stroke_width="4")


def test_simple_navrap(tmpdir):

    out_file_1 = str(tmpdir.join("nav01a.html"))
    out_file_2 = str(tmpdir.join("nonexistent/path/nav01b.html"))

    class MyPage(NavedYawrap):
        resources = [EmbedCss("""
        body {
            margin: 16;
            font-family: Verdana, sans-serif;
        }""")
                     ]

    home = MyPage(out_file_1, title="Title Force One")

    with home.tag('p'):
        home.text("I'm home")

    about = home.sub(out_file_2, 'Abouting')

    with about.tag('div'):
        about.text('Always do the abouting!')

    home.render_all_files()

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
            <a class='nav_page_link' href='nonexistent/path/nav01b.html'>Abouting</a>
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
        <div class='nav_page'><a class='nav_page_link' href='../../nav01a.html'>Title Force One</a></div>
        <div class='nav_group_div active'>
          <div class='nav_page with_bookmarks'><a class='active' href='nav01b.html'>Abouting</a></div>
        </div>
      </div>
    </nav>
    <main class='main_content_body'><div>Always do the abouting!</div></main>
  </body>
</html>"""


@contextmanager
def add_tooltip(target_doc, popup_width=280, type_='span', *args, **kwargs):

    target_doc.add(EmbedCss({
        ".tooltip": {
            "position": "relative",
            "display": "inline-block",
        },
        ".tooltip .tooltip_popup": {
            'padding': '16px',
            'background-color': "#121",
            'border-radius': '6px',
            'color': '#fff',
            "top": "100%",
            "left": "50%",
            "width": "{}px".format(popup_width),
            "margin-left": "-{}px".format(popup_width / 2),
            'visibility': 'hidden',
            'position': 'absolute',
            'z-index': '1'
        },
        ".tooltip:hover .tooltip_popup": {
            'visibility': 'visible'
        },
        ".tooltip .tooltip_popup::after": {
            "content": "' '",
            "position": "absolute",
            "bottom": "100%",
            "left": "50%",
            "margin-left": "-5px",
            "border-width": "5px",
            "border-style": "solid",
            "border-color": "transparent transparent black transparent"
        }
    }))

    popup_doc = Doc()

    with target_doc.tag(type_, klass="tooltip", *args, **kwargs):
        yield popup_doc
        with target_doc.tag('span', klass=".{}_popup".format("tooltip")[1:]):
            target_doc.asis(popup_doc.getvalue())


def other_styles_listing_plugin(host_doc, out_dir, current_test_out_dir):
    style = """\
    .main_container {
        background: #FFD;
        margin: 12px 26px;
        padding: 0px;
        -moz-box-shadow: 2px 2px 5px 2px #AAA;
        -webkit-box-shadow: 2px 2px 5px 2px #AAA;
        font-family: Verdana, sans-serif;
    }
    .main_container h4 {
        margin: 9px;
    }
    .container {
        padding: 2px 18px;
    }
    a.div_link {
        text-decoration: none;
    }
    .blue {
        background: #6699ff;
    }
    .leftbar {
        border-left: solid 7px #6699ff;
    }
    .info_card {
        color: #000;
        margin: 3px 10px;
        display: inline-block;
        padding: 4px 26px;
        -moz-box-shadow: 0 0 7px 0 #999 inset;
        -webkit-box-shadow: 0 0 7px 0 #999 inset;
    }
    .info_card:hover {
        background: #9CF
    }
    """

    plugin_info = """\
This div is placed here using kind of plugin. It's a stand-alone python function,
that can be called with Yawrap handle and any other arguments you desire. Of course you write it yourself.""", """\
It can add content, add CSS rules or insert a JS to that site. There is no need to define them
in a page (i.e. Yawrap class) that uses it. However of course those will appear in the final page - merged
with its native rules.""", """\
It is supposed to look almost the same way in each pages of different styles unless plugin's CSS selectors
collide with host page selectors.""", """\
Advantage of using such stuff is ability to joining CSS and HTML of a plugin in one place of source.
It's easy to maintain. It's reusable by separation from page class definition. It can be used totally dynamic.
"""

    host_doc.add(EmbedCss(style))
    with host_doc.tag('div', klass='main_container'):
        with host_doc.tag('div', klass='container blue'):
            with host_doc.tag('h4'):
                host_doc.text("Other versions")

        with host_doc.tag('div', klass='container leftbar'):
            for info in plugin_info:
                with host_doc.tag('p'):
                    host_doc.text(info)

            with host_doc.tag('h4'):
                host_doc.text("Check also other styles:")
            for other_class, info, other_dir in NAV_TEST_PARAMS:
                other_index = os.path.join(out_dir, other_dir, 'index.html')
                rel_link = os.path.relpath(other_index, current_test_out_dir)

                with host_doc.local_link(other_index, klass='div_link'):
                    with add_tooltip(host_doc, 340) as popup:
                        popup.text(rel_link)
                        with popup.tag('p'):
                            popup.text(info)
                        with host_doc.tag('div', klass="info_card"):
                            host_doc.text(other_class.__name__ + ' ')


def insert_lorem_ipsums(target_doc, lorem_ipsums):
    for bidx, lorem in enumerate(lorem_ipsums, 1):
        bookmark_name = 'chapter %s' % bidx
        with target_doc.bookmark(bookmark_name, type_='h3'):
            target_doc.text("That's chapter # %s" % bidx)
        with target_doc.tag('p'):
            target_doc.text(lorem)


@pytest.mark.parametrize('nav_class, style_name, root_dir_name', NAV_TEST_PARAMS)
def test_navigation(nav_class, style_name, root_dir_name, out_dir, lorem_ipsums):

    test_out_dir = os.path.join(out_dir, root_dir_name)
    index_file = os.path.join(test_out_dir, 'index.html')
    subs_dir = 'test_subs_subdir'

    files = [index_file]

    def make_content(j, text):
        rel_loc = os.path.relpath(j._target_file, out_dir)
        with j.tag('h2'):
            j.text(text)
        with j.tag('p'):
            j.text("And I'm enjoying the navigation with {}".format(style_name))
        with j.tag('p'):
            j.text("I'm located at {}.".format(rel_loc))

        with add_tooltip(j, 100) as popup:
            j.text("Hoverable")
            with popup.tag('div'):
                popup.text("I'm a popup")

    def create_sub(jarap_, new_file, text, title=''):
        files.append(new_file)
        new_jarap = jarap_.sub(new_file, title)
        make_content(new_jarap, text)
        return new_jarap

    parent = nav_class(index_file, 'Index')
    with parent.tag('h3'):
        parent.text("Index")
    with parent.tag('p'):
        parent.text("Hi, I'm a parent document in this structure. You can check how the navigation works.")

    other_styles_listing_plugin(parent, out_dir, test_out_dir)
    with parent.tag('p'):
        parent.text("that's nice")

    child_file0 = os.path.join(test_out_dir, 'child0.html')
    child0 = create_sub(parent, child_file0, "I'm a child 0. I have a nav-title, no children-pages",
                        'titled child 0')

    with child0.bookmark('the bookmark', type_='h3'):
        child0.text('thats the bookmark text')
    with child0.tag('p'):
        child0.text('A paragraph marked with a header with bookmark.')

    with child0.bookmark('some svg', type_='h3'):
        child0.text('Here comes some SVG')
    with child0.svg(width=250, height=250, svg_styles_as_str=".the_rect {fill: lime; stroke-width: 4; stroke: pink;}"):
        draw_sample_svg(child0)

    child_file1 = os.path.join(test_out_dir, 'child1.html')
    child1 = create_sub(parent, child_file1, "I'm a child 1, I have several bookmarks and some children.")
    insert_lorem_ipsums(child1, lorem_ipsums)

    child_file2 = os.path.join(test_out_dir, subs_dir, 'child2.html')
    child2 = create_sub(child1, child_file2, "I'm a child 2. No title")
    for i in range(3):
        f = os.path.join(test_out_dir, subs_dir, 'another_sub', '%s.html' % i)
        create_sub(child2, f, "I'm a child %s of child 2" % i, "CH%03d" % i)

    child_file3 = os.path.join(test_out_dir, subs_dir, 'child3.html')
    child3 = create_sub(parent, child_file3, "I'm a child 3.", "many bookmarks")

    for bix in range(1, 101):
        bookmark_name = 'bookmark %s' % bix
        with child3.bookmark(bookmark_name, type_='h3'):
            child3.text("That's chapter # %s" % bix)
        child3.text('contents of chapter %s' % bix)

    parent.render_all_files()
    assert all([os.path.isfile(file_) for file_ in files])

    assert child3._get_root() == parent

    flatten_structure = list(flatten(child2._get_nav_structure()))
    assert all([isinstance(j, nav_class) for j in flatten_structure])
    assert len(flatten_structure) == len(files)

    for file_ in files:
        with open(file_, 'rt') as ff:
            content = ff.read()

        soup = BeautifulSoup(content, "html.parser")
        assert soup.html
        assert soup.html.head
        assert soup.html.body

        assert len(soup.html.head.style) == 1

        nav_def = soup.html.body.find_all('nav', class_="nav_main_panel")
        assert len(nav_def) == 1
        links = nav_def[0].find_all('a')
        assert len(links) >= len(files)
        basenames = list(map(os.path.basename, files))
        assert all(os.path.basename(l['href']) and os.path.basename(l['href']).split('#')[0] in basenames
                   for l in links)
