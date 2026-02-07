import math
import utils
from vectors import Vector, Position
from constants import G

class Body:
	def __init__(self, density=None, mass=None, radius=None, position=Position()):
		# kg/m^3
		self.density = density
		# kg
		self.mass = mass
		# km
		self.radius = radius
		# km
		self.position = position
		self.predictedPosition = Position()
		
		# represent the body as a different size (for better visualisation) (1 -> accurate size) (10 -> appears 10 times larger than it actually is)
		self.visualScale = 1
		self.color = (255, 255, 255)

		# km/s
		self.velocity = Vector()
		self.predictedVelocity = Vector()
		# km/s^2
		self.acceleration = Vector()

		self.jerk = Vector()

		self.energy = 0

		self.calculateMissingParams()


	def setMass(self, mass):
		self.mass = mass
		self.calculateMissingParams()


	def setRadius(self, radius):
		self.radius = radius
		self.calculateMissingParams()


	def setDensity(self, density):
		self.density = density
		self.calculateMissingParams()

	
	def setColor(self, color: tuple):
		self.color = color


	def setVisualScale(self, scale):
		self.visualScale = scale


	def setPosition(self, position: 'Position'):
		if isinstance(position, Position):
			self.position = position
		else:
			raise TypeError("Position must be an instance of the Position class")


	def setVelocity(self, velocity: 'Vector'):
		self.velocity = velocity


	def setAcceleration(self, acceleration: 'Vector'):
		self.acceleration = acceleration


	def setJerk(self, jerk: 'Vector'):
		self.jerk = jerk
	

	def calculateEnergy(self, bodies):
		ke = (self.mass * (self.velocity.magnitude ** 2)) / 2
		gpe = 0
		for body in bodies:
			r = (body.position - self.position).magnitude
			if r != 0:
				gpe += -((G * self.mass * body.mass) / r)
		return (ke + gpe)
		

	def calculateMissingParams(self):
		if self.mass is None:
			if self.radius is not None and self.density is not None:
				self.mass = utils.calculateMass(self.density, utils.calculateVolume(self.radius))
				return

		if self.radius is None:
			if self.mass is not None and self.density is not None:
				self.radius = utils.calculateRadius(utils.CalculateVolume(self.density, self.mass))
				return

		if self.density is None:
			if self.mass is not None and self.radius is not None:
				volume = utils.calculateVolume(self.radius)
				if volume != 0:
					self.density = utils.calculateDensity(self.mass, volume)
				return