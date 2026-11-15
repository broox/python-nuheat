class NuHeatError(Exception):
    """Base error for python-nuheat."""


class NuHeatAuthError(NuHeatError):
    """Authentication with the NuHeat API failed."""
