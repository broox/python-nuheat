import requests
import nuheat.config as config
from nuheat.thermostat import NuHeatThermostat


class NuHeat(object):

    def __init__(self, username, password, session_id=None):
        """
        Initialize a NuHeat API session

        :param username: NuHeat username
        :param username: NuHeat password
        :param session_id: A Session ID token to re-use to avoid re-authenticating
        """
        self.username = username
        self.password = password
        self.session_id = session_id

    def __repr__(self):
        return "<NuHeat username='{}'>".format(self.username)

    def authenticate(self):
        """
        Authenticate against the NuHeat API
        """
        if self.session_id:
            return

        post_data = {
            "Email": self.username,
            "Password": self.password,
            "application": "0"
        }
        data = self.request(config.AUTH_URL, method="POST", data=post_data)
        session_id = data.get("SessionId")
        if not session_id:
            raise Exception("Authentication error")

        self.session_id = session_id

    def get_thermostat(self, serial_number):
        """
        Get a thermostat object by serial number

        :param serial_number: The serial number / ID of the desired thermostat
        """
        return NuHeatThermostat(self, serial_number)

    def request(self, url, method="GET", data=None, params=None):
        """
        Make a request to the NuHeat API

        :param url: The URL to request
        :param method: The type of request to make (GET, POST)
        :param data: Data to be sent along with POST requests
        :param params: Querystring parameters
        """
        headers = config.REQUEST_HEADERS

        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, params=params, data=data)

        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            # No JSON object
            return response
