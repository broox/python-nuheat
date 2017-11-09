from decimal import Decimal, ROUND_HALF_UP

def round_half(number):
    """
    Python's round() function behaves differently in Python 2 and 3
    This method makes it consistent.

    :param number: The number to round
    """
    return Decimal(number).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit to Celsius

    :param fahrenheit: The temperature to convert to Celsius
    """
    return int(round_half((fahrenheit - 32) / 1.8))


def fahrenheit_to_nuheat(fahrenheit):
    """
    Convert Fahrenheit to a temperature value that NuHeat understands
    Formula f(x) = ((x - 33) * 56) + 33

    :param fahrenheit: The temperature to convert to NuHeat
    """
    return int(round_half(((fahrenheit - 33) * 56) + 33))


def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit

    :param celsius: The temperature to convert to Fahrenheit
    """
    return int(round_half(celsius * 1.8 + 32))


def celsius_to_nuheat(celsius):
    """
    Convert Celsius to a temperature value that NuHeat understands
    Formula f(x) = ((x - 33) * 56) + 33

    :param celsius: The temperature to convert to NuHeat
    """
    fahrenheit = celsius_to_fahrenheit(celsius)
    return int(round_half(((fahrenheit - 33) * 56) + 33))

def nuheat_to_fahrenheit(nuheat_temperature):
    """
    Convert the NuHeat temp value to Fahrenheit
    Formula f(x) = ((x - 33) / 56) + 33

    :param nuheat_temperature: The temperature to convert to Fahrenheit
    """
    return int(round_half(((nuheat_temperature - 33) / 56.0) + 33))


def nuheat_to_celsius(nuheat_temperature):
    """
    Convert the NuHeat temp value to Celsius

    :param nuheat_temperature: The temperature to convert to Celsius
    """
    fahrenheit = nuheat_to_fahrenheit(nuheat_temperature)
    return fahrenheit_to_celsius(fahrenheit)
