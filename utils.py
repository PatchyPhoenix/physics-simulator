import math
import vectors
import numpy as np
from vectors import Vector, Position

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

def arrayToPosition(a: np.ndarray):
    return vectors.Position(a[0], a[1], a[2])

def arrayToVector(a: np.ndarray):
    return vectors.Vector(a[0], a[1], a[2])

def vectorToPosition(vector: 'Vector'):
    return Position(vector.x, vector.y, vector.z)