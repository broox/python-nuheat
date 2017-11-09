def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit to Celsius
    """
    return int(round((fahrenheit - 32) / 1.8))


def fahrenheit_to_nuheat(fahrenheit):
    """
    Convert Fahrenheit to a temperature value that NuHeat understands
    Formula f(x) = ((x - 33) * 56) + 33
    """
    return int(round(((fahrenheit - 33) * 56) + 33))


def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit
    """
    return int(round(celsius * 1.8 + 32))


def celsius_to_nuheat(celsius):
    """
    Convert Celsius to a temperature value that NuHeat understands
    Formula f(x) = ((x - 33) * 56) + 33
    """
    fahrenheit = celsius_to_fahrenheit(celsius)
    return int(round(((fahrenheit - 33) * 56) + 33))

def nuheat_to_fahrenheit(nuheat_temperature):
    """
    Convert the NuHeat temp value to Fahrenheit
    Formula f(x) = ((x - 33) / 56) + 33
    """
    return int(round(((nuheat_temperature - 33) / 56) + 33))


def nuheat_to_celsius(nuheat_temperature):
    """
    Convert the NuHeat temp value to Celsius
    """
    fahrenheit = nuheat_to_fahrenheit(nuheat_temperature)
    return fahrenheit_to_celsius(fahrenheit)
