from dataclasses import dataclass
from datetime import datetime, timezone, timedelta, time, date
from typing import Optional
import nuheat.config as config
from nuheat.util import (
    celsius_to_nuheat,
    fahrenheit_to_nuheat,
    nuheat_to_celsius,
    nuheat_to_fahrenheit
)


@dataclass
class HourlyUsage:
    """Hourly energy usage data."""

    hour: int
    heating_minutes: int
    energy_kwh: Optional[float]


@dataclass
class DailyUsage:
    """Daily energy usage data."""

    date: date
    heating_minutes: int
    energy_kwh: Optional[float]


@dataclass
class EnergyUsage:
    """Energy usage data from the NuHeat API (daily view with hourly breakdown)."""

    date: date
    heating_minutes: int
    energy_kwh: Optional[float]
    hourly: list


@dataclass
class WeeklyUsage:
    """Weekly energy usage data from the NuHeat API (weekly view with daily breakdown)."""

    week_start: date
    heating_minutes: int
    energy_kwh: Optional[float]
    daily: list


@dataclass
class MonthlyUsage:
    """Monthly energy usage data."""

    year: int
    month: int
    heating_minutes: int
    energy_kwh: Optional[float]


@dataclass
class YearlyUsage:
    """Yearly energy usage data from the NuHeat API (yearly view with monthly breakdown)."""

    year: int
    heating_minutes: int
    energy_kwh: Optional[float]
    monthly: list


class NuHeatThermostat(object):
    _session = None
    _data = None
    _schedule_mode = None
    _hold_time = None

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
    def _url(self):
        return f"{self._session._api_url}/thermostat"

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
        data = self._session.request(
            url=self._url,
            params=params,
        )

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
        hold_time_str = data.get("HoldSetPointDateTime")
        self._hold_time = datetime.fromisoformat(hold_time_str)

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

    @property
    def hold_time(self):
        """
        Return a datetime for the current temporary hold time (or None)
        """
        if self._schedule_mode == config.SCHEDULE_TEMPORARY_HOLD:
            return self._hold_time
        else:
            return None

    @hold_time.setter
    def hold_time(self, hold):
        """
        Set a temporary hold time (and change schedule_mode to Temporary Hold).

        :param hold: datetime for temporary hold_time.
        """
        hold_gmt = hold.astimezone(timezone(timedelta(0), 'GMT'))

        if hold_gmt < datetime.now(timezone.utc):
            raise Exception("Invalid hold_time - must be in the future.")

        hold_str = hold_gmt.strftime("%a, %d %b %Y %H:%M:%S %Z")
        post_data = {
            "ScheduleMode": config.SCHEDULE_TEMPORARY_HOLD,
            "HoldSetPointDateTime": hold_str
        }
        self.set_data(post_data)

    @property
    def next_schedule_event(self):
        """
        Return dictionary containing information about the next scheduled
        event.
        """
        if self._data is None:
            return None

        # Get thermostat's timezone from server data
        tstat_tzs = self._data.get("TZOffset", "")
        tstat_tz = time.fromisoformat("00:00:00" + tstat_tzs).tzinfo

        # Convert now to thermostat's timezone, so day/next_day will be right
        now = datetime.now().astimezone(tstat_tz)

        # Find the first active event in the next week that is after now.
        # Note: We start with yesterday (-1), in case yesterday's "Sleep" time
        # is set for today.
        for add_days in range(-1, 8):
            day = now.date() + timedelta(days=add_days)
            next_day = day + timedelta(days=1)
            dayofweek = day.weekday()
            for event in self._data.get("Schedules")[dayofweek].get("Events"):
                # Times in thermostat schedule are relative to TZOffset
                event_time = time.fromisoformat(event.get("Clock") + tstat_tzs)
                if (event.get("ScheduleType") == 3 and event_time <= time(3, 0, 0, 0, tstat_tz)):
                    # Special case: Thermostat schedule will accept times
                    # between midnight and 3am for the "Sleep" time.  These
                    # actually occur on the following day, based on empirical
                    # testing.
                    event_dt = datetime.combine(next_day, event_time)
                else:
                    event_dt = datetime.combine(day, event_time)
                if event.get("Active") and (now < event_dt):
                    # Convert back to local time before returning result
                    event_dt = event_dt.astimezone(datetime.now().tzinfo)
                    temp_floor = event.get("TempFloor")
                    return {"Time": event_dt, "NuheatTemperature": temp_floor}

        # Can't find an active event.
        return None

    def resume_schedule(self):
        """
        A convenience method to tell NuHeat to resume its programmed schedule
        """
        self.schedule_mode = config.SCHEDULE_RUN

    def set_target_fahrenheit(self, fahrenheit, mode=config.SCHEDULE_HOLD, hold_time=None):
        """
        Set the target temperature to the desired fahrenheit, with more granular control of the
        hold mode

        :param fahrenheit: The desired temperature in F
        :param mode: The desired mode to operate in
        :param hold_time: datetime object for Temporary Hold.  If None, the schedule will
                          resume at the next programmed event or previously-set hold time.
        """
        temperature = fahrenheit_to_nuheat(fahrenheit)
        self.set_target_temperature(temperature, mode, hold_time)

    def set_target_celsius(self, celsius, mode=config.SCHEDULE_HOLD, hold_time=None):
        """
        Set the target temperature to the desired celsius, with more granular control of the hold
        mode

        :param celsius: The desired temperature in C
        :param mode: The desired mode to operate in
        :param hold_time: datetime object for Temporary Hold.  If None, the schedule will
                          resume at the next programmed event or previously-set hold time.
        """
        temperature = celsius_to_nuheat(celsius)
        self.set_target_temperature(temperature, mode, hold_time)

    def set_target_temperature(self, temperature, mode=config.SCHEDULE_HOLD, hold_time=None):
        """
        Updates the target temperature on the NuHeat API

        :param temperature: The desired temperature in NuHeat format
        :param mode: The desired mode to operate in
        :param hold_time: datetime object for Temporary Hold.  If None, the schedule will
                          resume at the next programmed event or previously-set hold time.
        """
        if temperature < self.min_temperature:
            temperature = self.min_temperature

        if temperature > self.max_temperature:
            temperature = self.max_temperature

        modes = [config.SCHEDULE_TEMPORARY_HOLD, config.SCHEDULE_HOLD]
        if mode not in modes:
            raise Exception("Invalid mode. Please use one of: {}".format(modes))

        post_data = {
            "SetPointTemp": temperature,
            "ScheduleMode": mode
        }

        if mode == config.SCHEDULE_TEMPORARY_HOLD:
            if hold_time is None:
                # Use previously set hold_time if already in temporary hold.
                hold_time = self.hold_time

            if hold_time is None:
                # Hold until next scheduled event if we can determine it.
                event = self.next_schedule_event
                if event is not None:
                    hold_time = event.get("Time")

            if hold_time is None:
                # Still don't have a hold time to use; use time from server.
                # Note: This doesn't always work as expected.  For example, if
                # a temporary hold was set, then cleared, the server will give
                # us a HoldSetPointDateTime equal to the cleared temporary
                # hold time instead of the next scheduled event.
                hold_time = self._hold_time

            if hold_time is not None:
                hold_gmt = hold_time.astimezone(timezone(timedelta(0), 'GMT'))
                hold_str = hold_gmt.strftime("%a, %d %b %Y %H:%M:%S %Z")
                post_data["HoldSetPointDateTime"] = hold_str

        self.set_data(post_data)

    def set_data(self, post_data):
        """
        Update (patch) the current instance's data on the NuHeat API
        """
        params = {
            "serialnumber": self.serial_number
        }
        self._session.request(
            url=self._url,
            method="POST",
            data=post_data,
            params=params,
        )

    def get_energy_usage(self, for_date: Optional[date] = None) -> EnergyUsage:
        """
        Fetch energy usage data for a specific date.

        :param for_date: The date to fetch energy usage for. Defaults to today.
        :return: EnergyUsage object containing heating minutes and energy in kWh
        """
        if for_date is None:
            for_date = date.today()

        date_str = for_date.strftime("%Y-%m-%d")

        params = {
            "serialnumber": self.serial_number,
            "view": "day",
            "date": date_str,
            "history": "0",
            "calc": "yes",
            "weekstart": "sunday",
        }

        data = self._session.request(
            url=f"{self._session._api_url}/energyusage",
            params=params,
        )

        total_minutes = 0
        total_kwh = 0.0
        has_kwh = False
        hourly_data = []

        # Response format: {"EnergyUsage": [{"Usage": [{"Minutes": x, "EnergyKWattHour": y}, ...]}]}
        energy_usage = data.get("EnergyUsage", [])
        for day_data in energy_usage:
            usage_entries = day_data.get("Usage", [])
            for hour, entry in enumerate(usage_entries):
                minutes = entry.get("Minutes", 0)
                kwh = entry.get("EnergyKWattHour", 0)

                total_minutes += minutes
                if kwh > 0:
                    has_kwh = True
                    total_kwh += kwh

                hourly_data.append(HourlyUsage(
                    hour=hour,
                    heating_minutes=minutes,
                    energy_kwh=kwh if kwh > 0 else None,
                ))

        # If we have heating minutes but no kWh data, return None (user hasn't
        # configured watt density in NuHeat app). If heating minutes is 0,
        # return 0.0 since zero heating = zero energy.
        if total_minutes == 0:
            final_kwh: Optional[float] = 0.0
        elif has_kwh:
            final_kwh = total_kwh
        else:
            final_kwh = None

        return EnergyUsage(
            date=for_date,
            heating_minutes=total_minutes,
            energy_kwh=final_kwh,
            hourly=hourly_data,
        )

    def get_weekly_usage(self, for_date: Optional[date] = None) -> WeeklyUsage:
        """
        Fetch weekly energy usage data with daily breakdown.

        :param for_date: A date within the week to fetch. Defaults to today.
        :return: WeeklyUsage object containing daily breakdown
        """
        if for_date is None:
            for_date = date.today()

        date_str = for_date.strftime("%Y-%m-%d")

        params = {
            "serialnumber": self.serial_number,
            "view": "week",
            "date": date_str,
            "history": "0",
            "calc": "yes",
            "weekstart": "sunday",
        }

        data = self._session.request(
            url=f"{self._session._api_url}/energyusage",
            params=params,
        )

        total_minutes = 0
        total_kwh = 0.0
        has_kwh = False
        daily_data = []

        # Determine week start based on API response
        monday_first = data.get("MondayIsFirstDay", False)

        # Calculate the start of the week containing for_date
        weekday = for_date.weekday()  # Monday=0, Sunday=6
        if monday_first:
            days_since_start = weekday
        else:
            # Sunday=0 for week start
            days_since_start = (weekday + 1) % 7
        week_start = for_date - timedelta(days=days_since_start)

        # Response format: {"EnergyUsage": [{"Usage": [{"Minutes": x, "EnergyKWattHour": y}, ...]}]}
        energy_usage = data.get("EnergyUsage", [])
        for day_data in energy_usage:
            usage_entries = day_data.get("Usage", [])
            for day_offset, entry in enumerate(usage_entries):
                minutes = entry.get("Minutes", 0)
                kwh = entry.get("EnergyKWattHour", 0)

                total_minutes += minutes
                if kwh > 0:
                    has_kwh = True
                    total_kwh += kwh

                entry_date = week_start + timedelta(days=day_offset)
                daily_data.append(DailyUsage(
                    date=entry_date,
                    heating_minutes=minutes,
                    energy_kwh=kwh if kwh > 0 else None,
                ))

        # If we have heating minutes but no kWh data, return None (user hasn't
        # configured watt density in NuHeat app). If heating minutes is 0,
        # return 0.0 since zero heating = zero energy.
        if total_minutes == 0:
            final_kwh: Optional[float] = 0.0
        elif has_kwh:
            final_kwh = total_kwh
        else:
            final_kwh = None

        return WeeklyUsage(
            week_start=week_start,
            heating_minutes=total_minutes,
            energy_kwh=final_kwh,
            daily=daily_data,
        )

    def get_yearly_usage(self, year: Optional[int] = None) -> YearlyUsage:
        """
        Fetch yearly energy usage data with monthly breakdown.

        :param year: The year to fetch. Defaults to current year.
        :return: YearlyUsage object containing monthly breakdown
        """
        if year is None:
            year = date.today().year

        params = {
            "serialnumber": self.serial_number,
            "view": "year",
            "date": str(year),
            "history": "0",
            "calc": "yes",
            "weekstart": "sunday",
        }

        data = self._session.request(
            url=f"{self._session._api_url}/energyusage",
            params=params,
        )

        total_minutes = 0
        total_kwh = 0.0
        has_kwh = False
        monthly_data = []

        # Response format: {"EnergyUsage": [{"Usage": [{"Minutes": x, "EnergyKWattHour": y}, ...]}]}
        # 12 entries, one per month (January=0 to December=11)
        energy_usage = data.get("EnergyUsage", [])
        for year_data in energy_usage:
            usage_entries = year_data.get("Usage", [])
            for month_index, entry in enumerate(usage_entries):
                minutes = entry.get("Minutes", 0)
                kwh = entry.get("EnergyKWattHour", 0)

                total_minutes += minutes
                if kwh > 0:
                    has_kwh = True
                    total_kwh += kwh

                monthly_data.append(MonthlyUsage(
                    year=year,
                    month=month_index + 1,  # 1-12
                    heating_minutes=minutes,
                    energy_kwh=kwh if kwh > 0 else None,
                ))

        # If we have heating minutes but no kWh data, return None (user hasn't
        # configured watt density in NuHeat app). If heating minutes is 0,
        # return 0.0 since zero heating = zero energy.
        if total_minutes == 0:
            final_kwh: Optional[float] = 0.0
        elif has_kwh:
            final_kwh = total_kwh
        else:
            final_kwh = None

        return YearlyUsage(
            year=year,
            heating_minutes=total_minutes,
            energy_kwh=final_kwh,
            monthly=monthly_data,
        )
