NUHEAT = "NUHEAT"
MAPEHEAT = "MAPEHEAT"
BRANDS = (NUHEAT, MAPEHEAT)
HOSTNAMES = {
    NUHEAT: "www.mynuheat.com",
    MAPEHEAT: "www.mymapeheat.com",
}

# NuHeat Schedule Modes
SCHEDULE_RUN = 1
SCHEDULE_TEMPORARY_HOLD = 2  # hold the target temperature until the next scheduled program
SCHEDULE_HOLD = 3  # hold the target temperature until it is manually changed

# Default requests timeout: (connect, read) seconds
DEFAULT_TIMEOUT = (10, 30)

DEPRECATION_MESSAGE = (
    "The legacy NuHeat/Mapeheat API used by python-nuheat (www.mynuheat.com/api) was retired by "
    "Chemelex in 2026 and no longer responds. This library is deprecated. Use the chemelex-nuheat "
    "package or Home Assistant's updated NuHeat integration instead. "
    "See https://github.com/home-assistant/core/issues/175923"
)
