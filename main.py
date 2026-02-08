import pygame
import threading
from vectors import Vector
from constants import *
from body import Body
from utils import *
import time
import math
from hermite import calculateConditions, calculateHermite, calculateTimeStep, predictAll
from collision import *


#  IMPORTANT NOTE
#
#  BODY seems to oscilate ONLY under certain FPS or timescale conditions
#  switching to verlet's integration from euler's may fix it -> done
#  making an adaptive time step for calculating physics can also help
#

# AYO NIG-
# NOTE: the most expensive functions:  1. updateChunks   2. calculations

# TODO: just for funnzies -> check (delta)E (change of energy) of the body (if it is 0 -> simulation is perfectly accurate, higher the value, more the inaccuracy)
# also implement an adaptive time step
# parallel process for drawing :question:


class Simulation:
    def __init__(self, benchmark=False):

        self.tickRate = 600 # 0 = max FPS (currently can't be used as 0)
        self.scale = 50000 # 1 pixel = 50000 km
        self.running = 0
        self.lastRender = time.time()
        self.benchmark = benchmark
    
        self.timeScale = 1 # s/s -> no unit  # 1 = real time, 0 = max time scale
        self.simTime = 0
        self.frames = 0
        self.cycles = 0

        # planetary bodies
        self.bodies = []

        self.chunks = {"I":[],"II":[],"III":[],"IV":[]}
        self.focusedChunks = []

        pygame.init()

        self.screenWidth = pygame.display.Info().current_w
        self.screenHeight = pygame.display.Info().current_h

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.DOUBLEBUF, 1024)
        self.screen.set_alpha(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEWHEEL, pygame.ACTIVEEVENT]) # allow only these events ("improves performance")
        
        pygame.display.set_caption("Simulation")

        self.energy = 0
        self.MOMENTUM = Vector()
        self.MASS = 0
        self.VELOCITY = Vector()

        self.dscale = 200

        #self.font = pygame.font.SysFont("Roboto", 18)
        
    def start(self):

        for body in self.bodies:
            calculateConditions(body, self.bodies)
            self.MASS += body.mass
            self.MOMENTUM += body.mass * body.velocity    
        self.VELOCITY = self.MOMENTUM / self.MASS
        
        for body in self.bodies:
            body.velocity -= self.VELOCITY
    
        self.running = 1
        self.generateChunks()
        self.mainLoop()


    def mainLoop(self):
        self.refresh()
        while self.running:
            try:    
                self.clock.tick(self.tickRate)
                self.frames += int(self.clock.get_fps())
                self.cycles += 1
                self.handleEvents()
                self.calculations()
                if (time.time() - self.lastRender) >= 0.008:
                    self.draw()
                    self.lastRender = time.time()

                if self.benchmark and self.simTime >= 150:
                    self.exit()
            except:
                pass

    def handleEvents(self):
        scale_change_factor = 1.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit()
            
                if event.key == pygame.K_q:
                    self.timeScale *= 10
                    print(self.timeScale)
            
                if event.key == pygame.K_e:
                    self.timeScale /= 10
            
                if event.key == pygame.K_f:
                    print(int(self.clock.get_fps()))
            
            elif event.type == pygame.MOUSEWHEEL:
            
                if event.y > 0:  # Zoom in
                    self.scale /= scale_change_factor
                    self.dscale *= scale_change_factor
            

                elif event.y < 0:  # Zoom out
                    self.scale *= scale_change_factor
                    self.dscale /= scale_change_factor
                
                # Prevent scale from becoming zero or negative
                if self.scale < 1:
                    self.scale = 1
                
                # Regenerate chunks after scaling
                self.generateChunks()
                self.refresh()


            # event when window is interacted with
            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 1 and event.state == pygame.APPACTIVE: # windpw reopened
                    pygame.display.update()
                    self.drawGrid()
                if event.gain == 0 and event.state == pygame.APPACTIVE: # window minimized (lower framerate / stop sim when it occurs)
                    print("minimized")


    def addBody(self, body: Body):
        body.calculateMissingParams()
        self.bodies.append(body)


    def refresh(self):
        self.screen.fill((0,0,0))
        self.generateChunks()
        self.drawGrid()
        pygame.display.update()


    def draw(self):
        for body in self.bodies:
            x, y = self.calculatePosition(body)
            visual_radius = int(body.radius * body.visualScale / self.scale)
            
            # Draw only if the body is within the screen bounds
            if -visual_radius <= x <= self.screenWidth + visual_radius and \
               -visual_radius <= y <= self.screenHeight + visual_radius:
                pygame.draw.circle(self.screen, body.color, (x, y), visual_radius)

        #self.drawInfo()
        #pygame.display.update()

        self.updateChunks()


    # chunk detection system (identify the chunks in which a body is updating)
        
    def updateChunks(self):
        loaded = []

        # the major computation is the chunk loop 
        # (each takes abt 0.01ms there are around 50-100 chunks each iteration (at basic zoom) meaning, it takes 0.5-1ms on its own)
        # optimize by reducing the number of chunks
        for body in self.bodies:
            for chunk in find_candidate_chunks(self.chunks, self.calculatePosition(body), body.radius * body.visualScale / self.scale, (self.screenWidth // 2,self.screenHeight // 2)):
                s = time.time()
                if check_collision_rect_circle(chunk, self.calculatePosition(body), body.radius * body.visualScale / self.scale):

                    if chunk not in loaded:
                        pygame.draw.rect(self.screen, (0, 0, 0), chunk)
                        loaded.append(chunk)    
                    
                    x, y = self.calculatePosition(body)
                    
                    if ((x < self.screenWidth + int(body.radius * body.visualScale / self.scale) and x > int(body.radius * body.visualScale / self.scale)) and (y < self.screenHeight + int(body.radius * body.visualScale / self.scale) and y > int(body.radius * body.visualScale / self.scale))):
                        pygame.draw.circle(self.screen, body.color, (x, y), int(body.radius * body.visualScale / self.scale))
                e = time.time()
                #print((e-s) *1000)
                    #pygame.draw.rect(self.screen, (25, 25, 25), chunk, 1) # grid


        # update chunks which previously had a body (not anymore)
        for x in self.focusedChunks:
            if x not in loaded:
                pygame.draw.rect(self.screen, (0, 0, 0), x)
                pygame.display.update(x)

        # update chunks containing bodies
        for chunk in loaded:
            self.focusedChunks = loaded
            pygame.display.update(chunk)


    def generateChunks(self):
        self.chunks = {
            "I":[],
            "II":[],
            "III":[],
            "IV":[]
        }

        scale = 5000000 * math.ceil(self.scale // 50000)
        if int(scale) == 0:
            scale = 5000000

        for x in range(self.screenWidth // 2, self.screenWidth, int(scale / self.scale)):
            # III
            for y in range(self.screenHeight // 2, self.screenHeight, int(scale / self.scale)):
                self.chunks["III"].append(pygame.Rect(x, y, int(scale / self.scale), int(scale / self.scale)))
            # II
            for y in range(self.screenHeight // 2 -int(scale / self.scale), -int(scale / self.scale), -int(scale / self.scale)):
                self.chunks["II"].append(pygame.Rect(x, y, int(scale / self.scale), int(scale / self.scale)))
            
        for x in range(self.screenWidth // 2-int(scale / self.scale), -int(scale / self.scale), -int(scale / self.scale)):
            # IV
            for y in range(self.screenHeight // 2, self.screenHeight, int(scale / self.scale)):
                self.chunks['IV'].append(pygame.Rect(x, y, int(scale / self.scale), int(scale / self.scale)))
            # I
            for y in range(self.screenHeight // 2 -int(scale / self.scale), -int(scale / self.scale), -int(scale / self.scale)):
                self.chunks['I'].append(pygame.Rect(x, y, int(scale / self.scale), int(scale / self.scale)))
            
    
    def drawGrid(self):
        colour = (25, 25, 25)

        for quad in self.chunks:
            for chunk in self.chunks[quad]:
                pygame.draw.rect(self.screen, colour, chunk, 1)


    def drawInfo(self):
        scale_info = f"Scale: {representValue(self.scale)}km/pixel  TimeScale: {representValue(self.timeScale)}s/s"
        text = self.font.render(scale_info, True, (255, 255, 255))  
        self.screen.blit(text, (10, 10))

        fps_info = f"FPS: {int(self.clock.get_fps())}"
        text = self.font.render(fps_info, True, (255,255,255))
        self.screen.blit(text, (self.screenWidth - text.get_width(), 10))

    # deprecated
    def update(self):
        s = time.time()
        self.draw()
        e = time.time()
        self.lastRender = time.time()
        #print((e-s)*1000)


    def calculations(self):
        targetDt = 0.008
        achievedDt = 0

        while achievedDt < targetDt:
            dt = max(calculateTimeStep(self.bodies), 0.001) * self.timeScale  # make the physics independent of fps
            predictAll(self.bodies, dt)
            for body in self.bodies:            
                calculateHermite(body, self.bodies, dt)
            achievedDt += dt
        self.simTime += achievedDt


    def calculatePosition(self, body: Body):
        screen_x = self.screenWidth // 2 + (body.position.x / 1) * self.dscale
        screen_y = self.screenHeight // 2 + (body.position.y / 1) * self.dscale
        return (int(screen_x), int(screen_y))


    def exit(self):
        self.running = 0
        pygame.quit()


if __name__ == "__main__":
    sim = Simulation()
    star = Body()
    star.setMass(1)
    star.setRadius(4.652e-3)
    star.setColor((255, 255, 50))
    star.setVisualScale(10e7)

    planet = Body(9.284e6) 
    planet.setMass(3.003e-6)
    planet.setPosition(Vector(np.array([1, 0, 0.0], dtype='float64'))) 
    planet.setVelocity(Vector(np.array([0, 0.0172, 0.0], dtype='float64')))
    planet.setVisualScale(10e9)
    planet.setColor((0,255,50))

    print(planet.radius)

    sim.addBody(star)
    sim.addBody(planet)

    planet.energy = planet.calculateEnergy(sim.bodies)

    time.sleep(.2)
    sim.start()