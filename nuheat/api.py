import logging
import requests
from nuheat import config, util
from nuheat.thermostat import NuHeatThermostat

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class NuHeat(object):

    def __init__(self, username, password, session_id=None, brand=config.NUHEAT):
        """
        Initialize a NuHeat API session

        :param username: NuHeat username
        :param username: NuHeat password
        :param session_id: A Session ID token to re-use to avoid re-authenticating
        :param brand: Manages which API is used, can be NUHEAT or MAPEHEAT
        """
        self.username = username
        self.password = password
        self._session_id = session_id
        self._brand = brand if brand in config.BRANDS else config.BRANDS[0]

    def __repr__(self):
        return "<NuHeat username='{}'>".format(self.username)

    def authenticate(self):
        """
        Authenticate against the NuHeat API
        """
        if self._session_id:
            _LOGGER.debug("Using existing NuHeat session")
            return

        _LOGGER.debug("Creating NuHeat session")
        post_data = {
            "Email": self.username,
            "Password": self.password,
            "application": "0"
        }
        data = self.request(
            url=util.get_auth_url(config=config, brand=self._brand),
            method="POST",
            data=post_data,
        )
        session_id = data.get("SessionId")
        if not session_id:
            raise Exception("Authentication error")

        self._session_id = session_id

    def get_thermostat(self, serial_number):
        """
        Get a thermostat object by serial number

        :param serial_number: The serial number / ID of the desired thermostat
        """
        return NuHeatThermostat(self, serial_number)

    def request(self, url, method="GET", data=None, params=None, retry=True):
        """
        Make a request to the NuHeat API

        :param url: The URL to request
        :param method: The type of request to make (GET, POST)
        :param data: Data to be sent along with POST requests
        :param params: Querystring parameters
        :param retry: Attempt to re-authenticate and retry request if necessary
        """
        headers = util.get_request_headers(
            config=config,
            brand=self._brand,
        )

        if params and self._session_id:
            params['sessionid'] = self._session_id

        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, params=params, data=data)

        # Handle expired sessions
        if response.status_code == 401 and retry:
            _LOGGER.warning("NuHeat APIrequest unauthorized for  [401]. Try to re-authenticate.")
            self._session_id = None
            self.authenticate()
            return self.request(url, method=method, data=data, params=params, retry=False)

        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            # No JSON object
            return response
