import math
import numpy as np

class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.vector = np.array([x, y, z], dtype='float64')

    def asarray(self):
        return self.vector
    
    def tuple(self):
        return (self.vector[0], self.vector[1], {self.vector[2]})

    def __repr__(self):
        return f"Vector(x={self.vector[0]:.2f}, y={self.vector[1]:.2f}, z={self.vector[2]:.2f})"
        
    @property
    def magnitude(self):
        return np.linalg.norm(self.vector)
    
    @property
    def x(self):
        return self.vector[0]

    @property
    def y(self):
        return self.vector[1]

    @property
    def z(self):
        return self.vector[2]
    

    def __add__(self, other: 'Vector'):
        if isinstance(other, Vector):
            return Vector(*(self.vector + other.vector))
        else:
            return Vector(*(self.vector + other))


    def __sub__(self, other: 'Vector'):
        if isinstance(other, Vector):
            return Vector(*(self.vector - other.vector))
        else:
            return Vector(*(self.vector - other))


    def __mul__(self, scalar):
        return Vector(*(self.vector * scalar))


    def __rmul__(self, scalar):
        return self.__mul__(scalar)


    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(*(self.vector / scalar))


    def dot(self, other: 'Vector'):
        if isinstance(other, Vector):
            return np.dot(self.vector, other.vector)
        else:
            return np.dot(self.vector, other)


    def cross(self, other: 'Vector'):
        if isinstance(other, Vector):
            return Vector(*(np.cross(self.vector, other.vector)))
        else:
            return Vector(*(np.cross(self.vector, other)))


    def unit(self):
        if self.magnitude == 0:
            print("Magnitude of vector is 0. Zero vector used.")
            return Position()
        return self / self.magnitude


    def distance(self, other: 'Vector'):
        if isinstance(other, Vector):
            return np.linalg.norm(self.vector - other.vector)
        else:
            return np.linalg.norm(self.vector - other)


    def angle(self, other: 'Vector'):
        dot_product = self.dot(other)
        magnitudes = self.magnitude * other.magnitude
        if magnitudes == 0:
            raise ValueError("Cannot calculate angle with a zero vector")
        cos_theta = dot_product / magnitudes
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        return math.acos(cos_theta)
    
    

class Position(Vector):
    def updateX(self, x=0.0):
        self.pos[0] = x


    def updateY(self, y=0.0):
        self.pos[1] = y


    def update(self, x=0.0, y=0.0, z=0.0):
        self.pos[0] = x
        self.pos[1] = y
        self.pos[2] = z