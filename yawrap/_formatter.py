import re
from collections import namedtuple

_INDENT_PROG = re.compile("\s*\>\n\s*\<")
_END_TAG_PROG = re.compile("(\</\s*\w+\s*\>)")


@staticmethod
def _no_indent(raw_html_string):
    """ no indentation,
        the fastest store (no html postprocessing),
        slow read and JS DOM traverse,
        smallest file but unreadable for a human """
    if "\n" in raw_html_string:
        return _INDENT_PROG.sub("><", raw_html_string)
    return raw_html_string


@staticmethod
def _limited_line_width(raw_html_string):
    """ no indentation,
        ugly but fast store (html render),
        fast read and JS DOM traverse
        acceptable file size
    """
    max_line_width = 240

    def chop():
        cache, len_ = [], 0
        for part in raw_html_string.split(">"):
            cache.append(part)
            len_ += 1 + len(part)
            if len_ > max_line_width:
                yield ">".join(cache)
                cache, len_ = [], 0
        if cache:
            yield ">".join(cache)

    return ">\n".join(chop())


@staticmethod
def _new_line_each_end(raw_html_string):
    """ no indentation, new line at each ending tag
        fast store (html render) fast read and JS DOM traverse
        larger file size
    """
    return _END_TAG_PROG.sub(r"\1\n", raw_html_string)


@staticmethod
def _yattag_indent(raw_html_string):
    """ the prettiest html, but slow store (because of html tokenization),
        largest file size, fast read and JS DOM traverse
    """
    from yattag import indent
    return indent(raw_html_string)


# It's assumed they are sorted in order of performance
_HtmlFormatterOption = namedtuple("_HtmlFormatterOption", [
    "no_indent",
    "limited_line_width",
    "new_line_each_end",
    "yattag_indent",
])

HtmlFormatter = _HtmlFormatterOption(
    no_indent=_no_indent,
    limited_line_width=_limited_line_width,
    new_line_each_end=_new_line_each_end,
    yattag_indent=_yattag_indent,
)
