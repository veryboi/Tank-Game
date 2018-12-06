import pygame
import time
mapSize = (500, 400)
viewSize = (200,300)
screen = pygame.display.set_mode(viewSize)
camera = [0,0]
clock = pygame.time.Clock()
pygame.init()
tanksize = (30,15)
bluetank = pygame.image.load("tankblue.png")
bluetank = pygame.transform.scale(bluetank, tanksize)
redtank = pygame.image.load("tankred.png")
redtank = pygame.transform.scale(redtank, tanksize)
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
        screen.fill((0, 0, 0))
        viewport = (camera, (viewSize[0]+camera[0], viewSize[1]+camera[1]))
        for tank in self.Tanks:
            if viewport[0][0] <= tank.position[0] <= viewport[1][0] and viewport[0][1] <= tank.position[1] <= viewport[1][1]:
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

                point1 = (obstacle.position[0]+obstacle.radius, obstacle.position[1]+obstacle.radius)
                point2= (obstacle.position[0]-obstacle.radius, obstacle.position[1]-obstacle.radius)
                if (viewport[0][0] <= point1[0] <= viewport[1][0] and viewport[0][1] <= point1[1] <= viewport[1][1]) or (viewport[0][0] <= point2[0] <= viewport[1][0] and viewport[0][1] <= point2[1] <= viewport[1][1]):

                    pygame.draw.circle(screen, (0,0,255), obstacle.position, obstacle.radius)
            elif type(obstacle).__name__ == "Rock":
                point1 = obstacle.position
                point2 = (obstacle.position[0]+obstacle.width, obstacle.position[1]+obstacle.height)

                if (viewport[0][0] <= point1[0] <= viewport[1][0] and viewport[0][1] <= point1[1] <= viewport[1][1]) or (viewport[0][0] <= point2[0] <= viewport[1][0] and viewport[0][1] <= point2[1] <= viewport[1][1]):
                    pygame.draw.rect(screen, (100,100,100), (obstacle.position[0], obstacle.position[1], obstacle.position[0]+obstacle.width, obstacle.position[0]+obstacle.height))

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
        self.radius = 5
        self.health = 750
        self.position = position
class Rock:
    def __init__(self, position):
        self.width = 15
        self.height = 15
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
myTank = Tank(100, 100, 100, 100, [1,100], True)
objects = [myTank, Tree((0,100)), Rock((10,30))]

currentMap.AddObjects(objects)
while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            break
    keys_pressed = pygame.key.get_pressed()
    
    if keys_pressed[pygame.K_RIGHT]:
        myTank.position[0] += 5

    if keys_pressed[pygame.K_LEFT]:
        myTank.position[0] -= 5
    if keys_pressed[pygame.K_UP]:
        myTank.position[1] -= 5
    if keys_pressed[pygame.K_DOWN]:
        myTank.position[1] += 5

    # if keys_pressed[pygame.K_RIGHT]:
    #     x += 5
    # if keys_pressed[pygame.K_UP]:
    #     y -= 5
    # if keys_pressed[pygame.K_DOWN]:
    #     y += 5

    currentMap.Draw()
    time.sleep(0.03)
