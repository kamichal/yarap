import yattag

from .utils import fix_yattag
from .elements_def import H4, H5, CONTEXT_ELEMENTS, EMPTY_ELEMENTS

fix_yattag(yattag)


class Ya5(yattag.SimpleDoc):
    version = H5

    def __init__(self, stag_end=">"):
        super(Ya5, self).__init__(stag_end)

        def create_contextual(elm):
            def _tag(*args, **kwargs):
                return self.tag(elm.tag, *args, **kwargs)
            _tag.__name__ = elm.tag
            _tag.__doc__ = elm.info

            return _tag

        def create_empty(elm):
            def _stag(*args, **kwargs):
                return self.stag(elm.tag, *args, **kwargs)
            _stag.__name__ = elm.tag
            _stag.__doc__ = elm.info

            return _stag

        for elem in CONTEXT_ELEMENTS[self.version]:
            setattr(self, elem.tag, create_contextual(elem))

        for elem in EMPTY_ELEMENTS[self.version]:
            setattr(self, elem.tag, create_empty(elem))


class Ya4(Ya5):
    version = H4


def test_1():

    y = Ya5()
    with y.html():
        with y.body():
            with y.div():
                with y.p(klass='ok'):
                    y.text("that's all")
                    y.br()
            y.img(href='12')

    render = y.getvalue()
    assert render == '<html><body><div><p class="ok">that\'s all<br></p></div><img href="12"></body></html>'
