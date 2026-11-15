import logging
import warnings

import requests

from nuheat import config
from nuheat.exceptions import NuHeatAuthError, NuHeatError
from nuheat.thermostat import NuHeatThermostat

_LOGGER = logging.getLogger(__name__)


class NuHeat(object):

    def __init__(self, username, password, session_id=None, brand=config.NUHEAT, timeout=config.DEFAULT_TIMEOUT):
        """
        Initialize a NuHeat API session

        :param username: NuHeat username
        :param password: NuHeat password
        :param session_id: A Session ID token to re-use to avoid re-authenticating
        :param brand: Manages which API is used, can be NUHEAT or MAPEHEAT
        :param timeout: requests timeout in seconds, either a number or a (connect, read) tuple
        """
        warnings.warn(config.DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)
        self.username = username
        self.password = password
        self._session_id = session_id
        self._brand = brand if brand in config.BRANDS else config.BRANDS[0]
        self._timeout = timeout
        self._http = requests.Session()

    def __repr__(self):
        return "<NuHeat username='{}'>".format(self.username)

    @property
    def _hostname(self):
        return config.HOSTNAMES.get(self._brand)

    @property
    def _api_url(self):
        return f"https://{self._hostname}/api"

    @property
    def _auth_url(self):
        return f"{self._api_url}/authenticate/user"

    @property
    def _request_headers(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "HOST": self._hostname,
            "DNT": "1",
            "Origin": self._api_url,
        }

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
            url=self._auth_url,
            method="POST",
            data=post_data,
        )
        session_id = data.get("SessionId")
        if not session_id:
            raise NuHeatAuthError("Authentication error")

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
        headers = self._request_headers

        if params and self._session_id:
            params['sessionid'] = self._session_id

        if method not in ("GET", "POST"):
            raise NuHeatError(f"Unsupported request method: {method}")

        try:
            response = self._http.request(
                method, url, headers=headers, params=params, data=data, timeout=self._timeout
            )
        except (requests.ConnectionError, requests.Timeout) as err:
            raise NuHeatError(f"Unable to reach {url}. {config.DEPRECATION_MESSAGE}") from err

        # Handle expired sessions
        if response.status_code == 401 and retry:
            _LOGGER.warning("NuHeat API request unauthorized [401]. Attempting to re-authenticate.")
            self._session_id = None
            self.authenticate()
            return self.request(url, method=method, data=data, params=params, retry=False)

        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            # No JSON object
            return response
