import os
import re

from .six import str_types


def make_place(target_file):
    dir_ = os.path.dirname(target_file) or os.getcwd()
    if not os.path.isdir(dir_):
        assert not os.path.isfile(dir_)
        os.makedirs(dir_)
    return target_file


def assert_keys_not_in(restricted_keys, args, kwargs):
    restricted_keys = restricted_keys if isinstance(restricted_keys, (list, tuple)) else [restricted_keys]
    for key in restricted_keys:
        defined_keys = list(kwargs.keys()) + [x[0] for x in args if isinstance(x, tuple)]
        if key in defined_keys:
            raise ValueError("Duplicated '{}' attribute.".format(key))


def form_css(structured_css, indent_level=1):
    if isinstance(structured_css, str_types):
        return structured_css

    assert isinstance(structured_css, dict), "Input CSS is supposed to " \
                                             "be string or dict, got %s" % type(structured_css).__name__
    base_indent = ' ' * 2
    indent = base_indent * indent_level

    template = "\n{ind}{selector} {{{definitions}}}"
    def_tpl = "{ind}{bind}{property}: {value};"

    def rules():
        for selector, definitions in sorted(structured_css.items()):
            defs = '\n'.join(def_tpl.format(ind=indent, bind=base_indent, property=prop, value=val)
                             for prop, val in sorted(definitions.items()))
            if defs:
                defs = "\n{}\n{ind}".format(defs, ind=indent)
            yield template.format(ind=indent, selector=selector, definitions=defs)

    return ''.join(rules())


DJANGO_URL_VALIDATION_PROG = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_url(text):
    return isinstance(text, str) and DJANGO_URL_VALIDATION_PROG.match(text) is not None
