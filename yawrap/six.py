import sys


if sys.version < '3':
    str_types = (str, unicode)
else:
    str_types = str
