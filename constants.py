# units
 
"""

1 AU = 1.496 * 10 ** 8 km

1 SM (solar masses) = 1.989 * 10^30 kg

1 D (day) = 86400s

"""


# constant values
G = 0.000295912208  # Gravitational constant in AU^3/(SM*day^2)
# 1 km^3 = 1e9 m^3, so we multiply by 1e-9 to convert to km^3

e = 10e-5

eta = 0.001

# constant classes
class Material:
    def __init__(self):
        self.density = None
        self.color = (0, 0, 0)

class Rock(Material):
    def __init__(self):
        super().__init__()
        self.density = 10