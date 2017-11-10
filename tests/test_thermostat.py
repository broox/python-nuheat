import json
import unittest

import responses

from nuheat import NuHeat, NuHeatThermostat, config
from mock import patch
from . import load_fixture, urlencode


class TestThermostat(unittest.TestCase):
    # pylint: disable=protected-access
    # pylint: disable=no-self-use

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_init(self, _):
        api = NuHeat(None, None)
        serial_number = "serial-123"
        thermostat = NuHeatThermostat(api, serial_number)
        self.assertEqual(thermostat.serial_number, serial_number)
        self.assertEqual(thermostat._session, api)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_repr_without_data(self, _):
        api = NuHeat(None, None)
        serial_number = "serial-123"
        thermostat = NuHeatThermostat(api, serial_number)
        self.assertEqual(
            str(thermostat),
            "<NuHeatThermostat id='{}' temperature='{}F / {}C' target='{}F / {}C'>".format(
                serial_number,
                None,
                None,
                None,
                None
            )
        )

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_repr_with_data(self, _):
        api = NuHeat(None, None)
        serial_number = "serial-123"
        thermostat = NuHeatThermostat(api, serial_number)
        thermostat.temperature = 2000
        thermostat.target_temperature = 5000
        self.assertEqual(
            str(thermostat),
            "<NuHeatThermostat id='{}' temperature='{}F / {}C' target='{}F / {}C'>".format(
                serial_number,
                68,
                20,
                122,
                50
            )
        )

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_fahrenheit(self, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.temperature = 2222
        self.assertEqual(thermostat.fahrenheit, 72)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_celsius(self, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.temperature = 2222
        self.assertEqual(thermostat.celsius, 22)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_min_fahrenheit(self, _):
        thermostat = NuHeatThermostat(None, None)
        self.assertEqual(thermostat.min_fahrenheit, None)
        thermostat.min_temperature = 500
        self.assertEqual(thermostat.min_fahrenheit, 41)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_min_celsius(self, _):
        thermostat = NuHeatThermostat(None, None)
        self.assertEqual(thermostat.min_celsius, None)
        thermostat.min_temperature = 500
        self.assertEqual(thermostat.min_celsius, 5)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_max_fahrenheit(self, _):
        thermostat = NuHeatThermostat(None, None)
        self.assertEqual(thermostat.max_fahrenheit, None)
        thermostat.max_temperature = 7000
        self.assertEqual(thermostat.max_fahrenheit, 157)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_max_celsius(self, _):
        thermostat = NuHeatThermostat(None, None)
        self.assertEqual(thermostat.max_celsius, None)
        thermostat.max_temperature = 7000
        self.assertEqual(thermostat.max_celsius, 69)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_target_fahrenheit(self, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.target_temperature = 2222
        self.assertEqual(thermostat.target_fahrenheit, 72)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_target_celsius(self, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.target_temperature = 2222
        self.assertEqual(thermostat.target_celsius, 22)

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_target_temperature")
    def test_target_fahrenheit_setter(self, set_target_temperature, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.target_fahrenheit = 80
        set_target_temperature.assert_called_with(2665, permanent=True)

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_target_temperature")
    def test_target_celsius_setter(self, set_target_temperature, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.target_celsius = 26
        set_target_temperature.assert_called_with(2609, permanent=True)

    @responses.activate
    def test_get_data(self):
        response_data = load_fixture("thermostat.json")
        responses.add(
            responses.GET,
            config.THERMOSTAT_URL,
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )
        api = NuHeat(None, None, session_id="my-session")
        serial_number = response_data.get("SerialNumber")
        params = {
            "sessionid": api._session_id,
            "serialnumber": serial_number
        }
        request_url = "{}?{}".format(config.THERMOSTAT_URL, urlencode(params))

        thermostat = NuHeatThermostat(api, serial_number)
        # responses.calls.reset()  # get_data() is called once on NuHeatThermostat.__init__()
        thermostat.get_data()

        api_calls = responses.calls

        # Data is fetched once on instantiation and once on get_data()
        self.assertEqual(len(api_calls), 2)

        api_call = api_calls[0]
        self.assertEqual(api_call.request.method, "GET")
        self.assertEqual(api_call.request.url, request_url)

        self.assertEqual(thermostat._data, response_data)
        self.assertEqual(thermostat.heating, response_data["Heating"])
        self.assertEqual(thermostat.online, response_data["Online"])
        self.assertEqual(thermostat.room, response_data["Room"])
        self.assertEqual(thermostat.serial_number, response_data["SerialNumber"])
        self.assertEqual(thermostat.temperature, response_data["Temperature"])
        self.assertEqual(thermostat.min_temperature, response_data["MinTemp"])
        self.assertEqual(thermostat.max_temperature, response_data["MaxTemp"])
        self.assertEqual(thermostat.target_temperature, response_data["SetPointTemp"])
        self.assertEqual(thermostat.schedule_mode, response_data["ScheduleMode"])

    @responses.activate
    def test_get_data_401(self):
        # First request (when initializing the thermostat) is successful
        response_data = load_fixture("thermostat.json")
        responses.add(
            responses.GET,
            config.THERMOSTAT_URL,
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )

        # A later, second request throws 401 Unauthorized
        responses.add(
            responses.GET,
            config.THERMOSTAT_URL,
            status=401
        )

        # Attempt to reauthenticate
        auth_data = load_fixture("auth_success.json")
        responses.add(
            responses.POST,
            config.AUTH_URL,
            status=200,
            body=json.dumps(auth_data),
            content_type="application/json"
        )

        # Third request is successful
        responses.add(
            responses.GET,
            config.THERMOSTAT_URL,
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )

        bad_session_id = "my-bad-session"
        good_session_id = auth_data.get("SessionId")
        api = NuHeat(None, None, session_id=bad_session_id)
        serial_number = response_data.get("SerialNumber")

        thermostat = NuHeatThermostat(api, serial_number)
        thermostat.get_data()
        self.assertTrue(isinstance(thermostat, NuHeatThermostat))

        api_calls = responses.calls
        self.assertEqual(len(api_calls), 4)

        unauthorized_attempt = api_calls[1]
        params = {"sessionid": bad_session_id, "serialnumber": serial_number}
        request_url = "{}?{}".format(config.THERMOSTAT_URL, urlencode(params))
        self.assertEqual(unauthorized_attempt.request.method, "GET")
        self.assertEqual(unauthorized_attempt.request.url, request_url)
        self.assertEqual(unauthorized_attempt.response.status_code, 401)

        auth_call = api_calls[2]
        self.assertEqual(auth_call.request.method, "POST")
        self.assertEqual(auth_call.request.url, config.AUTH_URL)

        second_attempt = api_calls[3]
        params["sessionid"] = good_session_id
        request_url = "{}?{}".format(config.THERMOSTAT_URL, urlencode(params))
        self.assertEqual(second_attempt.request.method, "GET")
        self.assertEqual(second_attempt.request.url, request_url)
        self.assertEqual(second_attempt.response.status_code, 200)

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_data")
    def test_response_schedule(self, set_data, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.resume_schedule()
        set_data.assert_called_with({"ScheduleMode": config.SCHEDULE_RUN})

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_data")
    def test_set_target_temperature(self, set_data, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.min_temperature = 500
        thermostat.max_temperature = 7000

        # Permanent hold
        thermostat.set_target_temperature(2222)
        set_data.assert_called_with({
            "SetPointTemp": 2222,
            "ScheduleMode": config.SCHEDULE_HOLD
        })

        # Temporary hold
        thermostat.set_target_temperature(2222, permanent=False)
        set_data.assert_called_with({
            "SetPointTemp": 2222,
            "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD
        })

        # Below minimum
        thermostat.set_target_temperature(481)
        set_data.assert_called_with({
            "SetPointTemp": 500,
            "ScheduleMode": config.SCHEDULE_HOLD
        })

        # Above maximum
        thermostat.set_target_temperature(7020)
        set_data.assert_called_with({
            "SetPointTemp": 7000,
            "ScheduleMode": config.SCHEDULE_HOLD
        })

    @responses.activate
    @patch("nuheat.NuHeatThermostat.get_data")
    def test_set_data(self, _):
        responses.add(
            responses.POST,
            config.THERMOSTAT_URL,
            status=200,
            content_type="application/json"
        )

        api = NuHeat(None, None, session_id="my-session")
        serial_number = "my-thermostat"
        params = {
            "sessionid": api._session_id,
            "serialnumber": serial_number
        }
        request_url = "{}?{}".format(config.THERMOSTAT_URL, urlencode(params))
        post_data = {"test": "data"}
        thermostat = NuHeatThermostat(api, serial_number)
        thermostat.set_data(post_data)

        api_call = responses.calls[0]
        self.assertEqual(api_call.request.method, "POST")
        self.assertEqual(api_call.request.url, request_url)
        self.assertEqual(api_call.request.body, urlencode(post_data))
