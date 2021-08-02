BRANDS = ("NUHEAT", "MAPEHEAT")
HOSTNAMES = {
    "NUHEAT": "mynuheat.com",
    "MAPEHEAT": "mymapeheat.com",
}
API_URL = "https://{HOSTNAME}/api"

AUTH_URL = "{API_URL}/authenticate/user"
THERMOSTAT_URL = "{API_URL}/thermostat"

# NuHeat Schedule Modes
SCHEDULE_RUN = 1
SCHEDULE_TEMPORARY_HOLD = 2  # hold the target temperature until the next scheduled program
SCHEDULE_HOLD = 3  # hold the target temperature until it is manually changed
