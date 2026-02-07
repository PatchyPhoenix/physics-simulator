import sys 

sys.path.insert(1, './')

from main import Simulation
from vectors import Position, Vector
from body import Body


sim = Simulation()

planet = Body(9.284e6) 
planet.setMass(1)
planet.setPosition(Position(0.970004, -0.243087)) 
planet.setVelocity(Vector(0.008019, 0.007437))
planet.setVisualScale(10e7)
planet.setColor((255,0,0))


planet2 = Body(9.284e6) 
planet2.setMass(1)
planet2.setPosition(Position(-0.970004, 0.243087)) 
planet2.setVelocity(Vector(0.008019, 0.007437))
planet2.setVisualScale(10e7)
planet2.setColor((0,255,0))


planet3 = Body(9.284e6) 
planet3.setMass(1)
planet3.setPosition(Position(0, 0)) 
planet3.setVelocity(Vector(-0.016039, -0.014875))
planet3.setVisualScale(10e7)
planet3.setColor((0,0,255))


sim.addBody(planet)
sim.addBody(planet2)
sim.addBody(planet3)


sim.start()