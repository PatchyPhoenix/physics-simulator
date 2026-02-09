import sys 
import numpy as np

sys.path.insert(1, './')


from main import Simulation
from vectors import Vector
from body import Body


def orbit(benchmark=False, dataDump=False):
    sim = Simulation(benchmark, dataDump)
    star = Body()
    star.setMass(1)
    star.setRadius(4.652e-3)
    star.setColor((255, 255, 50))
    star.setVisualScale(10e7)

    planet = Body(9.284e6) 
    planet.setMass(3.003e-6)
    planet.setPosition(Vector(np.array([1, 0, 0], dtype='float64'))) 
    planet.setVelocity(Vector(np.array([0, 0.0172, 0.0], dtype='float64')))
    planet.setVisualScale(10e9)
    planet.setColor((0,255,50))


    sim.addBody(star)
    sim.addBody(planet)

    sim.start()
    return (sim.frames/sim.cycles)

if __name__ == "__main__":
    print("Average FPS:", orbit())