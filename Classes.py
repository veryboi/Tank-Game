import pygame
import time
mapSize = (500, 400)
viewSize = (200,300)
screen = pygame.display.set_mode(viewSize)
camera = (0,0)
clock = pygame.time.Clock()
pygame.init()
bluetank = pygame.image.load("tankblue.png")
redtank = pygame.image.load("tankblue.png")
bullet = pygame.image.load("bullet.png")
class Map:
    def __init__(self):
        self.Tanks = []
        self.Bullets = []
        self.Naturals = []

    def AddObjects(self, listofObjects):
        for o in listofObjects:
            if type(o).__name__ == "Tank":
                self.Tanks.append(o)

            elif type(o).__name__ == "Bullet":
                self.Bullets.append(o)
            else:
                self.Naturals.append(o)
            print("It is a " + type(o).__name__)
    def Draw(self):
        viewport = (camera, (viewSize[0]+camera[0], viewSize[1]+camera[1]))


        for tank in self.Tanks:
            if (viewport[0][0]<=tank.position[0]<=viewport[1][0] and viewport[0][1]<=tank.position[1]<=viewport[1][1]):
                if tank.isPlayer == True:
                    screen.blit(bluetank, tank.position)

                else:
                    screen.blit(redtank, tank.position)
        for bullet in self.Bullets:
            if viewport[0][0] <= bullet.position[0] <= viewport[1][0]:
                screen.blit(bullet, bullet.position)
        pygame.display.flip()
        for obstacle in self.Naturals:
            if type(obstacle).__name__ == "Tree":
                pygame.draw.circle(screen, (0,0,255), (obstacle.position[0]-obstacle.radius, obstacle.position[1]-obstacle.radius, obstacle.position[0]+obstacle.radius, obstacle.position[1]+obstacle.radius)
    def Destroy(self, object):
        for i in self.Tanks:
            if id(i) == id(object):
                self.Tanks.remove(object)
                break
        for i in self.Bullets:
            if id(i) == id(object):
                self.Tanks.remove(object)
                break
        for i in self.Naturals:
            if id(i) == id(object):
                self.Tanks.remove(object)


class Tank:
    def __init__(self, health, damage, speed, bspeed, position, isPlayer):
        self.health = health
        self.maxhealth = health
        self.damage = damage
        self.speed = speed
        self.bspeed = bspeed
        self.position = position
        self.isPlayer = isPlayer

    def shoot(self, vector):
        pass
class Bullet:
    def __init___(self, current, target):
        self.position = current
class Tree:
    def __init__(self, position):
        self.radius = 50
        self.health = 750
        self.position = position
class Rock:
    def __init__(self, position):
        self.width = 50
        self.height = 50
        self.health = 2000
        self.position = position
class NaturalPoly:
    def __int__(self, points):
        self.points = points


def destroy(object):
    pass
def takeDamage(object, damage):
    if object.health > damage:
        object.health = object.health - damage
    else:
        object.Die()
currentMap = Map()
newTank = Tank(100, 100, 100, 100, (1,100), True)
currentMap.AddObjects([newTank])
while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            break

    currentMap.Draw()

