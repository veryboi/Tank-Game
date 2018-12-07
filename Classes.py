import pygame
import math
import random
mapSize = (5000, 4000)
viewSize = (400,300)
screen = pygame.display.set_mode(viewSize)
camera = [0,0]
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
systemFont = pygame.font.SysFont('Calibri', 30)
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
        screen.fill((173,255,47))
        viewport = (camera, (viewSize[0]+camera[0], viewSize[1]+camera[1]))
        for tank in self.Tanks:
                adjustPosition = [tank.position[0] - camera[0], tank.position[1] - camera[1]]
                if tank.isPlayer:
                    blueInstance = rotate(bluetank,tank.rotation)
                    blueInstance.set_colorkey((195,195,195))

                    screen.blit(blueInstance,adjustPosition)

                else:
                    redInstance = pygame.transform.rotozoom(redtank, tank.rotation,1)
                    # redInstance.set_colorkey((195, 195, 195))
                    screen.blit(redInstance, adjustPosition)

        for bullet in self.Bullets:
            adjustPosition = [bullet.position[0] - camera[0], bullet.position[1] - camera[1]]
            screen.blit(bullet, adjustPosition)

        for obstacle in self.Naturals:

            if type(obstacle).__name__ == "Tree":

                point1 = (obstacle.position[0]+obstacle.radius-camera[0], obstacle.position[1]+obstacle.radius-camera[1])

                pygame.draw.circle(screen, (0,100,0), point1, obstacle.radius)
            elif type(obstacle).__name__ == "Rock":
                point1 = (obstacle.position[0]-camera[0], obstacle.position[1]-camera[1])
                pygame.draw.rect(screen, (100,100,100), (point1, (obstacle.width, obstacle.height)))

        pygame.draw.rect(screen, (255,0,0), ((-camera[0], -camera[1]), mapSize), 3)
        TankPos = systemFont.render(str(myTank.position), False, (0, 0, 0))
        screen.blit(TankPos, (0, 0))
        pygame.display.flip()


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
    def __init__(self, health, damage, speed, bspeed, position, isPlayer, rotation=0):
        self.health = health
        self.maxhealth = health
        self.damage = damage
        self.speed = speed
        self.bspeed = bspeed
        self.position = position
        self.isPlayer = isPlayer
        self.rotation = rotation

    def shoot(self, vector):
        pass


class Bullet:
    def __init___(self, current, angle, speed):
        self.position = current
        self.angle = angle
        self.speed = speed
        self.counter = 0
        while self.counter < 100:
            self.position = self.position + [speed*math.cos(2*angle*math.pi/360), speed*math.sin(2*angle*math.pi/360)]
            self.counter += 1
        currentMap.Destroy(self)


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


def rotate(image, angle):
    """rotate a Surface, maintaining position."""

    loc = image.get_rect().center  #rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc

    return rot_sprite

currentMap = Map()
#health, damage, speed, bspeed, position, isPlayer
myTank = Tank(100, 100, 100, 100, [(viewSize[0]-tanksize[0])/2,(viewSize[1]-tanksize[1])/2], True)
pooptank = Tank(100,100,100,100,[5,100], False)
objects = [myTank, Tree((0,100)), Rock((10,30)), pooptank]
for i in range(1000):
    objects.append(Tree([random.randint(0,mapSize[0]), random.randint(0,mapSize[1])]))

currentMap.AddObjects(objects)

while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            break
    keys_pressed = pygame.key.get_pressed()
    interval = 3

    if keys_pressed[pygame.K_RIGHT]:
        if myTank.position[0] <= mapSize[0]-interval-tanksize[0]:
            myTank.position[0] += interval

            camera[0] += interval
    if keys_pressed[pygame.K_LEFT]:
        if myTank.position[0] >= interval:
            myTank.position[0] -= interval
            camera[0] -= interval
    if keys_pressed[pygame.K_UP]:
        if myTank.position[1] >= interval:
            myTank.position[1] -= interval
            camera[1] -= interval
    if keys_pressed[pygame.K_DOWN]:
        if myTank.position[1] <= mapSize[1]-interval-tanksize[1]:
            myTank.position[1] += interval
            camera[1] += interval
    if keys_pressed[pygame.K_r]:
        myTank.rotation += 1
    if keys_pressed[pygame.K_SPACE]:
        pass
    currentMap.Draw()
    clock.tick(60)
