import math
import numpy as np
from constants import *
from vectors import Vector

def calculateDensity(mass, volume):
    if volume == 0:
        raise ValueError("Volume cannot be zero.")
    return mass / volume


def calculateMass(density, volume):
    return density * volume


def CalculateVolume(density, mass):
    if density == 0:
        raise ValueError("Density cannot be zero.")
    return mass / density


def calculateRadius(volume):
    if volume < 0:
        raise ValueError("Volume cannot be negative.")
    return ((3 * volume) / (4 * math.pi)) ** (1/3)


def calculateVolume(radius):
    return (4/3) * math.pi * (radius**3)


def calculateEnergy(bodies):
    e = 0
    for body in bodies:
        for x in bodies:
            if x != body:
                r = x.position - body.position
                e += (G * body.mass * x.mass) / (2 * r.magnitude)

    return e


def representValue(value):
    if value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value))))
    mantissa = value / (10 ** exponent)
    return f"{mantissa:.1f} * 10^{exponent}"


def magnitude(a: np.ndarray):
    return np.linalg.norm(a)

def unit(a: np.ndarray):
    mag = magnitude(a)
    if mag == 0:
        return np.zeros_like(a)
    return a / mag

def arrayToVector(a: np.ndarray):
    return Vector(a[0], a[1], a[2])

def massConversion(mass):
    return mass / (1.989 * (10 ** 30))

def distanceConversion(distance):
    return distance / (1.496 * (10 ** 8))

def timeConversion(time):
    return time / 86400

def densityConversion(density):
    return density * (1.685 * (10 ** -7))

def velocityConversion(velocity):
    return velocity * (5.775 * (10 ** -4))

def accelerationConversion(acceleration):
    return acceleration * (6.68 * (10 ** -9))