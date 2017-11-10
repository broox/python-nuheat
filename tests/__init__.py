import json
import os

try:  # Python 3
    from urllib.parse import urlencode
except ImportError:  # Python 2
    from urllib import urlencode


def load_fixture(filename):
    """
    Load some fixture JSON
    """
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path) as json_data:
        return json.load(json_data)
