from vectors import Vector
from constants import *
from body import Body


def calculateHermite(body: Body, bodies: list, dt: int):
        predictedPos = body.position + body.velocity*dt + body.acceleration*(dt**2)/2 + body.jerk*(dt**3)/6
        predictedVel = body.velocity + body.acceleration*dt + body.acceleration*(dt**2)/2
        
        futureAcc = Vector()
        futureJerk = Vector()
        for b in bodies:
            if b == body:
                 continue
            r_vec = b.predictedPosition - predictedPos 
            v_vec = b.predictedVelocity - predictedVel
            
            r2 = r_vec.magnitude**2
            r3 = r2**1.5 + 1e-20
            r5 = r2**2.5 + 1e-20
            
            futureAcc += (G * b.mass * r_vec) / r3
            dot_rv = r_vec.dot(v_vec)
            futureJerk += (G * b.mass) * ((v_vec / r3) - (3 * dot_rv * r_vec / r5))
            
        correctedVel = body.velocity + (body.acceleration + futureAcc)*dt/2 + (body.jerk - futureJerk)*(dt**2)/12
        correctedPos = predictedPos + (body.acceleration - futureAcc)*(dt**2) / 12 + (body.jerk + futureJerk)*(dt**3) / 120
        body.setPosition(correctedPos)
        body.setVelocity(correctedVel)
        body.setAcceleration(futureAcc)
        body.setJerk(futureJerk)


def calculateTimeStep(bodies: list):
    timeSteps = []
    for body in bodies:
            try:
                timeStep =  eta * (body.acceleration.magnitude / (body.jerk.magnitude + 0.0000000000001) )
                timeSteps.append(timeStep)
            except:
                pass
    return min(min(timeSteps), 0.01)

def calculateConditions(body: Body, bodies:list):
    a = Vector()
    j = Vector()
    for b in bodies:
        if b == body:
             continue
        r_vec = b.position - body.position
        v_vec = b.velocity - body.velocity
        r2 = r_vec.magnitude**2
        r3 = r2**1.5 + 1e-20
        r5 = r2**2.5 + 1e-20
        a += (G * b.mass * r_vec) / r3
        dot_rv = r_vec.dot(v_vec)
        j += (G * b.mass) * ((v_vec / r3) - (3 * dot_rv * r_vec / r5))
    body.setAcceleration(a)
    body.setJerk(j)

def predictAll(bodies, dt):
    for b in bodies:
        # Step 3: Jump into the future
        b.predictedPosition = b.position + b.velocity*dt + b.acceleration*(dt**2)/2 + b.jerk*(dt**3)/6
        b.predictedVelocity = b.velocity + b.acceleration*dt + b.jerk*(dt**2)/2