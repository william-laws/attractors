import random
import pygame

class Lorenz:
    def __init__(self):
        self.xMin, self.xMax = -30, 30
        self.yMin, self.yMax = -30, 30
        self.zMin, self.zMax = 0, 50
        self.X, self.Y, self.Z = 0.1, 0.0, 0.0
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.dt = 0.01
        self.a, self.b, self.c = 0.2, 0.2, 5.7
        self.pixelColor = (255, 0, 0)

    def step(self):
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * (-self.Y-self.Z))
        self.Y = self.Y + (self.dt * (self.X + (self.a * self.Y)))
        self.Z = self.Z + (self.dt * (self.b + (self.X * self.Z) - (self.c * self.Z)))

    def draw(self, displaySurface):
        width, height = displaySurface.get_size()
        oldPos = self.ConvertToScreen(self.oX, self.oY, self.xMin, self.xMax, self.yMin, self.yMax, width, height)
        newPos = self.ConvertToScreen(self.X, self.Y, self.xMin, self.xMax, self.yMin, self.yMax, width, height)

        newRect = pygame.draw.line(displaySurface, self.pixelColor, oldPos, newPos, 2)

        return newRect
    
    def ConvertToScreen(self, x, y, xMin, xMax, yMin, yMax, width, height):
        newX = width * ((x - xMin) / (xMax - xMin))
        newY = height * ((y - yMin) / (yMax - yMin))
        return round(newX), round(newY)
    
class Application:
    def __init__(self):
        self.isRunning = True
        self.displaySurface = None
        self.fpsClock = None
        self.attractors = []
        self.size = self.width, self.height = 1440, 800
        self.count = 0
        self.outputCount = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Lorenz Attractor")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.isRunning = True
        self.fpsClock = pygame.time.Clock()
        
        # the chaotic part
        color = []
        color.append((0,255,128))
        color.append((51,255,255))
        color.append((153,51,255))

        for i in range(0,3):
            self.attractors.append(Lorenz())
            self.attractors[i].X = random.uniform(-0.1,0.1)
            self.attractors[i].pixelColor = color[i]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        for x in self.attractors:
            x.step()

    def on_render(self):
        for x in self.attractors:
            newRect = x.draw(self.displaySurface)
            pygame.display.update(newRect)
    
    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False
        
        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
            
            self.fpsClock.tick()
            self.count += 1
        
        pygame.quit()

if __name__ == "__main__":
    t = Application()
    t.on_execute()