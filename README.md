# Python NuHeat

[![PyPI version](https://badge.fury.io/py/nuheat.svg)](https://badge.fury.io/py/nuheat)
[![Travis](https://travis-ci.org/broox/python-nuheat.svg?branch=master)](https://travis-ci.org/broox/python-nuheat)
[![Coveralls](https://coveralls.io/repos/github/broox/python-nuheat/badge.svg?branch=master&release=0.2.0)](https://coveralls.io/github/broox/python-nuheat?branch=master)
[![Supported Versions](https://img.shields.io/pypi/pyversions/nuheat.svg)](https://travis-ci.org/broox/python-nuheat)

A Python 2/Python 3 library that allows control of connected [NuHeat Signature](http://www.nuheat.com/products/thermostats/signature-thermostat) radiant floor thermostats.

* This uses the web-based NuHeat API, so it requires an external internet connection
* The API in use is not an officially published API, so it could change without notice
* Please contribute!

# Installation

```
$ pip install nuheat
```

# Usage

```
from nuheat import NuHeat

# Initalize an API session with your login credentials
api = NuHeat("email@example.com", "your-secure-password")
api.authenticate()

# Fetch a thermostat by serial number / ID. This can be found on the NuHeat website by selecting
# your thermostat and noting the Thermostat ID
thermostat = api.get_thermostat("12345")

# Get the current temperature of the thermostat
thermostat.fahrenheit
thermostat.celsius

# Get the current target temperature of the thermostat
thermostat.target_fahrenheit
thermostat.target_celsius

# Get the minimum and maximum temperatures supported by the thermostat
thermostat.min_fahrenheit
thermostat.max_fahrenheit
thermostat.min_celsius
thermostat.max_celsius

# Get the current mode of the thermostat
thermostat.schedule_mode

# The possible schedule modes are one of the following 3 integers:
# 1. Run the schedule programmed into the thermostat
# 2. Temporarily hold a target temperature until the next scheduled event
# 3. Permanently hold a target temperature until the mode is manually changed

# Get other properties
thermostat.heating
thermostat.online
thermostat.serial_number

# Set a new target temperature with an explicit mode
thermostat.set_target_fahrenheit(75, 2)

# If you prefer celsius, you can use that too
thermostat.set_target_celsius(23, 2)

# If you want a permanent HOLD, you can also use the convenience property setters instead.
# Note: Any pre-programmed thermostat schedules will be ignored until you resume the schedule or
# change the mode.
thermostat.target_fahrenheit = 75

# If you prefer celsius you can do that too
thermostat.target_celsius = 23

# Resume the schedule programmed into the thermostat
thermostat.resume_schedule()

# Which is effectively the same as explicitly changing the mode like so
thermostat.schedule_mode = 1
```