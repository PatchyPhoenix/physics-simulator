import sys 
import numpy as np

sys.path.insert(1, './')

from main import Simulation
from vectors import Vector
from body import Body

def burrau(benchmark=False, dataDump=False):
    sim = Simulation(benchmark, dataDump)

    planet = Body(9.284e6) 
    planet.setMass(3)
    planet.setPosition(Vector(np.array([1, 3, 0.0], dtype='float64')))
    planet.setVelocity(Vector(np.array([0.0, 0.0, 0.0], dtype='float64')))
    planet.setVisualScale(10e7)
    planet.setColor((255,0,0))


    planet2 = Body(9.284e6) 
    planet2.setMass(4)
    planet2.setPosition(Vector(np.array([-2, -1, 0.0], dtype='float64')))
    planet2.setVelocity(Vector(np.array([0.0, 0.0, 0.0], dtype='float64')))
    planet2.setVisualScale(10e7)
    planet2.setColor((0,255,0))


    planet3 = Body(9.284e6) 
    planet3.setMass(5)
    planet3.setPosition(Vector(np.array([1, -1, 0], dtype='float64'))) 
    planet3.setVelocity(Vector(np.array([0.0, 0.0, 0.0], dtype='float64')))
    planet3.setVisualScale(10e7)
    planet3.setColor((0,0,255))


    sim.addBody(planet)
    sim.addBody(planet2)
    sim.addBody(planet3)


    sim.start()
    
    return (sim.frames/sim.cycles)

if __name__ == "__main__":
    print("Average FPS:", burrau(dataDump=True))