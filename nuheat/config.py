NUHEAT = "NUHEAT"
MAPEHEAT = "MAPEHEAT"
BRANDS = (NUHEAT, MAPEHEAT)
HOSTNAMES = {
    NUHEAT: "mynuheat.com",
    MAPEHEAT: "mymapeheat.com",
}

# NuHeat Schedule Modes
SCHEDULE_RUN = 1
SCHEDULE_TEMPORARY_HOLD = 2  # hold the target temperature until the next scheduled program
SCHEDULE_HOLD = 3  # hold the target temperature until it is manually changed
