# Python NuHeat

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nuheat?style=flat-square)](https://pypi.org/project/nuheat/)
[![PyPI - Version](https://img.shields.io/pypi/v/nuheat?style=flat-square)](https://pypi.org/project/nuheat/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/nuheat?style=flat-square)](https://pypi.org/project/nuheat/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/broox/python-nuheat/test.yaml?branch=master&style=flat-square)](https://github.com/broox/python-nuheat/actions?query=branch%3Amaster)
[![Coveralls](https://img.shields.io/coveralls/github/broox/python-nuheat?style=flat-square)](https://coveralls.io/github/broox/python-nuheat?branch=master)

> [!WARNING]
> **This library no longer works and is deprecated.**
>
> In 2026, Chemelex (the maker of NuHeat) retired the legacy `www.mynuheat.com/api` used here, along with the old
> Signature app and website. Signature thermostats moved to the NUHEAT Conductor app and a new OAuth2-based API,
> so requests from this library now time out.
>
> - **Home Assistant users:** the core `nuheat` integration is being moved to the new API. Follow
>   [home-assistant/core#175923](https://github.com/home-assistant/core/issues/175923) for status.
> - **Python users:** use [`chemelex-nuheat`](https://pypi.org/project/chemelex-nuheat/), which targets the new API.
>
> Version 1.2.0 is the final release. It warns on use and raises a clear `NuHeatError` instead of hanging.
> The documentation below describes the legacy API and is kept for reference only.

A Python 3 library that allows control of connected [NuHeat Signature](http://www.nuheat.com/products/thermostats/signature-thermostat) radiant floor thermostats.

This also supports the **Mapei MapeHeat** line of smart thermostats.

* This uses the legacy web-based NuHeat API (now retired; see above)
* The API in use was never an officially published API

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

# Initialize an API session for a specific brand
api = NuHeat("email@example.com", "your-secure-password", brand="MAPEHEAT")
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

# Development

This project is no longer maintained. To run the tests locally:

```shell
$ pip install -e ".[dev]"
$ ruff check .
$ pytest
```

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
