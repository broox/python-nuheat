import json
import responses

from unittest.mock import patch
from parameterized import parameterized
from urllib.parse import urlencode

from nuheat import NuHeat, NuHeatThermostat
from . import NuTestCase, load_fixture


class TestNuHeat(NuTestCase):
    # pylint: disable=protected-access

    @parameterized.expand([
        (None, "mynuheat.com"),
        ("NUHEAT", "mynuheat.com"),
        ("BAD-BRAND", "mynuheat.com"),
        ("MAPEHEAT", "mymapeheat.com"),
    ])
    def test_brands(self, brand, hostname):
        api = NuHeat("test@example.com", "secure-password", brand=brand)
        self.assertEqual(api._hostname, hostname)
        self.assertEqual(api._api_url, f"https://{hostname}/api")
        self.assertEqual(api._auth_url, f"https://{hostname}/api/authenticate/user")

    def test_init_with_session(self):
        existing_session_id = "passed-session"
        api = NuHeat("test@example.com", "secure-password", existing_session_id)
        self.assertEqual(api._session_id, existing_session_id)
        api.authenticate()

    def test_repr(self):
        email = "test@example.com"
        api = NuHeat(email, "secure-password")
        self.assertEqual(str(api), "<NuHeat username='{}'>".format(email))

    @responses.activate
    def test_successful_authentication(self):
        api = NuHeat("test@example.com", "secure-password")

        response_data = load_fixture("auth_success.json")
        responses.add(
            responses.POST,
            api._auth_url,
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )

        self.assertIsNone(api._session_id)
        api.authenticate()
        self.assertEqual(api._session_id, response_data.get("SessionId"))

    @responses.activate
    def test_authentication_error(self):
        api = NuHeat("test@example.com", "secure-password")

        response_data = load_fixture("auth_error.json")
        responses.add(
            responses.POST,
            api._auth_url,
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )

        with self.assertRaises(Exception) as _:
            api.authenticate()
            self.assertIsNone(api._session_id)

    def test_authentication_failure(self):
        # TODO: 401, expired session
        pass

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_get_thermostat(self, _):
        api = NuHeat(None, None)
        serial_number = "serial-123"
        thermostat = api.get_thermostat(serial_number)
        self.assertTrue(isinstance(thermostat, NuHeatThermostat))

    @responses.activate
    def test_get_request(self):
        url = "http://www.example.com/api"
        params = dict(test="param")
        responses.add(
            responses.GET,
            url,
            status=200,
            content_type="application/json"
        )
        api = NuHeat(None, None)
        response = api.request(url, method="GET", params=params)

        self.assertEqual(response.status_code, 200)
        self.assertUrlsEqual(response.request.url, "{}?{}".format(url, urlencode(params)))
        request_headers = response.request.headers
        self.assertEqual(
            request_headers["Origin"],
            api._request_headers["Origin"],
        )
        self.assertEqual(
            request_headers["Content-Type"],
            api._request_headers["Content-Type"],
        )

    @responses.activate
    def test_post_request(self):
        url = "http://www.example.com/api"
        params = dict(test="param")
        data = dict(test="data")
        responses.add(
            responses.POST,
            url,
            status=200,
            content_type="application/json"
        )
        api = NuHeat(None, None)
        response = api.request(url, method="POST", data=data, params=params)

        self.assertEqual(response.status_code, 200)
        self.assertUrlsEqual(response.request.url, "{}?{}".format(url, urlencode(params)))
        self.assertEqual(response.request.body, urlencode(data))
        request_headers = response.request.headers
        self.assertEqual(
            request_headers["Origin"],
            api._request_headers["Origin"],
        )
        self.assertEqual(
            request_headers["Content-Type"],
            api._request_headers["Content-Type"],
        )
