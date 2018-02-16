import sys


if sys.version < '3':
    str_types = (str, unicode)
    from itertools import ifilter
else:
    ifilter = filter
    str_types = str
