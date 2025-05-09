import math

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.magnitude = self.calculateMagnitude()

    def calculateMagnitude(self):
        return (self.x**2 + self.y**2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self):
        return f"Vector: ({self.x}, {self.y})"
    
    def tuple(self):
        return (self.x, self.y)

    def __add__(self, other: 'Vector'):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector'):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector(self.x / scalar, self.y / scalar)
        else:
            raise ValueError("Cannot divide by zero")
    
    def angle(self, other: 'Vector'):
        dot_product = self.dot(other)
        magnitudes = self.magnitude * other.magnitude
        if magnitudes != 0:
            cos_theta = dot_product / magnitudes
            return math.acos(cos_theta)
        else:
            raise ValueError("Cannot calculate angle with zero vector")

    def resolve(self, other: 'Vector'):
        if self.magnitude != 0 and other.magnitude != 0:
            angle = self.angle(other)
            print(angle)
            return self.magnitude * math.cos(angle), self.magnitude * math.sin(angle)
        else:
            raise ValueError("Cannot resolve with zero vector")

    def dot(self, other: 'Vector'):
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: 'Vector'):
        return self.x * other.y - self.y * other.x
    
    def normalize(self):
        if self.magnitude != 0:
            return self / self.magnitude
        else:
            raise ValueError("Cannot normalize a zero vector")

    def angle(self, other):
        dot_product = self.dot(other)
        magnitudes = self.magnitude * other.magnitude
        if magnitudes != 0:
            cos_theta = dot_product / magnitudes
            return math.acos(cos_theta)
        else:
            raise ValueError("Cannot calculate angle with zero vector")
        
    def distance(self, other: 'Vector'):
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5
    
    def __lt__(self, other: 'Vector'):
        return self.magnitude < other.magnitude
    
    def __le__(self, other: 'Vector'):
        return self.magnitude <= other.magnitude
    
    def __gt__(self, other: 'Vector'):
        return self.magnitude > other.magnitude
    
    def __ge__(self, other: 'Vector'):
        return self.magnitude >= other.magnitude
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __copy__(self):
        return Vector(self.x, self.y, self.z)
    
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
    
    def __pos__(self):
        return Vector(self.x, self.y, self.z)

    def __abs__(self):
        return self.magnitude

    @staticmethod
    def from_magnitude_and_angle(magnitude, angle, reference: 'Vector'):
        if reference.magnitude == 0:
            raise ValueError("Reference vector cannot be a zero vector")
        
        # Normalize the reference vector to get its direction
        reference_normalized = reference.normalize()
        
        # Calculate the new vector's components
        x = magnitude * math.cos(angle) * reference_normalized.x
        y = magnitude * math.cos(angle) * reference_normalized.y
        
        # Create and return the new vector
        return Vector(x, y)
    
    

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def updateX(self, x):
        self.x = x

    def updateY(self, y):
        self.y = y


    def update(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return (self.x**2 + self.y**2) ** 0.5
    
    def distance(self, other: 'Position'):
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

    def unit(self):
        return Position(self.x / self.magnitude(), self.y / self.magnitude()) if self.magnitude() != 0 else Position(0, 0)

    def __repr__(self):
        return f"Position({self.x}, {self.y})"
    
    def __str__(self):
        return f"Position: ({self.x}, {self.y})"
    
    def tuple(self):
        return (self.x, self.y)
    
    def __add__(self, other: 'Position'):
        return Position(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Position'):
        return Position(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Position(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        if scalar != 0:
            return Position(self.x / scalar, self.y / scalar)
        else:
            raise ValueError("Cannot divide by zero")
    