from ._engine import Doc
from .elements_def import H4, H5, CONTEXT_ELEMENTS, EMPTY_ELEMENTS


class Ya5(Doc):
    version = H5

    def __init__(self):
        super(Ya5, self).__init__()

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
