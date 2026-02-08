from vectors import Vector
from constants import *
from body import Body
import numpy as np


def calculateHermite(body: Body, bodies: list, dt: float):
        dt2 = dt * dt
        
        dt3 = dt2 * dt
        predictedPos = body.position.vector + (body.velocity.vector * dt) + (body.acceleration.vector * dt2) / 2 + (body.jerk.vector * dt3) / 6
        predictedVel = body.velocity.vector + (body.acceleration.vector * dt) + (body.jerk.vector * dt2 / 2)
        
        futureAcc = np.zeros(3, dtype='float64')
        futureJerk = np.zeros(3, dtype='float64')
        for b in bodies:
            if b == body:
                 continue
            r_vec = b.predictedPosition.vector - predictedPos 
            v_vec = b.predictedVelocity.vector - predictedVel
            
            r2 = np.dot(r_vec, r_vec) + 1e-15
            r3 = r2**1.5
            r5 = r3 * r2
            c = G * b.mass
            futureAcc += (c * r_vec) / r3
            dot_rv = r_vec.dot(v_vec)
            futureJerk += c * ((v_vec / r3) - (3 * dot_rv * r_vec / r5))
            
        correctedVel = body.velocity.vector + ((body.acceleration.vector + futureAcc) * dt) / 2 + ((body.jerk.vector - futureJerk) * dt2)/12
        correctedPos = predictedPos + ((body.acceleration.vector - futureAcc)* dt2) / 12 + ((body.jerk.vector + futureJerk) * dt3) / 120
        body.position.vector = correctedPos
        body.velocity.vector = correctedVel
        body.acceleration.vector = futureAcc
        body.jerk.vector = futureJerk

        """body.setPosition(Vector(correctedPos))
        body.setVelocity(Vector(correctedVel))
        body.setAcceleration(futureAcc)
        body.setJerk(futureJerk)"""


def calculateTimeStep(bodies: list):
    minDt = 0.01
    for body in bodies:
        dt =  eta * (body.acceleration.magnitude / (body.jerk.magnitude + 1e-15))
        if dt < minDt:
            minDt = dt
    return minDt


def calculateConditions(body: Body, bodies:list):
    a = Vector()
    j = Vector()

    for b in bodies:
        if b == body:
             continue
        
        r_vec = b.position.vector - body.position.vector
        v_vec = b.velocity.vector - body.velocity.vector

        r2 = np.dot(r_vec, r_vec) + 1e-15
        r3 = r2**1.5 
        r5 = r2*r3
        c = G * b.mass
        a += (c * r_vec) / r3
        dot_rv = r_vec.dot(v_vec)
        j += c * ((v_vec / r3) - (3 * dot_rv * r_vec / r5))

    body.setAcceleration(a)
    body.setJerk(j)

def predictAll(bodies, dt: float):
    for b in bodies:
        # Step 3: Jump into the future
        b.predictedPosition.vector[:] = b.position.vector + b.velocity.vector * dt + b.acceleration.vector * (dt * dt) / 2 + b.jerk.vector * (dt * dt * dt) / 6
        b.predictedVelocity.vector[:] = b.velocity.vector + b.acceleration.vector * dt + b.jerk.vector * (dt * dt) / 2