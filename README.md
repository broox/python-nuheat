# Python NuHeat

[![PyPi](https://badge.fury.io/py/nuheat.svg)](https://badge.fury.io/py/nuheat)
[![Travis](https://travis-ci.org/broox/python-nuheat.svg?branch=master)](https://travis-ci.org/broox/python-nuheat)
[![Coveralls](https://coveralls.io/repos/github/broox/python-nuheat/badge.svg?branch=master)](https://coveralls.io/github/broox/python-nuheat?branch=master)

A Python library that allows control of connected [NuHeat Signature](http://www.nuheat.com/products/thermostats/signature-thermostat) radiant floor thermostats.

* This uses the web-based NuHeat API, so it requires an external internet connection
* The API in use is not an officially published API, so it could change without notice
* Please contribute!

# Usage

```
from nuheat import NuHeat

# Initalize an API session with your login credentials
api = NuHeat("email@example.com", "your-secure-password")
api.authenticate()

# Fetch a thermostat by serial number / ID. This can be found on the NuHeat website by selecting
# your thermostat and noting the Thermostat ID
thermostat = api.get_thermostat("12345")

# Print the current temperature of the thermostat
thermostat.fahrenheit
thermostat.celsius

# Print the current target temperature of the thermostat
thermostat.target_fahrenheit
thermostat.target_celsius

# Set a new target temperature to turn the heat on/off. This is effectively a set and HOLD command,
# so any pre-programmed thermostat schedules will be ignored.
thermostat.target_fahrenheit = 75

# If you prefer celsius you can do that too
thermostat.target_celsius = 23

# Resume the schedule programmed into the thermostat
thermostat.resume_schedule()
```