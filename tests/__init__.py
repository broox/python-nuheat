import json
import os
import unittest

try:  # Python 3
    from urllib.parse import parse_qsl, urlencode, urlparse
except ImportError:  # Python 2
    from urllib import urlencode
    from urlparse import parse_qsl, urlparse


def load_fixture(filename):
    """
    Load some fixture JSON
    """
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path) as json_data:
        return json.load(json_data)


class Url(object):
    """
    A url object that can be compared with other url orbjects without regard to the vagaries of
    encoding, escaping, and ordering of parameters in query strings.
    """
    _url = None

    def __init__(self, url):
        self._url = url
        parts = urlparse(url)
        _query = frozenset(parse_qsl(parts.query))
        _path = parts.path
        parts = parts._replace(query=_query, path=_path)
        self.parts = parts

    def __repr__(self):
        return "<URL url='{}'>".format(self._url)

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.parts)


class NuTestCase(unittest.TestCase):

    def assertUrlsEqual(self, url1, url2):
        # pylint: disable=invalid-name
        self.assertEqual(Url(url1), Url(url2))
