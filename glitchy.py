import pygame
import math
import random
mapSize = (5000, 4000)
viewSize = (1000,500)
screen = pygame.display.set_mode(viewSize)
camera = [0,0]
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
systemFont = pygame.font.SysFont('Courier New', 10)
tanksize = (50,25)
bluetank = pygame.image.load("tankblue.png")
bluetank = pygame.transform.scale(bluetank, tanksize)
redtank = pygame.image.load("tankred.png")
redtank = pygame.transform.scale(redtank, tanksize)
bulletImage = pygame.image.load("bullet.png")


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


    def Draw(self):
        screen.fill((173,255,47))
        viewport = (camera, (viewSize[0]+camera[0], viewSize[1]+camera[1]))
        for tank in self.Tanks:

                if tank.isPlayer:
                    blueInstance, rect = rotate(bluetank,tank.rotation)
                    blueInstance.set_colorkey((195,195,195))

                    screen.blit(blueInstance,[(viewSize[0]-rect.width)/2,(viewSize[1]-rect.height)/2])

                else:
                    adjustPosition = [tank.position[0] - camera[0], tank.position[1] - camera[1]]
                    redInstance = pygame.transform.rotozoom(redtank, tank.rotation,1)
                    # redInstance.set_colorkey((195, 195, 195))
                    screen.blit(redInstance, adjustPosition)

        for bullet in self.Bullets:
            if bullet.counter < 100:
                for i in self.Naturals:
                    if type(i).__name__ == "Tree":
                        if getCollision(pygame.Rect(i.position[0]-i.radius, i.position[1]-i.radius, i.radius*2, i.radius*2),(bullet.position, [bullet.position[0] + bullet.angle[0] * bullet.speed / 10,
                                   bullet.position[1] + bullet.angle[1] * bullet.speed / 10])):
                            print("NOOO")
                            self.Destroy(bullet)
                    else:
                        if getCollision(pygame.Rect(i.position[0],i.position[1],i.width, i.height), (bullet.position, [bullet.position[0] + bullet.angle[0] * bullet.speed / 10,
                                   bullet.position[1] + bullet.angle[1] * bullet.speed / 10])):
                            print("NOOO")
                            self.Destroy(bullet)
                print("cool!")
                bullet.position = [bullet.position[0] + bullet.angle[0] * bullet.speed / 10,
                                   bullet.position[1] + bullet.angle[1] * bullet.speed / 10]
                bullet.counter += 1
            else:
                print("ded")
                self.Destroy(bullet)
            adjustPosition = [bullet.position[0] - camera[0], bullet.position[1] - camera[1]]
            screen.blit(bulletImage, adjustPosition)

        for obstacle in self.Naturals:

            if type(obstacle).__name__ == "Tree":

                point1 = (int(obstacle.position[0]+obstacle.radius-camera[0]), int(obstacle.position[1]+obstacle.radius-camera[1]))

                pygame.draw.circle(screen, (0,100,0), point1, int(obstacle.radius))
            elif type(obstacle).__name__ == "Rock":
                point1 = (obstacle.position[0]-camera[0], obstacle.position[1]-camera[1])
                pygame.draw.rect(screen, (100,100,100), (point1, (obstacle.width, obstacle.height)))

        pygame.draw.rect(screen, (255,0,0), ((-camera[0], -camera[1]), mapSize), 3)
        TankPos = systemFont.render( "("+str(round(myTank.position[0],2))+", "+str(round(myTank.position[1],2))+")" , False, (0, 0, 0))
        screen.blit(TankPos, (0, 0))
        pygame.display.flip()


    def Destroy(self, object):
        for i in self.Tanks:
            if id(i) == id(object):
                self.Tanks.remove(object)
                break
        for i in self.Bullets:
            if id(i) == id(object):
                self.Bullets.remove(object)
                break
        for i in self.Naturals:
            if id(i) == id(object):
                self.Naturals.remove(object)


class Bullet:
    def __init__(self, current, angle, speed):

        self.position = current
        self.angle = angle
        self.speed = speed
        self.counter = 0



        # currentMap.Destroy(self)


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


class Tank:
    def __init__(self, health, damage, speed, bspeed, position, isPlayer, rotation=0, rspeed = 3,rpm=180):
        self.health = health
        self.maxhealth = health
        self.damage = damage
        self.speed = speed
        self.bspeed = bspeed
        self.position = position
        self.isPlayer = isPlayer
        self.rotation = rotation
        self.rspeed = rspeed
        self.rpm = rpm
        self.lastFired = 0
    def shoot(self, position, angle, speed):
        newBullet = Bullet(position,angle,speed)
        currentMap.AddObjects([newBullet])

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
    return rot_sprite, rot_sprite.get_rect()

def getCollision(rect, segment):
    a,b = segment[0]
    c,d = segment[1]
    slope = (d-b)/(c-a)
    #getY is slope*(x+a)+b
    #getX is (y-b)/slope + a
    #segment AB(y=rect.top):
    if a <= (rect.top-b)/slope + a <= c or c <= (rect.top-b)/slope + a <= a:
        return True
    if a<= (rect.top-rect.height-b)/slope + a <= c or c <= (rect.top-rect.height-b)/slope + a <= a:
        return True
    if b <= slope*(rect.left+a)+b <= d or d <= slope*(rect.left + a)+b <= b:
        return True
    if b <= slope*(rect.left+rect.width +a)+b <= d or d<=slope*(rect.left+rect.width+a)+b<=b:
        return True
    print("FALSE")
    return False

#_START




currentMap = Map()
#health, damage, speed, bspeed, position, isPlayer
myTank = Tank(100, 100, 100, 10, [(viewSize[0]-tanksize[0])/2,(viewSize[1]-tanksize[1])/2], True,5, 1200)
myTank.rpm = 182
# health, damage, speed, bspeed, position, isPlayer, rotation=0, rspeed = 3,rpm=180
enemyTank = Tank(100,100,100,100,[5,100], False)
objects = [myTank, Tree((0,100)), Rock((10,30)), enemyTank]
for i in range(1000):
    objects.append(Tree([random.randint(0,mapSize[0]), random.randint(0,mapSize[1])]))

currentMap.AddObjects(objects)

while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            break
    keys_pressed = pygame.key.get_pressed()
    interval = myTank.speed/50
    theta = ((myTank.rotation) * 2 * math.pi / 360)
#(myTank.position[0] <= mapSize[0]-interval-tanksize[0]) and (myTank.position[0] >= interval) and (myTank.position[1] >= interval) and (myTank.position[1] <= mapSize[1]-interval-tanksize[1])
    if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
        myTank.rotation -= 1
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:

        myTank.rotation += 1
    xInterval = -1*interval*math.cos(theta)
    yInterval = interval*math.sin(theta)
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        if (myTank.position[0] <= mapSize[0] - xInterval - tanksize[0]) and (myTank.position[0] >= xInterval) and (
                myTank.position[1] >= yInterval) and (myTank.position[1] <= mapSize[1] - yInterval - tanksize[1]):

            myTank.position[0] += xInterval
            myTank.position[1] += yInterval

            camera[0] += xInterval
            camera[1] += yInterval
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:

        if (myTank.position[0] <= mapSize[0] - xInterval - tanksize[0]) and (myTank.position[0] >= xInterval) and (
                myTank.position[1] >= yInterval) and (myTank.position[1] <= mapSize[1] - yInterval - tanksize[1]):
            myTank.position[0] -= xInterval
            myTank.position[1] -= yInterval
            camera[0] -= xInterval
            camera[1] -= yInterval
    if keys_pressed[pygame.K_r]:
        myTank.rotation += 1
    if keys_pressed[pygame.K_SPACE]:

        if pygame.time.get_ticks() - myTank.lastFired >= 60000/myTank.rpm:
            myTank.lastFired = pygame.time.get_ticks()
            myTank.shoot([camera[0]+viewSize[0]/2, camera[1]+viewSize[1]/2], [-1*xInterval/interval, -1*yInterval/interval], myTank.bspeed)
    currentMap.Draw()
    clock.tick(60)
