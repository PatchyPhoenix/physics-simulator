import math

def calculateDensity(mass, volume):
    return mass / volume


def calculateMass(density, volume):
    return density * volume


def CalculateVolume(density, mass):
    return mass / density


def calculateRadius(volume):
    return ((((3/4)/math.pi) * volume) ** (1/3))


def calculateVolume(radius):
    return (4/3) * math.pi * (radius**3)


def representValue(value):
    if value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value))))
    mantissa = value / (10 ** exponent)
    return f"{mantissa:.1f} * 10^{exponent}"