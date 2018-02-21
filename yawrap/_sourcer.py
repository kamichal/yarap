"""
    There are some possibilities when you want to use CSS or JS scripts in a html page.

    A. When the content is on web, specified by an url - you may want to:
        1. save it and reference from a directory close to target page or 2. embed in the target page
        or 3. just reference it by the url

    B. When the content is in local file - you mpage ay want to:
        1. save it in target directory or 2. embed in the page

    C. When content is in loacal string variable - you may want to:
        1. save it in target directory or 2. embed in the page
"""

from contextlib import closing
import os
import posixpath

from .six import urlopen, urlparse, str_types
from .utils import make_place, is_url, error, warn_


HEAD = "head"
BODY_END = "body_end"
BODY_BEGIN = "body_begin"
PLACEMENT_OPTIONS = [HEAD, BODY_BEGIN, BODY_END]


class _Gainer(object):
    """ Class that handles acquisition of the resource content.
        It creates an object that exposes "read()" function and file_name, that can be also useful. """
    __slots__ = ("read", "file_name", "placement")

    def __init__(self, read_function_or_str, placement=HEAD, file_name=None):
        if isinstance(read_function_or_str, str_types):
            self.read = lambda: read_function_or_str
        else:
            self.read = read_function_or_str
        self.file_name = file_name
        self._placement = placement
        assert placement in PLACEMENT_OPTIONS

    @classmethod
    def from_url(cls, url, placement=HEAD):
        """ Provide content of the resource from the web. """
        assert url, "Bad argument: %s" % url
        assert is_url(url), "That doesn't seem to be a valid url: %s" % url
        file_name = posixpath.basename(urlparse(url).path)

        def read():
            return cls._download(url)
        return cls(read, placement, file_name)

    @classmethod
    def from_file(cls, file_path, placement=HEAD):
        """ Provide content of the resource from a local file. """
        assert file_path, "Bad argument: %s" % file_path
        assert os.path.isfile(file_path), "That file doesn't exist: %s" % file_path
        file_name = os.path.basename(file_path)

        def read():
            return cls._read_file(file_path)
        return cls(read, placement, file_name)

    @staticmethod
    def _download(url):
        assert is_url(url), "That doesn't seem to be a valid url: %s" % url
        try:
            with closing(urlopen(url)) as response:
                return response.read()
        except Exception as e:
            error("unable to download: %s\n%s" % (url, e))
            return "// Failed to download %s" % url

    @staticmethod
    def _read_file(file_path):
        assert os.path.exists(file_path), "File doesn't exist: %s" % file_path
        with open(file_path, "rt") as ff:
            return ff.read()

    def _placement_match(self, placement):
        assert placement in PLACEMENT_OPTIONS, "Invalid placement type."
        assert self._placement in PLACEMENT_OPTIONS, "Invalid placement type."
        return self._placement == placement

    @staticmethod
    def _save_as_file(str_content, target_file_path):
        if os.path.exists(target_file_path):
            warn_("File: %s already exists, overwritting." % target_file_path)
        with open(make_place(target_file_path), "wt") as ff:
            ff.write(str_content)


class _JsResource(_Gainer):
    type_ = "text/javascript"

    @classmethod
    def link(cls, doc, href):
        with doc.tag('script', src=href):
            pass

    @classmethod
    def embed(cls, doc, content):
        with doc.tag('script', type=cls.type_):
            doc.asis(content)


class _CssResource(_Gainer):
    rel = "stylesheet"
    type_ = "text/css"

    def __init__(self, read_function, placement=HEAD, file_name=None):
        if placement != HEAD:
            raise TypeError("Cannot place CSS out of head section (%s)" % placement)
        super(_CssResource, self).__init__(read_function, placement, file_name)

    @classmethod
    def link(cls, doc, href):
        doc.stag('link', rel=cls.rel, type=cls.type_, href=href)

    @classmethod
    def embed(cls, doc, content):
        with doc.tag('style'):
            doc.asis(content)

    def _placement_match(self, placement):
        assert self._placement == HEAD, "CSS can be placed only in head section."
        return self._placement == placement


class _Embed(_Gainer):

    def visit(self, doc, _, placement):
        if self._placement_match(placement):
            content = self.read()
            self.embed(doc, content)


class _LinkLocal(_Gainer):
    resource_subdir = "resources"

    def visit(self, doc, yawrap_doc, placement):
        if self._placement_match(placement):
            self._check_file_name_provided(self.file_name)

            root_dir = yawrap_doc.get_root_dir()
            target_file = os.path.join(root_dir, self.resource_subdir, self.file_name)
            content = self.read()
            self._save_as_file(content, target_file)
            href = posixpath.relpath(target_file, yawrap_doc._target_dir)
            self.link(doc, href)

    @classmethod
    def _check_file_name_provided(cls, file_name):
        if not file_name:
            raise ValueError("You need to provide filename in order to store "
                             "the content for %s operation." % cls.__name__)


class _LinkExternal(_Gainer):
    __slots__ = ("url", "placement")

    def __init__(self, url, placement=HEAD):
        assert is_url(url), "That doesn't seem to be a valid url: %s" % url
        self.url = url
        self._placement = placement

    def visit(self, doc, _, placement):
        if self._placement_match(placement):
            self.link(doc, self.url)

    @classmethod
    def from_url(cls, url, placement=HEAD):
        return cls(url, placement)

    @classmethod
    def from_file(cls, *_):
        raise TypeError("Cannot reference remote/external file by local file content.")


class EmbedCss(_Embed, _CssResource):
    pass


class EmbedJs(_Embed, _JsResource):
    pass


class LinkCss(_LinkLocal, _CssResource):
    pass


class LinkJs(_LinkLocal, _JsResource):
    pass


class ExtenalCss(_LinkExternal, _CssResource):
    pass


class ExtenalJs(_LinkExternal, _JsResource):
    pass
