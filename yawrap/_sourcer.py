"""
    There are some possibilities when you want to use CSS or JS scripts in a html page.

    A. When the content is on the web, specified by an url - you may want to:
        1. download it (while the page is being built), save it and reference it from a directory
        relative to target page (several pages may wont like to share the file)
        2. embed it in the target page (it's better for a single-file document type)
        3. just reference it by the url (will require web access for each view)

    B. When the content is in a local file - you may want to:
        1. export it to directory relative to a target document or
        2. embed it in the document (CSS in head, JS anywhere)

    B'. When the content is in loacal python string - you may want to:
        1. export it to directory relative to a target document or
        2. embed it in the document (CSS in head, JS anywhere)
"""

from contextlib import closing
import os
import posixpath

from .six import urlopen, urlparse, str_types
from .utils import make_place, is_url, error, warn_
from yawrap.utils import form_css, dictionize_css


HEAD = "head"
BODY_END = "body_end"
BODY_BEGIN = "body_begin"
PLACEMENT_OPTIONS = [HEAD, BODY_BEGIN, BODY_END]


class _Resource(object):
    """
        Class that provides methods of resource content's acquisition.
        The from_url and from_file classmethods are supposed to serve alternative contructors.
    """

    def __init__(self, read_method, file_name):
        self.read_method = read_method
        self.file_name = file_name

    @classmethod
    def from_url(cls, url, placement=HEAD):
        """ Provide content of the resource from the web. """
        assert url, "Bad argument: %s" % url
        assert is_url(url), "That doesn't seem to be a valid url: %s" % url
        assert issubclass(cls, _DocumentVisitor), "You messed up."

        def read_method():
            return cls._download(url)

        file_name = posixpath.basename(urlparse(url).path)
        return cls(read_method, placement, file_name)

    @classmethod
    def from_file(cls, file_path, placement=HEAD):
        """ Provide content of the resource from a local file. """
        assert file_path, "Bad argument: %s" % file_path
        assert os.path.isfile(file_path), "That file doesn't exist: %s" % file_path
        file_name = os.path.basename(file_path)

        def read_method():
            return cls._read_file(file_path)
        assert issubclass(cls, _DocumentVisitor), "You messed up."
        return cls(read_method, placement, file_name)

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


class _DocumentVisitor(object):

    def __init__(self, placement_target):
        assert placement_target in PLACEMENT_OPTIONS, "Invalid placement type."
        self._placement = placement_target

    def _placement_match(self, placement):
        return self._placement == placement

    def visit(self, page_doc, yawrap_instance, placement):
        if self._placement_match(placement):
            self.act(page_doc, yawrap_instance)

    @classmethod
    def act(self):
        raise ValueError("You messed up.")


class _JsResource(_Resource, _DocumentVisitor):
    type_ = "text/javascript"

    def __init__(self, read_function_or_str, placement=HEAD, file_name=None):
        if isinstance(read_function_or_str, str_types):
            def read_method():
                return read_function_or_str
        else:
            read_method = read_function_or_str

        _Resource.__init__(self, read_method, file_name)
        _DocumentVisitor.__init__(self, placement)

    @classmethod
    def link(cls, page_doc, href):
        with page_doc.tag('script', src=href):
            pass

    @classmethod
    def embed(cls, page_doc, content):
        with page_doc.tag('script', type=cls.type_):
            page_doc.asis(content)


class _CssResource(_Resource, _DocumentVisitor):
    rel = "stylesheet"
    type_ = "text/css"

    def __init__(self, read_function_or_str_or_dict, placement=HEAD, file_name=None):
        if placement != HEAD:
            raise TypeError("Cannot place CSS out of head section (%s)" % placement)

        if isinstance(read_function_or_str_or_dict, str_types):
            def read_method():
                return form_css(dictionize_css(read_function_or_str_or_dict), indent_level=0)
        elif isinstance(read_function_or_str_or_dict, dict):
            def read_method():
                return form_css(read_function_or_str_or_dict, indent_level=0)
        else:
            read_method = read_function_or_str_or_dict

        _Resource.__init__(self, read_method, file_name)
        _DocumentVisitor.__init__(self, placement)

    @classmethod
    def link(cls, page_doc, href):
        page_doc.stag('link', rel=cls.rel, type=cls.type_, href=href)

    @classmethod
    def embed(cls, page_doc, content):
        content = form_css(dictionize_css(content), indent_level=0)
        with page_doc.tag('style'):
            page_doc.asis(content)

    def _placement_match(self, placement):
        assert self._placement == HEAD, "CSS can be placed only in head section."
        return self._placement == placement


class _Embed(_DocumentVisitor):

    def act(self, page_doc, _):
        content = self.read_method()
        self.embed(page_doc, content)


class _ExportToTargetFs(_DocumentVisitor):
    resource_subdir = "resources"

    def act(self, page_doc, yawrap_instance):
        self._check_file_name_provided()
        href = self._create_local_file(yawrap_instance)
        self.link(page_doc, href)

    def _check_file_name_provided(self):
        if not self.file_name:
            raise ValueError("You need to provide filename in order to store "
                             "the content for %s operation." % self.__class__.__name__)

    def _create_local_file(self, yawrap_instance):
        root_dir = yawrap_instance.get_root_dir()
        target_file = os.path.join(root_dir, self.resource_subdir, self.file_name)
        content = self.read_method()
        self._save_as_file(content, target_file)
        href = posixpath.relpath(target_file, yawrap_instance._target_dir)
        return href

    @staticmethod
    def _save_as_file(str_content, target_file_path):
        if os.path.exists(target_file_path):
            warn_("File: %s already exists, overwritting." % target_file_path)
        with open(make_place(target_file_path), "wt") as ff:
            ff.write(str_content)


class _LinkExternalURL(_DocumentVisitor):

    def __init__(self, url, placement=HEAD):
        assert is_url(url), "That doesn't seem to be a valid url: %s" % url
        self.url = url
        _DocumentVisitor.__init__(self, placement)

    def act(self, page_doc, _):
        self.link(page_doc, self.url)

    @classmethod
    def from_url(cls, url, placement=HEAD):
        return cls(url, placement)  # constructor bypass

    @classmethod
    def from_file(cls, *_, **__):
        raise TypeError("Cannot reference remote/external file by local file content.")


class EmbedCss(_Embed, _CssResource):
    pass


class EmbedJs(_Embed, _JsResource):
    pass


class LinkCss(_ExportToTargetFs, _CssResource):
    pass


class LinkJs(_ExportToTargetFs, _JsResource):
    pass


class ExtenalCss(_LinkExternalURL, _CssResource):
    pass


class ExtenalJs(_LinkExternalURL, _JsResource):
    pass
