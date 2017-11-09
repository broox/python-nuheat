API_URL = "https://www.mynuheat.com/api"

AUTH_URL = API_URL + "/authenticate/user"
THERMOSTAT_URL = API_URL + "/thermostat"

REQUEST_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "Host": "mynuheat.com",
    "DNT": "1",
    "Origin": "https://mynuheat.com/api"
}

# NuHeat Schedule Modes
SCHEDULE_RUN = 1
SCHEDULE_TEMPORARY_HOLD = 2  # hold the target temperature until the next scheduled program
SCHEDULE_HOLD = 3  # hold the target temperature until it is manually changed
