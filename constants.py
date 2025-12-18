# constant values
G = 6.6743 * 10**-20  # Gravitational constant in km^3/(kg*s^2)
# 1 km^3 = 1e9 m^3, so we multiply by 1e-9 to convert to km^3

e = 10 ** -5

eta = 0.02

# constant classes
class Material:
    def __init__(self):
        self.density = None
        self.color = (0, 0, 0)

class Rock(Material):
    def __init__(self):
        super().__init__()
        self.density = 10