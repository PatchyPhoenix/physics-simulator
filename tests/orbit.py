import sys 

sys.path.insert(1, './')


from main import Simulation
from vectors import Position, Vector
from body import Body


sim = Simulation()
star = Body()
star.setMass(1)
star.setRadius(4.652e-3)
star.setColor((255, 255, 50))
star.setVisualScale(10e7)

planet = Body(9.284e6) 
planet.setMass(3.003e-6)
planet.setPosition(Position(1, 0)) 
planet.setVelocity(Vector(0, 0.0172))
planet.setVisualScale(10e9)
planet.setColor((0,255,50))


sim.addBody(star)
sim.addBody(planet)

sim.start()