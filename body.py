import math
import utils
from vectors import Vector, Position

class Body:
	def __init__(self, density=None, mass=None, radius=None, position=None):
		self.density = density
		self.mass = mass
		self.radius = radius
		self.position = Position(0, 0) if position is None else position
		
		self.visualScale = 1
		self.color = (255, 255, 255)

		# km/s
		self.velocity = Vector(0, 0)
		# km/s^2
		self.acceleration = Vector(0, 0)


	def setMass(self, mass):
		self.mass = mass
		self.calculateMissingParams()


	def setRadius(self, radius):
		self.radius = radius
		self.calculateMissingParams()


	def setDensity(self, density):
		self.density = density
		self.calculateMissingParams()


	def calculateMissingParams(self):
		if self.mass == None:
			if self.radius != None and self.density != None:
				self.mass = utils.calculateMass(self.density, utils.calculateVolume(self.radius))

		if self.radius == None:
			if self.mass != None and self.density != None:
				self.radius = utils.calculateRadius(utils.CalculateVolume(self.density, self.mass))

		if self.density == None:
			if self.mass != None and self.radius != None:
				self.density = utils.calculateDensity(self.mass, utils.calculateVolume(self.radius))


	def setVelocity(self, velocity: 'Vector'):
		self.velocity = velocity

	
	def setColor(self, color: tuple):
		self.color = color

	def setVisualScale(self, scale):
		self.visualScale = scale


	def setAcceleration(self, acceleration: 'Vector'):
		self.acceleration = acceleration


	def setPosition(self, position):
		if isinstance(position, Position):
			self.position = position
		else:
			raise TypeError("Position must be an instance of the Position class")