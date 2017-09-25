#!/usr/bin/python
'''
Created on 24 Sep 2017

@author: kamichal
'''
from bs4 import BeautifulSoup
import os
import pytest

from yarap.yawrap import NavedYawrap
from random import choice


def flatten(nav_entry):
    yield nav_entry.element
    for i in nav_entry.children:
        for j in flatten(i):
            yield j


LOREM_IPSUMS = ["""\
Ferri affert expetenda ei duo, vel cu legimus splendide. Oblique dignissim elaboraret vix cu,
eos errem graeco ponderum ut, id quidam semper melius mei. Tantas munere ornatus an vel.
Sit simul tempor tibique cu.
His te erat etiam phaedrum, qui graece dicunt sensibus te, qui ad salutandi periculis.
At quaeque sensibus sed, persius dolorum usu ea, apeirian urbanitas ius te. Eos doctus
virtute ne, id qui choro possit graeco. Ei duo dolor expetendis scribentur, ut decore
labitur consetetur pri. Summo ludus referrentur cu sit, elitr periculis voluptaria vix ei.
Vix soluta facilis repudiandae ne. Ius graecis fabellas ad, duo percipitur instructior an.""", """\
Placerat gloriatur mei ea. Mel id alienum pertinacia, ne per viris choro mnesarchum, ad inani
consul his. Error audiam explicari quo an, mea corpora invenire ex. Id luptatum dissentiet eam.
Utroque adolescens ut pro, te vel labitur iudicabit. Dicant putent tractatos duo in.""", """\
Atqui animal utamur ea nam, nam id quodsi ornatus probatus. Lorem nostrud in mei.
Ne mei etiam ignota. Ut dico veritus pri, facilisis corrumpit vis ei.
Est utroque consulatu ne, deleniti perfecto ocurreret id duo. Tibique accusam in mea.
Ex pro delenit persequeris, qui magna maluisset definitionem id.
Has postulant omittantur ad.""", """\
Mundi principes eum ea, velit sapientem theophrastus vel at. Malis facer ad vel, cetero delicata
id usu. Alterum liberavisse ea vis. Mea ignota possim ex, vim sale iusto in. Ferri justo consul
eum ut, usu corpora ocurreret et, mea ut malis dolore viderer."""]


class StyledNavrap(NavedYawrap):
    css = """
body {
    margin: 0;
    padding: 8px;
    background: #fdfafa;
}
.nav_main_panel {
    margin : 0;
    padding: 16px 2px 0px 0px;
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
    padding: 8px 16px;
    display: block;
    color: #000;
    text-decoration: none;
}
.nav_group_div a.active {
    border-radius: 4px;
    background-color: #4CAF50;
    color: #000;
}
.nav_group_div a:hover:not(.active) {
    border-radius: 4px;
    background-color: #777;
    color: white;
}
.main_content_body {
    margin: 20px 16px 20px 335px;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding:1px 16px;

}
"""


class W3StyledNavrap(NavedYawrap):
    css = """
body {
    margin: 0;
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


NAV_TEST_PARAMS = [(NavedYawrap, 'minimal', 'subs_plain'),
                   (StyledNavrap, 'styled', 'subs_StyledNavrap'),
                   (W3StyledNavrap, 'W3 styled', 'subs_W3StyledNavrap')]


@pytest.mark.parametrize('nav_class, style_name, root_dir_name', NAV_TEST_PARAMS)
def test_navigation(nav_class, style_name, root_dir_name, out_dir):

    test_out_dir = os.path.join(out_dir, root_dir_name)

    index_file = os.path.join(test_out_dir, 'index.html')

    files = [index_file]

    def make_content(j, text):
        rel_loc = os.path.relpath(j._target_file, out_dir)
        with j.tag('h2'):
            j.text(text)
        with j.tag('p'):
            j.text("And I'm enjoying the navigation with {} css.".format(style_name))
        with j.tag('p'):
            j.text("I'm located at {}.".format(rel_loc))
        with j.tag('p'):
            j.text("Would you check also other styles? Check:")
            with j.tag('ul'):
                for other_class, other_name, other_dir in NAV_TEST_PARAMS:
                    other_index = os.path.join(out_dir, other_dir, 'index.html')
                    rel_link = os.path.relpath(other_index, test_out_dir)
                    with j.tag('li'):
                        with j.tag('p'):
                            j.text(other_name)
                            j.stag('br')
                            j.text(other_class.__name__ + ' ')
                            with j.local_link(other_index):
                                j.text(rel_link)

        for bidx in xrange(len(LOREM_IPSUMS)):
            bookmark_name = 'chapter %s' % (bidx + 1)
            with j.bookmark(bookmark_name, type_='h3'):
                j.text("That's chapter # %s" % (bidx + 1))
            with j.tag('p'):
                lorem_index = choice(range(len(LOREM_IPSUMS)))
                j.text(LOREM_IPSUMS[lorem_index])

    def create_sub(jarap_, new_file, text, title=''):
        files.append(new_file)
        new_jarap = jarap_.sub(new_file, title)
        make_content(new_jarap, text)
        return new_jarap

    parent = nav_class(index_file, 'Index')
    make_content(parent, "I'm a parent")
    with parent.tag('p'):
        parent.text("that's nice")

    child_file0 = os.path.join(test_out_dir, 'test_subs_child0.html')
    child0 = create_sub(parent, child_file0, "I'm a child 0. I have a nav-title",
                        'titled child 0')

    with child0.bookmark('the bookmark', type_='h3'):
        child0.text('thats the bookmark text')
    with child0.tag('p'):
        child0.text('A paragraph marked with a header with bookmark.')

    child_file1 = os.path.join(test_out_dir, 'test_subs_child1.html')
    child1 = create_sub(parent, child_file1, "I'm a child 1")

    child_file2 = os.path.join(test_out_dir, 'test_subs_subdir', 'test_subs_child2.html')
    child2 = create_sub(child1, child_file2, "I'm a child 2. No title")
    for i in xrange(3):
        f = os.path.join(test_out_dir, 'test_subs_subdir', 'another_sub', '%s.html' % i)
        create_sub(child2, f, "I'm a child %s of child 2" % i)

    child_file3 = os.path.join(test_out_dir, 'test_subs_subdir', 'test_subs_child3.html')
    child3 = create_sub(parent, child_file3, "I'm a child 3. I don't have a title.")

    parent.render_all_files()
    assert all(os.path.isfile(f) for f in files)

    assert child3._get_root() == parent

    flatten_structure = list(flatten(child2._get_nav_structure()))
    assert all(isinstance(j, nav_class) for j in flatten_structure)
    assert len(flatten_structure) == len(files)

    for file_ in files:
        with open(file_, 'rt') as ff:
            content = ff.read()

        soup = BeautifulSoup(content)
        assert soup.html
        assert soup.html.head
        assert soup.html.body
        if nav_class.css:
            assert len(soup.html.head.style) == 1

        nav_def = soup.html.body.find_all('nav', class_="nav_main_panel")
        assert len(nav_def) == 1
        links = nav_def[0].find_all('a')
        assert len(links) >= len(files)
        basenames = map(os.path.basename, files)
        assert all(os.path.basename(l['href']) and os.path.basename(l['href']).split('#')[0] in basenames
                   for l in links)
