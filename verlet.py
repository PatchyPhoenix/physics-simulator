from vectors import Vector
from constants import *
from body import Body

# refer secret stash for formulas
# wasteful calculations are performed

# to be replaced by hermite (4th order)


# public function (initiator)
def calculateVerlet(body: Body, bodies: list, dt):
    preCalculateVerletPosition(body, bodies, dt)

# velocity after half timestep
def calculateHalfStepVelocity(body: Body, dt):
     return (body.velocity + (body.acceleration * (dt/2)))

# position after full timestep
def calculateFullStepPosition(body: Body, halfStepVelocity, dt):
    return (body.position + (halfStepVelocity * dt))

# velocity after full timestep
def calculateFullStepVelocity(body: Body, halfStepVelocity, dt):
    return halfStepVelocity + (body.acceleration * (dt/2))

# acceleration after full timestep
def calculateAcceleration(body: Body, otherBody: Body, dt):
     otherFullStepPosition = calculateFullStepPosition(otherBody, calculateHalfStepVelocity(otherBody, dt), dt)
     return (G * otherBody.mass * (otherFullStepPosition - body.position))/ ((otherFullStepPosition - body.position).magnitude ** 2 + e**2) ** 1.5

# jerk after full timestep
def calculateJerk(body: Body, otherBody: Body, dt):
    otherHalfStepVelocity = calculateHalfStepVelocity(otherBody, dt)

    fullStepVelocity = body.velocity
    otherFullStepVelocity = calculateFullStepVelocity(otherBody, otherHalfStepVelocity, dt)
    velocity = otherFullStepVelocity - fullStepVelocity

    fullStepPosition = body.position
    otherFullStepPosition = calculateFullStepPosition(otherBody, otherHalfStepVelocity, dt)
    position = otherFullStepPosition - fullStepPosition
    
    # denominator for all terms (to reduce compuations)
    denominator = ((position.magnitude ** 2) + e ** 2)

    # first term in the equation
    a = velocity
    
    # second term in the equation
    b = 3 * (velocity.dot(position)) / denominator

    # third term in the eqaution
    c = position

    jerk = (G * otherBody.mass / (denominator ** 1.5)) * (a - b * c)
    
    return jerk

# calculate position of body (and initiate velocity, acceleration and jerk calculations)
def preCalculateVerletPosition(body: Body, bodies: list, dt):
    halfStepVelocity = calculateHalfStepVelocity(body, dt)
    fullStepPosition = calculateFullStepPosition(body, halfStepVelocity, dt)

    body.setPosition(fullStepPosition)

    preCalculateVerletAcceleration(body, bodies, dt)
    preCalculateVerletVelocity(body, halfStepVelocity, dt)
    preCalculateVerletJerk(body, bodies, dt)

# calculate velocity of boyd 
def preCalculateVerletVelocity(body: Body, halfStepVelocity, dt):
     fullStepVelocity = calculateFullStepVelocity(body, halfStepVelocity, dt)
     body.setVelocity(fullStepVelocity)

# calculate accerlation of body
def preCalculateVerletAcceleration(body: Body, bodies: list, dt):
    acceleration = Vector()
    for otherBody in bodies:
        if otherBody != body:
            acceleration += calculateAcceleration(body, otherBody, dt)

    body.setAcceleration(acceleration)
    

# calculate jerk of body
def preCalculateVerletJerk(body: Body, otherBodies: list, dt):
    jerk = Vector()
    for otherBody in otherBodies:
        if otherBody != body:
            jerk += calculateJerk(body, otherBody, dt)

    body.setJerk(jerk)

# calculate timestep for next cycle
def calculateTimeStep(bodies: list):
    timeSteps = []
    for body in bodies:
            try:
                timeStep =  eta * (body.acceleration.magnitude / (body.jerk.magnitude + 0.0000000000001) )
                timeSteps.append(timeStep)
            except:
                pass
    return min(min(timeSteps), 1)
