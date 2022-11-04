# Python NuHeat

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nuheat?style=flat-square)
![PyPI - Version](https://img.shields.io/pypi/v/nuheat?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nuheat?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/broox/python-nuheat/Python%20package?style=flat-square)
![Coveralls](https://img.shields.io/coveralls/github/broox/python-nuheat?style=flat-square)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/broox/python-nuheat?style=flat-square)

A Python 3 library that allows control of connected [NuHeat Signature](http://www.nuheat.com/products/thermostats/signature-thermostat) radiant floor thermostats.

* This uses the web-based NuHeat API, so it requires an external internet connection
* The API in use is not an officially published API, so it could change without notice
* Please contribute!

# Installation

```shell
$ pip install nuheat
```

# Usage

```python
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

# Set a new temperature and permanently hold
# Note: Any pre-programmed thermostat schedules will be ignored until you resume the schedule or
# change the mode.
thermostat.set_target_fahrenheit(72)

# If you prefer celsius...
thermostat.set_target_celsius(22)

# You can also do this via the convenience property setters
thermostat.target_fahrenheit = 72

# or with celsius
thermostat.target_celsius = 22

# To resume the schedule programmed into the thermostat
thermostat.resume_schedule()

# Which is effectively the same as explicitly changing the mode like so
thermostat.schedule_mode = 1

# To set a new target temperature with an explicit schedule mode
thermostat.set_target_fahrenheit(72, mode=2)

# If you prefer celsius, you can use that too
thermostat.set_target_celsius(22, mode=2)

# Set a target temperature until a specified datetime
# Note: A timezone aware datetime should be passed in, otherwise UTC will be assumed
from datetime import datetime, timedelta, timezone
hold_time = datetime.now() + timedelta(hours=4)
thermostat.set_target_fahrenheit(69, mode=2, hold_time=hold_time)
```

# Contributing

Pull requests are always welcome!

## Running locally with Docker

```shell
# Build and run the docker container:
$ docker build -t python-nuheat .
$ docker run -it --rm -v $(pwd):/python-nuheat python-nuheat

# To run the interactive shell:
$ ipython

# To run tests:
$ pytest
```
