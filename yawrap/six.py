# flake8: noqa
import sys

if sys.version < '3':
    str_types = (str, unicode)
    from itertools import ifilter
    from urllib2 import urlopen
    from urlparse import urlparse

else:
    ifilter = filter
    str_types = str
    from urllib.request import urlopen
    from urllib.parse import urlparse
