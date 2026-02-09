import sys 
import numpy as np

sys.path.insert(1, './')

from main import Simulation
from vectors import Vector
from body import Body

def figure8(benchmark=False, dataDump=False):
    sim = Simulation(benchmark, dataDump)

    planet = Body(9.284e6) 
    planet.setMass(1)
    planet.setPosition(Vector(np.array([0.970004, -0.243087, 0.0], dtype='float64')))
    planet.setVelocity(Vector(np.array([0.008019, 0.007437, 0.0], dtype='float64')))
    planet.setVisualScale(10e7)
    planet.setColor((255,0,0))


    planet2 = Body(9.284e6) 
    planet2.setMass(1)
    planet2.setPosition(Vector(np.array([-0.970004, 0.243087, 0.0], dtype='float64')))
    planet2.setVelocity(Vector(np.array([0.008019, 0.007437, 0.0], dtype='float64')))
    planet2.setVisualScale(10e7)
    planet2.setColor((0,255,0))


    planet3 = Body(9.284e6) 
    planet3.setMass(1)
    planet3.setPosition(Vector(np.array([0, 0, 0], dtype='float64'))) 
    planet3.setVelocity(Vector(np.array([-0.016039, -0.014875, 0.0], dtype='float64')))
    planet3.setVisualScale(10e7)
    planet3.setColor((0,0,255))


    sim.addBody(planet)
    sim.addBody(planet2)
    sim.addBody(planet3)


    sim.start()
    
    return (sim.frames/sim.cycles)

if __name__ == "__main__":
    print("Average FPS:", figure8(dataDump=True, benchmark=True))