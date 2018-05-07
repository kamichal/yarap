from contextlib import contextmanager

from yawrap.six import str_types

"""
    The purpose of this module is to replace dependency to yattag with own machinery.
    The Doc class shares same interface with yattag. Cannot guarantee that, but in vast most
    of cases this module's code fully substitutes yattag.SimpleDoc class.

    The main reason - to make own code that supplements well known package is that:
    - the well known package doesn't create indentation on the fly.
    - the well known package doesn't like to change. New features are not welcome.
    - because no dependency and pure pythonic code are nice
"""


class IndentableLine(object):
    __slots__ = ("text", "indent_level")
    indenter = "  "

    def __init__(self, text):
        self.text = text
        self.indent_level = 0

    def increase_indent(self):
        self.indent_level += 1

    def __str__(self):
        indent = self.indenter * self.indent_level
        return "%s%s" % (indent, self.text)


class NonindentableLine(IndentableLine):
    indenter = ""


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

DEFAULT_ATTRIBUTE_ORDER = {
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


class Tag(object):
    __slots__ = ("tag_name", "attributes", "children")
    attribute_precedence_rank = DEFAULT_ATTRIBUTE_ORDER
    max_line_width = 100

    def __init__(self, tag_name, *args, **kwargs):
        self.tag_name = tag_name
        self.attributes = dict(self._process_attributes(args, kwargs))
        self.children = []

    def __str__(self):
        return "\n".join(str(l) for l in self._build_lines())

    @classmethod
    def _process_attributes(cls, args, kwargs):
        for arg in args:
            if isinstance(arg, tuple):
                if len(arg) != 2:
                    raise ValueError("Attribute argument must be tuple of 2 elements (name, value).")
                yield arg
            elif isinstance(arg, str_types):
                yield (arg, None)
            else:
                raise ValueError("Couldn't make an attribute & value pair out of %r." % arg)

        for key, value in kwargs.items():
            unslugged_key = ATTRIBUTE_SUBSTITUTES.get(key, key)
            yield unslugged_key, value

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

    def _update_attributes(self, *args, **kwargs):
        new_attrs = dict(self._process_attributes(args, kwargs))
        self.attributes.update(new_attrs)

    def _build_lines(self):
        begin_tag = "<%s%s>" % (self.tag_name, self._form_attributes(self.attributes))
        end_tag = "</%s>" % self.tag_name
        children_lines = [line for child in self.children for line in child._build_lines()]

        if len(children_lines) <= 1:
            # try to fit it in single line
            parts = [begin_tag] + [str(l) for l in children_lines] + [end_tag]
            total_length = sum(map(len, parts))
            if total_length <= self.max_line_width:
                return [IndentableLine("".join(parts))]

        for child_line in children_lines:
            child_line.increase_indent()
        return [IndentableLine(begin_tag)] + children_lines + [IndentableLine(end_tag)]


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
        return [IndentableLine(l) for l in str(self).split("\n")]

    def __str__(self):
        return self._text


class PlainText(Text):

    def _build_lines(self):
        return [NonindentableLine(str(self))]


class Comment(Text):
    def __str__(self):
        return "<!-- %s -->" % self._text


class CdataTag(PlainText):

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
    def _top_element(self):
        return self.__tag_stack[-1]

    @property
    def __root_element(self):
        return self.__tag_stack[0]

    @property
    def _attributes(self):
        return self._top_element.attributes

    @property
    def _children(self):
        return self._top_element.children

    def _clone_children(self, other_doc):
        assert isinstance(other_doc, Doc)
        self._children.extend(other_doc.__root_element.children)

    @contextmanager
    def tag(self, tag_name, *args, **kwargs):
        tag = Tag(tag_name, *args, **kwargs)
        self._children.append(tag)
        self.__tag_stack.append(tag)
        try:
            yield
        finally:
            self.__tag_stack.pop()

    def text(self, *text):
        self._children.extend([Text(t) for t in text])

    def line(self, tag_name, content="", *args, **kwargs):
        tag = Tag(tag_name, *args, **kwargs)
        tag.children.append(Text(content))
        self._children.append(tag)

    def stag(self, tag_name, *args, **kwargs):
        tag = SingleTag(tag_name, *args, **kwargs)
        self._children.append(tag)

    def tagtext(self):  # pragma: no cover
        return self, self.tag, self.text

    def ttl(self):  # pragma: no cover
        return self, self.tag, self.text, self.line

    def getvalue(self):
        return str(self)

    def comment(self, text):
        self._children.append(Comment(text))

    def cdata(self, raw_text):
        self._children.append(CdataTag(raw_text))

    def asis(self, raw_text):
        """ add the text, whatever is there """
        self._children.append(PlainText(raw_text))

    def nl(self):
        """ adds blank line to resulting html document """
        self.asis("")

    def attr(self, *args, **kwargs):
        """ update attribures of current element """
        self._top_element._update_attributes(*args, **kwargs)

    def classes(self):
        top_element = self._top_element
        assert not isinstance(top_element, self.DocumentRootTag), "Root element has no classes."
        return top_element.attributes.get("class", "").split()

    def add_class(self, names):
        """ adds class names (space-separated words) to current element """
        assert isinstance(names, str_types)
        classes = self.classes()

        for name in names.split():
            if name not in classes:
                classes.append(name)

        self._attributes.update({"class": " ".join(classes)})

    def discard_class(self, names):
        """ removes class names (space-separated words) to current element """
        assert isinstance(names, str_types)
        classes = self.classes()
        for name in names.split():
            if name in classes:
                classes.pop(classes.index(name))
        if classes:
            self._attributes.update({"class": " ".join(classes)})
        else:
            self._attributes.pop("class", None)

    def toggle_class(self, names):
        """ toggles class names (space-separated words) to current element """
        already_processed = []
        for name in names.split():
            if name not in already_processed:
                if name in self.classes():
                    self.discard_class(name)
                else:
                    self.add_class(name)
                already_processed.append(name)
