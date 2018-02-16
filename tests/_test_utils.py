from bs4 import BeautifulSoup, element
import os
import re


MIN_PROG = re.compile("\s*\>\n*\s*\<")


def minify(html_string):
    return MIN_PROG.sub("><", html_string)


def html_from_file_or_string(file_or_string):
    if ">" not in file_or_string:
        assert os.path.isfile(file_or_string)
        with open(file_or_string, "rt") as ff:
            return ff.read()
    else:
        return file_or_string


def get_soup(html_file_or_string):
    return BeautifulSoup(html_from_file_or_string(html_file_or_string), "lxml")


def assert_html_equal(result_html_string, reference_html_string):

    result = walk_html(get_soup(result_html_string))
    reference = walk_html(get_soup(reference_html_string))
    assert result == reference
    return True


def walk_html(html_soup):
    if isinstance(html_soup, element.Tag):
        children = [walk_html(elm) for elm in getattr(html_soup, "children", [])]
        children = [c for c in children if c] or getattr(html_soup, "contents", "NO CONTENTS")
        attributes = getattr(html_soup, "attrs", None)
        return html_soup.name, attributes, children
    else:
        return html_soup.strip()
