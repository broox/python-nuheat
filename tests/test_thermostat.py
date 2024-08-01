import json
import responses

from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from parameterized import parameterized
from urllib.parse import urlencode

from nuheat import NuHeat, NuHeatThermostat, config
from . import NuTestCase, load_fixture


class TestThermostat(NuTestCase):
    # pylint: disable=protected-access
    # pylint: disable=no-self-use

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_init(self, _):
        api = NuHeat(None, None)
        serial_number = "serial-123"
        thermostat = NuHeatThermostat(api, serial_number)
        self.assertEqual(thermostat.serial_number, serial_number)
        self.assertEqual(thermostat._session, api)

    @parameterized.expand([
        (None, "mynuheat.com"),
        ("NUHEAT", "mynuheat.com"),
        ("BAD-BRAND", "mynuheat.com"),
        ("MAPEHEAT", "mymapeheat.com"),
    ])
    @patch("nuheat.NuHeatThermostat.get_data")
    def test_brand_urls(self, brand, hostname, _):
        api = NuHeat(None, None, brand=brand)
        serial_number = "serial-123"
        thermostat = NuHeatThermostat(api, serial_number)
        self.assertEqual(thermostat._url, f"https://{hostname}/api/thermostat")

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
    @patch("nuheat.NuHeatThermostat.set_target_fahrenheit")
    def test_target_fahrenheit_setter(self, set_target_fahrenheit, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.target_fahrenheit = 80
        set_target_fahrenheit.assert_called_with(80)

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_target_celsius")
    def test_target_celsius_setter(self, set_target_celsius, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.target_celsius = 26
        set_target_celsius.assert_called_with(26)

    @responses.activate
    def test_get_data(self):
        response_data = load_fixture("thermostat.json")

        api = NuHeat(None, None, session_id="my-session")

        responses.add(
            responses.GET,
            f"{api._api_url}/thermostat",
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )

        serial_number = response_data.get("SerialNumber")
        thermostat = NuHeatThermostat(api, serial_number)

        params = {
            "sessionid": api._session_id,
            "serialnumber": serial_number
        }
        request_url = "{}?{}".format(
            thermostat._url,
            urlencode(params),
        )

        thermostat.get_data()

        api_calls = responses.calls

        # Data is fetched once on instantiation and once on get_data()
        self.assertEqual(len(api_calls), 2)

        api_call = api_calls[0]
        self.assertEqual(api_call.request.method, "GET")
        self.assertUrlsEqual(api_call.request.url, request_url)

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
        auth_data = load_fixture("auth_success.json")

        bad_session_id = "my-bad-session"
        good_session_id = auth_data.get("SessionId")
        api = NuHeat(None, None, session_id=bad_session_id)
        responses.add(
            responses.GET,
            f"{api._api_url}/thermostat",
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )

        serial_number = response_data.get("SerialNumber")
        thermostat = NuHeatThermostat(api, serial_number)

        # A later, second request throws 401 Unauthorized
        responses.add(
            responses.GET,
            thermostat._url,
            status=401
        )

        # Attempt to reauthenticate
        responses.add(
            responses.POST,
            api._auth_url,
            status=200,
            body=json.dumps(auth_data),
            content_type="application/json"
        )

        # Third request is successful
        responses.add(
            responses.GET,
            thermostat._url,
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )

        thermostat.get_data()
        self.assertTrue(isinstance(thermostat, NuHeatThermostat))

        api_calls = responses.calls
        self.assertEqual(len(api_calls), 4)

        unauthorized_attempt = api_calls[1]
        params = {"sessionid": bad_session_id, "serialnumber": serial_number}
        request_url = "{}?{}".format(
            thermostat._url,
            urlencode(params),
        )
        self.assertEqual(unauthorized_attempt.request.method, "GET")
        self.assertUrlsEqual(unauthorized_attempt.request.url, request_url)
        self.assertEqual(unauthorized_attempt.response.status_code, 401)

        auth_call = api_calls[2]
        self.assertEqual(auth_call.request.method, "POST")
        self.assertUrlsEqual(
            auth_call.request.url,
            api._auth_url,
        )

        second_attempt = api_calls[3]
        params["sessionid"] = good_session_id
        request_url = "{}?{}".format(
            thermostat._url,
            urlencode(params),
        )
        self.assertEqual(second_attempt.request.method, "GET")
        self.assertUrlsEqual(second_attempt.request.url, request_url)
        self.assertEqual(second_attempt.response.status_code, 200)

    @patch("nuheat.NuHeatThermostat.get_data")
    def test_schedule_mode(self, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat._schedule_mode = 1
        self.assertEqual(thermostat.schedule_mode, 1)

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_data")
    def test_schedule_mode_setter(self, set_data, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.schedule_mode = 2
        set_data.assert_called_with({"ScheduleMode": 2})

        # Invalid mode
        with self.assertRaises(Exception) as _:
            thermostat.schedule_mode = 5

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_data")
    def test_resume_schedule(self, set_data, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.resume_schedule()
        set_data.assert_called_with({"ScheduleMode": config.SCHEDULE_RUN})

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_target_temperature")
    def test_set_target_fahrenheit(self, set_target_temperature, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.set_target_fahrenheit(80)
        set_target_temperature.assert_called_with(2665, config.SCHEDULE_HOLD, None)

        thermostat = NuHeatThermostat(None, None)
        thermostat.set_target_fahrenheit(80, config.SCHEDULE_TEMPORARY_HOLD)
        set_target_temperature.assert_called_with(2665, config.SCHEDULE_TEMPORARY_HOLD, None)

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_target_temperature")
    def test_set_target_celsius(self, set_target_temperature, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.set_target_celsius(26)
        set_target_temperature.assert_called_with(2609, config.SCHEDULE_HOLD, None)

        thermostat = NuHeatThermostat(None, None)
        thermostat.set_target_celsius(26, config.SCHEDULE_TEMPORARY_HOLD)
        set_target_temperature.assert_called_with(2609, config.SCHEDULE_TEMPORARY_HOLD, None)

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

        self.assertEqual(thermostat.hold_time, None)

        # Temporary hold - no schedule, no hold time from server
        thermostat.set_target_temperature(2222, mode=config.SCHEDULE_TEMPORARY_HOLD)
        set_data.assert_called_with({
            "SetPointTemp": 2222,
            "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD
        })

        # Temporary hold - no schedule, server HoldSetPointDateTime available
        # Battle of Lexington and Concord
        est = timezone(timedelta(hours=-5), 'EST')
        thermostat.schedule_mode = config.SCHEDULE_RUN
        thermostat._hold_time = datetime(1775, 4, 19, 5, 0, tzinfo=est)
        thermostat.set_target_temperature(2223, mode=config.SCHEDULE_TEMPORARY_HOLD)
        set_data.assert_called_with({
            "SetPointTemp": 2223,
            "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD,
            "HoldSetPointDateTime": "Wed, 19 Apr 1775 10:00:00 GMT"
        })

        # Temporary hold - time specified
        # Attack on Fort Sumter
        hold_time = datetime(1861, 4, 12, 4, 30, tzinfo=est)
        thermostat.set_target_temperature(2224, mode=config.SCHEDULE_TEMPORARY_HOLD, hold_time=hold_time)
        set_data.assert_called_with({
            "SetPointTemp": 2224,
            "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD,
            "HoldSetPointDateTime": "Fri, 12 Apr 1861 09:30:00 GMT"
        })

        # Simulate effect of calling get_data after setting temporary hold
        thermostat._schedule_mode = config.SCHEDULE_TEMPORARY_HOLD
        thermostat._hold_time = datetime.fromisoformat("1861-04-12T09:30:00+00:00")
        self.assertEqual(thermostat.hold_time, thermostat._hold_time)

        # Temporary hold - use previous hold time
        # Attack on Fort Sumter
        thermostat.set_target_temperature(2225, mode=config.SCHEDULE_TEMPORARY_HOLD)
        set_data.assert_called_with({
            "SetPointTemp": 2225,
            "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD,
            "HoldSetPointDateTime": "Fri, 12 Apr 1861 09:30:00 GMT"
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

        # Invalid mode
        with self.assertRaises(Exception) as _:
            thermostat.set_target_temperature(2222, 5)

    @patch("nuheat.NuHeatThermostat.get_data")
    @patch("nuheat.NuHeatThermostat.set_data")
    def test_hold_time_setter(self, set_data, _):
        thermostat = NuHeatThermostat(None, None)
        thermostat.min_temperature = 500
        thermostat.max_temperature = 7000

        # Battle of Gettysburg
        est = timezone(timedelta(hours=-5), 'EST')
        hold_time = datetime(1863, 7, 1, 7, 30, tzinfo=est)
        with self.assertRaises(Exception) as _:
            # Invalid hold_time - must be in the future.
            thermostat.hold_time = hold_time

        # 6 hours from now
        hold_time = datetime.now(timezone.utc) + timedelta(hours=+6)
        hold_str = hold_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        thermostat.hold_time = hold_time
        set_data.assert_called_with({
            "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD,
            "HoldSetPointDateTime": hold_str
        })

    @responses.activate
    def test_next_schedule_event(self):
        # Use thermostat.json to load a schedule into thermostat
        response_data = load_fixture("thermostat.json")

        api = NuHeat(None, None, session_id="my-session")
        responses.add(
            responses.GET,
            f"{api._api_url}/thermostat",
            status=200,
            body=json.dumps(response_data),
            content_type="application/json"
        )

        serial_number = response_data.get("SerialNumber")
        thermostat = NuHeatThermostat(api, serial_number)
        thermostat.get_data()

        # Does anybody really know what time it is?
        with patch("nuheat.thermostat.datetime", wraps=datetime) as mock_dt:
            # Monday @ 11:00am (WW1 Armistice)
            wet = timezone(timedelta(hours=+1), 'WET')
            thermostat._data["TZOffset"] = "+01:00"
            mock_dt.now.return_value = datetime(1918, 11, 11, 11, 0, tzinfo=wet)
            next_event = thermostat.next_schedule_event
            # next_event = 9:30pm, same day
            self.assertEqual(next_event.get("Time"),
                             datetime(1918, 11, 11, 21, 30, tzinfo=wet))
            self.assertEqual(next_event.get("NuheatTemperature"), 2666)

            # Monday @ 02:41am (VE Day, first signing)
            wemt = timezone(timedelta(hours=+2), 'WEMT')
            thermostat._data["TZOffset"] = "+02:00"
            mock_dt.now.return_value = datetime(1945, 5, 7, 2, 41, tzinfo=wemt)
            # next_event = Monday @ 5:45am
            next_event = thermostat.next_schedule_event
            self.assertEqual(next_event.get("Time"),
                             datetime(1945, 5, 7, 5, 45, tzinfo=wemt))
            self.assertEqual(next_event.get("NuheatTemperature"), 2666)

            # Change Sunday "sleep" time to 3am
            thermostat._data["Schedules"][6]["Events"][3]["Clock"] = "03:00:00"
            # next_event = Monday @ 3:00am
            next_event = thermostat.next_schedule_event
            self.assertEqual(next_event.get("Time"),
                             datetime(1945, 5, 7, 3, 0, tzinfo=wemt))
            self.assertEqual(next_event.get("NuheatTemperature"), 2333)

            # Friday @ 10:45pm (Fall of Berlin Wall)
            cet = timezone(timedelta(hours=+1), 'CET')
            thermostat._data["TZOffset"] = "+01:00"
            mock_dt.now.return_value = datetime(1990, 11, 9, 22, 45, tzinfo=cet)
            # next_event = Midnight Friday night / Saturday morning
            next_event = thermostat.next_schedule_event
            self.assertEqual(next_event.get("Time"),
                             datetime(1990, 11, 10, 0, 0, tzinfo=cet))
            self.assertEqual(next_event.get("NuheatTemperature"), 2222)

            # Disable Friday's "sleep" event
            thermostat._data["Schedules"][4]["Events"][3]["Active"] = False
            # next_event = 8am Saturday morning
            next_event = thermostat.next_schedule_event
            self.assertEqual(next_event.get("Time"),
                             datetime(1990, 11, 10, 8, 0, tzinfo=cet))
            self.assertEqual(next_event.get("NuheatTemperature"), 2666)

            # Simulate thermostat and python-nuheat in different timezones
            # Thermostat in GMT (schedule becomes relative to there)
            thermostat._data["TZOffset"] = "+00:00"
            # next_event = 9am Saturday morning
            next_event = thermostat.next_schedule_event
            next_event["Time"] = next_event["Time"].astimezone(cet)
            self.assertEqual(next_event.get("Time"),
                             datetime(1990, 11, 10, 9, 0, tzinfo=cet))
            self.assertEqual(next_event.get("NuheatTemperature"), 2666)

            # Thermostat in Auckland, NZ (where time is 10:45am Saturday)
            thermostat._data["TZOffset"] = "+13:00"
            nzdt = timezone(timedelta(hours=+13), 'NZDT')
            # next_event = 10pm Saturday evening in Auckland
            next_event = thermostat.next_schedule_event
            next_event["Time"] = next_event["Time"].astimezone(nzdt)
            self.assertEqual(next_event.get("Time"),
                             datetime(1990, 11, 10, 22, 0, tzinfo=nzdt))
            self.assertEqual(next_event.get("NuheatTemperature"), 2666)

    @responses.activate
    @patch("nuheat.NuHeatThermostat.set_data")
    def test_set_target_temperature_temporary_hold_time(self, set_data):
        response_data = load_fixture("thermostat.json")
        api = NuHeat(None, None, session_id="my-session")
        serial_number = response_data.get("SerialNumber")

        with patch("nuheat.thermostat.datetime", wraps=datetime) as mock_dt:
            responses.add(
                responses.GET,
                f"{api._api_url}/thermostat",
                status=200,
                body=json.dumps(response_data),
                content_type="application/json"
            )
            thermostat = NuHeatThermostat(api, serial_number)
            thermostat.get_data()

            cet = timezone(timedelta(hours=+1), 'CET')
            thermostat._data["TZOffset"] = "+01:00"
            mock_dt.now.return_value = datetime(1990, 11, 9, 22, 45, tzinfo=cet)
            thermostat.set_target_temperature(2222,
                                              config.SCHEDULE_TEMPORARY_HOLD)
            set_data.assert_called_with({
                "SetPointTemp": 2222,
                "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD,
                "HoldSetPointDateTime": "Fri, 09 Nov 1990 23:00:00 GMT"
            })

    @responses.activate
    @patch("nuheat.NuHeatThermostat.get_data")
    def test_set_data(self, _):
        api = NuHeat(None, None, session_id="my-session")

        responses.add(
            responses.POST,
            f"{api._api_url}/thermostat",
            status=200,
            content_type="application/json"
        )

        serial_number = "my-thermostat"
        thermostat = NuHeatThermostat(api, serial_number)

        params = {
            "sessionid": api._session_id,
            "serialnumber": serial_number
        }
        request_url = "{}?{}".format(
            thermostat._url,
            urlencode(params),
        )
        post_data = {"test": "data"}
        thermostat.set_data(post_data)

        api_call = responses.calls[0]
        self.assertEqual(api_call.request.method, "POST")
        self.assertUrlsEqual(api_call.request.url, request_url)
        self.assertEqual(api_call.request.body, urlencode(post_data))
