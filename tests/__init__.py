import json
import os
import unittest

try:  # Python 3
    from urllib.parse import urlencode
except ImportError:  # Python 2
    from urllib import urlencode


class NuTestCase(unittest.TestCase):

    def load_fixture(self, filename):
        """
        Load some fixture JSON
        """
        path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
        with open(path) as json_data:
            return json.load(json_data)
