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
from .utils import make_place, is_url
from yawrap.utils import form_css

HEAD = "head"
BODY_END = "body_end"
BODY_BEGIN = "body_begin"
PLACEMENT_OPTIONS = [HEAD, BODY_BEGIN, BODY_END]
RAISE_ON_DOWNLOAD_FAIL = True


def warn_(text):
    print(text)


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
        file_name = os.path.basename(file_path)

        def read_method():
            return cls._read_file(file_path)
        assert issubclass(cls, _DocumentVisitor), "You messed up."
        return cls(read_method, placement, file_name)

    @staticmethod
    def _download(url):
        assert is_url(url), "That doesn't seem to be a valid url: %s" % url
        try:
            with closing(urlopen(url, timeout=3)) as response:
                return response.read()
        except Exception as e:  # pragma: no cover
            if RAISE_ON_DOWNLOAD_FAIL:
                raise
            else:
                print("unable to download: %s\n%s" % (url, e))
                return ""

    @staticmethod
    def _read_file(file_path):
        assert os.path.isfile(file_path), "File doesn't exist: %s" % file_path
        with open(file_path, "rt") as ff:
            return ff.read()


class _DocumentVisitor(_Resource):

    def __init__(self, read_function_or_str, placement=HEAD, file_name=None):
        self._check_placement(placement)
        self._placement = placement
        read_method = self._form_read_method(read_function_or_str)
        _Resource.__init__(self, read_method, file_name)

    @classmethod
    def _form_read_method(cls, read_function_or_str):
        if isinstance(read_function_or_str, str_types):
            def read_method():
                return read_function_or_str
            return read_method
        else:
            return read_function_or_str

    def _check_placement(self, placement):
        assert (placement in PLACEMENT_OPTIONS), "Wrong placement value: %s" % placement

    def _placement_match(self, placement):
        return self._placement == placement

    def visit(self, page_doc, yawrap_instance, placement):
        if self._placement_match(placement):
            self.act(page_doc, yawrap_instance)

    @classmethod
    def act(self):
        raise ValueError("You messed up. That shouldn't happen.")


class _JsResource(_DocumentVisitor):
    type_ = "text/javascript"

    @classmethod
    def link(cls, page_doc, href):
        with page_doc.tag('script', src=href):
            pass

    @classmethod
    def embed(cls, page_doc, content):
        with page_doc.tag('script', type=cls.type_):
            page_doc.asis(content)


class _CssResource(_DocumentVisitor):
    rel = "stylesheet"
    type_ = "text/css"

    @classmethod
    def link(cls, page_doc, href):
        page_doc.stag('link', rel=cls.rel, type=cls.type_, href=href)

    @classmethod
    def embed(cls, page_doc, content):
        with page_doc.tag('style'):
            page_doc.asis(content)

    @classmethod
    def _form_read_method(cls, function_or_str_or_dict):
        if isinstance(function_or_str_or_dict, str_types):
            def read_method():
                return function_or_str_or_dict
            return read_method
        elif isinstance(function_or_str_or_dict, dict):
            def read_method():
                return form_css(function_or_str_or_dict)
            return read_method
        else:
            return function_or_str_or_dict

    def _check_placement(self, placement):
        _DocumentVisitor._check_placement(self, placement)
        if placement != HEAD:
            raise TypeError("Cannot place CSS out of head section (%s)" % placement)


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
        super(_LinkExternalURL, self).__init__(lambda: self.url, placement=placement)

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


class ExternalCss(_LinkExternalURL, _CssResource):
    pass


class ExternalJs(_LinkExternalURL, _JsResource):
    pass
