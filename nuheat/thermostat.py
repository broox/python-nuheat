import nuheat.config as config
from nuheat.util import (
    celsius_to_nuheat,
    fahrenheit_to_nuheat,
    nuheat_to_celsius,
    nuheat_to_fahrenheit
)


class NuHeatThermostat(object):
    _session = None
    _data = None
    _schedule_mode = None

    heating = False
    online = False
    room = None
    serial_number = None
    temperature = None
    min_temperature = None
    max_temperature = None
    target_temperature = None

    def __init__(self, nuheat_session, serial_number):
        """
        Initialize a local Thermostat object with the data returned from NuHeat
        """
        self._session = nuheat_session
        self.serial_number = serial_number
        self.get_data()

    def __repr__(self):
        return "<NuHeatThermostat id='{}' temperature='{}F / {}C' target='{}F / {}C'>".format(
            self.serial_number,
            self.fahrenheit,
            self.celsius,
            self.target_fahrenheit,
            self.target_celsius
        )

    @property
    def fahrenheit(self):
        """
        Return the current temperature in Fahrenheit
        """
        if not self.temperature:
            return None
        return nuheat_to_fahrenheit(self.temperature)

    @property
    def celsius(self):
        """
        Return the current temperature in Celsius
        """
        if not self.temperature:
            return None
        return nuheat_to_celsius(self.temperature)

    @property
    def min_fahrenheit(self):
        """
        Return the thermostat's minimum temperature in Fahrenheit
        """
        if not self.min_temperature:
            return None
        return nuheat_to_fahrenheit(self.min_temperature)

    @property
    def min_celsius(self):
        """
        Return the thermostat's minimum temperature in Celsius
        """
        if not self.min_temperature:
            return None
        return nuheat_to_celsius(self.min_temperature)

    @property
    def max_fahrenheit(self):
        """
        Return the thermostat's maximum temperature in Fahrenheit
        """
        if not self.max_temperature:
            return None
        return nuheat_to_fahrenheit(self.max_temperature)

    @property
    def max_celsius(self):
        """
        Return the thermostat's maximum temperature in Celsius
        """
        if not self.max_temperature:
            return None
        return nuheat_to_celsius(self.max_temperature)

    @property
    def target_fahrenheit(self):
        """
        Return the current target temperature in Fahrenheit
        """
        if not self.target_temperature:
            return None
        return nuheat_to_fahrenheit(self.target_temperature)

    @property
    def target_celsius(self):
        """
        Return the current target temperature in Celsius
        """
        if not self.target_temperature:
            return None
        return nuheat_to_celsius(self.target_temperature)


    @target_fahrenheit.setter
    def target_fahrenheit(self, fahrenheit):
        """
        Helper to set and HOLD the target temperature to the desired fahrenheit

        :param fahrenheit: The desired temperature in F
        """
        self.set_target_fahrenheit(fahrenheit)

    @target_celsius.setter
    def target_celsius(self, celsius):
        """
        Helper to set and HOLD the target temperature to the desired fahrenheit

        :param celsius: The desired temperature in C
        """
        # Note: headers are diff
        self.set_target_celsius(celsius)

    def get_data(self):
        """
        Fetch/refresh the current instance's data from the NuHeat API
        """
        params = {
            "serialnumber": self.serial_number
        }
        data = self._session.request(config.THERMOSTAT_URL, params=params)

        self._data = data

        self.heating = data.get("Heating")
        self.online = data.get("Online")
        self.room = data.get("Room")
        self.serial_number = data.get("SerialNumber")
        self.temperature = data.get("Temperature")
        self.min_temperature = data.get("MinTemp")
        self.max_temperature = data.get("MaxTemp")
        self.target_temperature = data.get("SetPointTemp")
        self._schedule_mode = data.get("ScheduleMode")

    @property
    def schedule_mode(self):
        """
        Return the mode that the thermostat is currently using
        """
        return self._schedule_mode

    @schedule_mode.setter
    def schedule_mode(self, mode):
        """
        Set the thermostat mode

        :param mode: The desired mode integer value.
                     Auto = 1
                     Temporary hold = 2
                     Permanent hold = 3
        """
        modes = [config.SCHEDULE_RUN, config.SCHEDULE_TEMPORARY_HOLD, config.SCHEDULE_HOLD]
        if mode not in modes:
            raise Exception("Invalid mode. Please use one of: {}".format(modes))

        self.set_data({"ScheduleMode": mode})

    def resume_schedule(self):
        """
        A convenience method to tell NuHeat to resume its programmed schedule
        """
        self.schedule_mode = config.SCHEDULE_RUN

    def set_target_fahrenheit(self, fahrenheit, mode=config.SCHEDULE_HOLD):
        """
        Set the target temperature to the desired fahrenheit, with more granular control of the
        hold mode

        :param fahrenheit: The desired temperature in F
        :param mode: The desired mode to operate in
        """
        temperature = fahrenheit_to_nuheat(fahrenheit)
        self.set_target_temperature(temperature, mode)

    def set_target_celsius(self, celsius, mode=config.SCHEDULE_HOLD):
        """
        Set the target temperature to the desired celsius, with more granular control of the hold
        mode

        :param celsius: The desired temperature in C
        :param mode: The desired mode to operate in
        """
        temperature = celsius_to_nuheat(celsius)
        self.set_target_temperature(temperature, mode)

    def set_target_temperature(self, temperature, mode=config.SCHEDULE_HOLD):
        """
        Updates the target temperature on the NuHeat API

        :param temperature: The desired temperature in NuHeat format
        :param permanent: Permanently hold the temperature. If set to False, the schedule will
                          resume at the next programmed event
        """
        if temperature < self.min_temperature:
            temperature = self.min_temperature

        if temperature > self.max_temperature:
            temperature = self.max_temperature

        modes = [config.SCHEDULE_TEMPORARY_HOLD, config.SCHEDULE_HOLD]
        if mode not in modes:
            raise Exception("Invalid mode. Please use one of: {}".format(modes))

        self.set_data({
            "SetPointTemp": temperature,
            "ScheduleMode": mode
        })

    def set_data(self, post_data):
        """
        Update (patch) the current instance's data on the NuHeat API
        """
        params = {
            "serialnumber": self.serial_number
        }
        self._session.request(config.THERMOSTAT_URL, method="POST", data=post_data, params=params)
