from contextlib import contextmanager

from yawrap.six import str_types


ATTRIBUTE_SUBSTITUTES = {
    'klass': 'class',
    'Class': 'class',
    'class_': 'class',
    'fill_opacity': 'fill-opacity',
    'stroke_width': 'stroke-width',
    'stroke_dasharray': ' stroke-dasharray',
    "stroke_opacity": "stroke-opacity",
    "stroke_dashoffset": "stroke-dashoffset",
    "stroke_linejoin": "stroke-linejoin",
    "stroke_miterlimit": "stroke-miterlimit",
}


class IndentableLine(object):
    __slots__ = ("text", "indent_level")
    single_indent = "  "

    def __init__(self, text):
        self.text = text
        self.indent_level = 0

    def increase_indent(self):
        self.indent_level += 1

    def __str__(self):
        return self.single_indent * self.indent_level + self.text

    def __len__(self):
        return len(str(self))


class NonindentableLine(IndentableLine):
    single_indent = ""


class Tag(object):
    __slots__ = ("tag_name", "attributes", "children")
    max_line_width = 20
    attribute_precedence_rank = {
        "class": 0,
        "id": 1,
        "name": 2,
        "src": 3,
        "for": 4,
        "type": 5,
        "href": 6,
        "value": 7,
        "default rank for other attributes": 10,
        "title": 101,
        "alt": 102,
        "style": 103,
    }

    def __init__(self, tag_name, *args, **kwargs):
        self.tag_name = tag_name
        self.attributes = self._process_attributes(args, kwargs)
        self.children = []

    def __str__(self):
        return "\n".join(str(l) for l in self._build_lines())

    @classmethod
    def _process_attributes(cls, args, kwargs):
        def pair(arg):
            if isinstance(arg, tuple):
                if len(arg) != 2:
                    raise ValueError("Attribute argument must be tuple of 2 elements (name, value).")
                return arg
            elif isinstance(arg, str_types):
                return (arg, None)
            else:
                raise ValueError("Couldn't make an attribute/value pair out of %r." % arg)

        result = dict(pair(a) for a in args)
        result.update({ATTRIBUTE_SUBSTITUTES.get(k, k): v for k, v in kwargs.items()})
        return result

    @classmethod
    def _form_attributes(cls, attributes_dict):
        assert isinstance(attributes_dict, dict)

        def sorting_function(element):
            attribute_name = element[0]
            default_rank = cls.attribute_precedence_rank["default rank for other attributes"]
            attribute_rank = cls.attribute_precedence_rank.get(attribute_name, default_rank)
            return attribute_rank, attribute_name

        def collect_attributes():
            for key, value in sorted(attributes_dict.items(), key=sorting_function):
                if value is None:
                    yield " %s" % key
                else:
                    yield " %s=%r" % (key, value)

        return ''.join(list(collect_attributes()))

    def _build_lines(self):
        begin_tag = "<%s%s>" % (self.tag_name, self._form_attributes(self.attributes))
        end_tag = "</%s>" % self.tag_name
        inner_lines = [line for child in self.children for line in child._build_lines()]

        if len(inner_lines) <= 1:
            # try to fit it in single line
            parts = [begin_tag] + [str(l) for l in inner_lines] + [end_tag]
            total_length = sum(map(len, parts))
            if total_length <= self.max_line_width:
                return [IndentableLine("".join(parts))]

        for c in inner_lines:
            c.increase_indent()
        return [IndentableLine(begin_tag)] + inner_lines + [IndentableLine(end_tag)]


class SingleTag(Tag):
    """ E.g.: <br />, <hr /> or <img src="#" alt="" /> """

    def _build_lines(self):
        tag_body = "<%s%s />" % (self.tag_name, self._form_attributes(self.attributes))
        return [IndentableLine(tag_body)]


class Text(object):
    __slots__ = ("_text", )

    def __init__(self, text):
        self._text = text

    def _build_lines(self):
        return [IndentableLine(l) for l in self._text.split("\n")]

    def __str__(self):
        return self._text


class Asis(Text):

    def _build_lines(self):
        return [NonindentableLine(str(self))]


class CdataTag(Asis):

    def __str__(self):
        return "<![CDATA[%s]]>" % self._text


class Doc(object):

    class DocumentRootTag(object):
        __slots__ = ("children", )

        def __init__(self):
            self.children = []

    def __init__(self):
        self._root_tag = Doc.DocumentRootTag()
        self.__tag_stack = [self._root_tag]

    def __str__(self):
        return "".join(str(c) for c in self._root_tag.children)

    @property
    def _children(self):
        top_most_element = self.__tag_stack[-1]
        return top_most_element.children

    @contextmanager
    def tag(self, tag_name, *args, **kwargs):
        tag = Tag(tag_name, *args, **kwargs)
        self._children.append(tag)
        self.__tag_stack.append(tag)
        try:
            yield
        finally:
            self.__tag_stack.pop()

    def text(self, *text_):
        self._children.extend([Text(t) for t in text_])

    def line(self, tag_name, content="", *args, **kwargs):
        tag = Tag(tag_name, *args, **kwargs)
        tag.children.append(Text(content))
        self._children.append(tag)

    def stag(self, tag_name, *args, **kwargs):
        tag = SingleTag(tag_name, *args, **kwargs)
        self._children.append(tag)

    def tagtext(self):
        return self, self.tag, self.text

    def ttl(self):
        return self, self.tag, self.text, self.line

    def getvalue(self):
        return str(self)

    def cdata(self, raw_text):
        self._children.append(CdataTag(raw_text))

    def asis(self, raw_text):
        self._children.append(Asis(raw_text))
