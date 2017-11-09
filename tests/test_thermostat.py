import json
import responses

from nuheat import NuHeat, NuHeatThermostat, config
from mock import patch
from . import NuTestCase, urlencode


class TestThermostat(NuTestCase):

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_init(self, _):
        api = NuHeat(None, None)
        serial_number = "serial-123"
        thermostat = NuHeatThermostat(api, serial_number)
        self.assertEqual(thermostat.serial_number, serial_number)
        self.assertEqual(thermostat._session, api)

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
        response_data = self.load_fixture("thermostat.json")
        responses.add(
            responses.GET,
            config.THERMOSTAT_URL,
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )
        api = NuHeat(None, None)
        api.session_id = "my-session"
        serial_number = "my-thermostat"
        params = {
            "sessionid": api.session_id,
            "serialnumber": serial_number
        }
        request_url = "{}?{}".format(config.THERMOSTAT_URL, urlencode(params))

        thermostat = NuHeatThermostat(api, serial_number)
        thermostat.get_data()

        api_call = responses.calls[0]
        self.assertEqual(api_call.request.method, "GET")
        self.assertEqual(api_call.request.url, request_url)

        self.assertEqual(thermostat._data, response_data)
        self.assertEqual(thermostat.heating, response_data["Heating"])
        self.assertEqual(thermostat.online, response_data["Online"])
        self.assertEqual(thermostat.room, response_data["Room"])
        self.assertEqual(thermostat.serial_number, response_data["SerialNumber"])
        self.assertEqual(thermostat.temperature, response_data["Temperature"])
        self.assertEqual(thermostat.target_temperature, response_data["SetPointTemp"])

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
        thermostat.set_target_temperature(2222)
        set_data.assert_called_with({
            "SetPointTemp": 2222,
            "ScheduleMode": config.SCHEDULE_HOLD
        })

        thermostat.set_target_temperature(2222, permanent=False)
        set_data.assert_called_with({
            "SetPointTemp": 2222,
            "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD
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

        api = NuHeat(None, None)
        api.session_id = "my-session"
        serial_number = "my-thermostat"
        params = {
            "sessionid": api.session_id,
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
