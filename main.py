import pygame
from vectors import Vector, Position
from constants import *
from body import Body
from utils import *
from dataCollection import *
import time
import random

#  IMPORTANT NOTE
#
#  BODY seems to oscilate ONLY under certain FPS or timescale conditions
#  switching to verlet's integration from euler's may fix it
#  making a constant time step for calculating physics can also help
#


class Simulation:
    def __init__(self):

        self.tickRate = 140 # 0 = max FPS
        self.scale = 50000 # 1 pixel = 50000 km
        self.running = 0

        self.timeScale = 10e3 # s/s -> no unit  # 1 = real time, 0 = max time scale

        self.bodies = []
        self.startTime = None

        self.gData = StoreDict()
        self.accelerationData = StoreDict()
        self.velocityData = StoreDict()
        #self.positionData = StoreDict()


        pygame.init()

        self.screenWidth = pygame.display.Info().current_w
        self.screenHeight = pygame.display.Info().current_h

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.DOUBLEBUF, 1024)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEWHEEL])
        
        pygame.display.set_caption("Simulation")
        

    def start(self):
        self.running = 1
        self.startTime = time.time()
        self.mainLoop()


    def mainLoop(self):
        while self.running:
            self.clock.tick(self.tickRate)
            self.handleEvents()
            self.update()


    def handleEvents(self):

        scaleVar = 4999
        if self.scale > 1000000:
            scaleVar = 49999
        if self.scale > 10000000:
            scaleVar = 499999

        if self.scale <= 6000:
            scaleVar = 499
        if self.scale <= 600:
            scaleVar = 49

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = 0
                    self.exit()
                if event.key == pygame.K_q:
                    self.timeScale *= 10
                if event.key == pygame.K_e:
                    self.timeScale /= 10
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.scale += scaleVar
                elif event.y < 0:
                    self.scale -= scaleVar
                if self.scale < 1:
                    self.scale = 1


    def addBody(self, body: Body):
        body.calculateMissingParams()
        self.bodies.append(body)
        

    def calculatePosition(self, body: Body):
        if body.position == None:
            raise ValueError("Body position is not set")
        else:
            return self.screenWidth // 2 + int(body.position.x / self.scale), self.screenHeight // 2 + int(body.position.y / self.scale)


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.drawGrid()
        for body in self.bodies:
            if isinstance(body, Body):
                x, y = self.calculatePosition(body)
                #if ((x < self.screenWidth + int(body.radius * 50 / self.scale) and x > int(body.radius * 50 / self.scale)) and (y < self.screenHeight + int(body.radius * 50 / self.scale) and y > int(body.radius * 50 / self.scale))):
                pygame.draw.circle(self.screen, body.color, (x, y), int(body.radius * body.visualScale / self.scale))
                
        self.drawInfo()
        pygame.display.update()


    def drawGrid(self):

        colour = (25, 25, 25)

        scale = 5000000
        if self.scale >= 100000:
            scale = 10**7
        if self.scale >= 1000000:
            scale = 10**8
        if self.scale >= 10000000:
            scale = 10**9

        for x in range(self.screenWidth // 2, self.screenWidth, int(scale / self.scale)):
            pygame.draw.line(self.screen, colour, (x, 0), (x, self.screenHeight))
        
        for x in range(self.screenWidth // 2, 0, -int(scale / self.scale)):
            pygame.draw.line(self.screen, colour, (x, 0), (x, self.screenHeight))

        for y in range(self.screenHeight // 2, self.screenHeight, int(scale / self.scale)):
            pygame.draw.line(self.screen, colour, (0, y), (self.screenWidth, y))

        for y in range(self.screenHeight // 2, 0, -int(scale / self.scale)):
            pygame.draw.line(self.screen, colour, (0, y), (self.screenWidth, y))


    def drawInfo(self):
        font = pygame.font.SysFont("Roboto", 18)

        scale_info = f"Scale: {representValue(self.scale)}km/pixel  TimeScale: {representValue(self.timeScale)}s/s"
        text = font.render(scale_info, True, (255, 255, 255))  
        self.screen.blit(text, (10, 10))

        fps_info = f"FPS: {int(self.clock.get_fps())}"
        text = font.render(fps_info, True, (255,255,255))
        self.screen.blit(text, (self.screenWidth - text.get_width(), 10))


    def update(self):
        self.calculations()
        self.draw()


    def calculations(self):
        for body in self.bodies:
            force = Vector(0,0)

            for otherBody in self.bodies:
                if otherBody != body:
                    r12 = otherBody.position - body.position

                    magnitude = r12.magnitude()
                    unitVector = r12.unit()

                    # newton's shell theorem - absolutely useless for a star
                    #starMass = self.star.mass)

                    if magnitude == 0:
                        f = 0

                    # depth
                    if otherBody.radius > magnitude:
                        f = (G * otherBody.mass * magnitude * body.mass) / (otherBody.radius**3)

                    # height
                    if otherBody.radius < magnitude:
                        f = (G * otherBody.mass * body.mass) / (magnitude) ** 2

                    force += unitVector * f
                

            # Calculate acceleration: a = F / m
            body.acceleration.x = (force.x/body.mass)
            body.acceleration.y = (force.y/body.mass)

            # Update velocity based on acceleration
            body.velocity.x += (body.acceleration.x / self.tickRate) * self.timeScale
            body.velocity.y += (body.acceleration.y / self.tickRate) * self.timeScale


            # Update position based on velocity and acceleration
            body.position.x += (body.velocity.x / self.tickRate) * self.timeScale
            body.position.y += (body.velocity.y / self.tickRate) * self.timeScale

            end = time.time()
            self.gData.addEntry((end - self.startTime), (force/body.mass))
            self.velocityData.addEntry((end - self.startTime), body.velocity.tuple())
            self.accelerationData.addEntry((end - self.startTime), body.acceleration.tuple())



    def exit(self):
        self.running = 0
        self.gData.dump("tg")
        self.velocityData.dump("tv")
        self.accelerationData.dump("ta")
        pygame.quit()
        exit()


if __name__ == "__main__":
    sim = Simulation()
    star = Body()
    star.setMass(1.989e30)
    star.setRadius(696340)
    star.setColor((255, 255, 50))

    planet = Body(5.51 * (10 ** 12)) 
    planet.setMass(5.972e24)
    planet.setPosition(Position(14.96e6, 0)) 
    planet.setVelocity(Vector(0, 0))
    planet.setVisualScale(50)
    planet.setColor((255,0,0))

    planet2 = Body(5.51 * (10 ** 12))
    planet2.setMass(5.972e24)
    planet2.setPosition(Position(-4.96e5, 0))
    planet2.setVelocity(Vector(0, 0))

    sim.addBody(star)
    sim.addBody(planet)
    #sim.addBody(planet2)
    sim.start()