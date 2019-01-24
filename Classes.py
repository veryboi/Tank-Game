import pygame
import math
import random
pygame.init()
infoObject = pygame.display.Info()
mapSize = (infoObject.current_w*2, infoObject.current_h*2)
viewSize = ((infoObject.current_w, infoObject.current_h))
screen = pygame.display.set_mode(viewSize, pygame.FULLSCREEN)
camera = [0,0]
clock = pygame.time.Clock()

pygame.font.init()
systemFont = pygame.font.SysFont('Courier New', 10)
tanksize = (50,25)
bluetank = pygame.image.load("tankblue.png")
bluetank = pygame.transform.scale(bluetank, tanksize)
bluetank.convert_alpha()
redtank = pygame.image.load("tankred.png")
redtank = pygame.transform.scale(redtank, tanksize)
redtank.convert_alpha()
bulletImage = pygame.image.load("bullet.png")
bulletImage.convert_alpha()


def intro():
    # pygame.mixr.Sound.play(start_music)
    intro = True
    menu1_x = 200
    menu1_y = 400
    menu2_x = 500
    menu2_y = 400
    menu_width = 100
    menu_height = 50
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        pygame.draw.rect(screen, (255,255,255), (200, 400, 100, 50))
        pygame.draw.rect(screen, (255,255,255), (500, 400, 100, 50))
        font = pygame.font.SysFont("Arial", 72)
        hi1 = font.render(
            "Start", False, (0, 0, 0))
        hi2 = font.render(
            "Quit", False, (0, 0, 0))

        screen.fill((0,255,255))


        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, (0, 255, 255), (200, 400, 100, 50))
        pygame.draw.rect(screen, (0, 255, 255), (500, 400, 100, 50))
        screen.blit(hi1, (200,400))

        screen.blit(hi2, (500, 400))
        # like a hyperlink to the game page
        if menu1_x < mouse[0] < menu1_x + menu_width and menu1_y < mouse[1] < menu1_y + menu_height:
            pygame.draw.rect(screen,(0,0,255),(200,400,100,50))
            if click[0] == 1:
                intro = False
        if menu2_x < mouse[0] < menu2_x + menu_width and menu2_y < mouse[1] < menu2_y + menu_height:
            pygame.draw.rect(screen,(0,0,255),(500,400,100,50))
            if click[0] == 1:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(50)
class Map:
    def __init__(self):
        self.Tanks = []
        self.Bullets = []
        self.Naturals = []
        self.healthb = []
        self.walls =[]
    def AddObjects(self, listofObjects):
        for o in listofObjects:
            if type(o).__name__ == "Tank":
                self.Tanks.append(o)

            elif type(o).__name__ == "Bullet":
                self.Bullets.append(o)
            else:
                self.Naturals.append(o)
    def addHealthBar(self, listofObjects):
        for o in listofObjects:
            self.healthb.append(o)
    def addWalls(self, listofObjects):
        for o in listofObjects:
            self.walls.append(o)

    def Draw(self):
        screen.fill((173,255,47))
        viewport = (camera, (viewSize[0]+camera[0], viewSize[1]+camera[1]))
        for tank in self.Tanks:

                if tank.isPlayer:
                    blueInstance, rect = rotate(bluetank,tank.rotation)


                    screen.blit(blueInstance,[(viewSize[0]-rect.width)/2,(viewSize[1]-rect.height)/2])
                    tank.width,tank.height = rect.width, rect.height
                    tank.hitbox = pygame.Rect(tank.position[0] - rect.width / 2, tank.position[1] - rect.height / 2,
                                              rect.width, rect.height)
                else:

                    redInstance,rect = rotate(redtank,tank.rotation)

                    adjustPosition = [tank.position[0] - camera[0]-rect.width/2, tank.position[1] - camera[1]-rect.height/2]
                    screen.blit(redInstance, adjustPosition)
                    tank.width, tank.height = rect.width, rect.height
                    tank.hitbox = pygame.Rect(tank.position[0]-rect.width/2,tank.position[1]-rect.height/2,rect.width,rect.height)


        for bullet in self.Bullets:
            if bullet.counter < 100:
                for i in self.Naturals + self.Tanks:
                    if type(i).__name__ == "Tree":
                        if getCollision(pygame.Rect(i.position[0]-i.radius, i.position[1]-i.radius, i.radius*2, i.radius*2),(bullet.position, [bullet.position[0] + bullet.angle[0] * bullet.speed / 10,
                                   bullet.position[1] + bullet.angle[1] * bullet.speed / 10])):
                            takeDamage(i, bullet.parent.damage)
                            self.Destroy(bullet)
                    else:
                        if i != bullet.parent:
                            if type(i).__name__=="Rock":
                                if getCollision(pygame.Rect(i.position[0],i.position[1],i.width, i.height), (bullet.position, [bullet.position[0] + bullet.angle[0] * bullet.speed / 10,
                                           bullet.position[1] + bullet.angle[1] * bullet.speed / 10])):
                                    takeDamage(i, bullet.parent.damage)
                                    self.Destroy(bullet)
                            elif type(i).__name__=="Tank":
                                if getCollision(i.hitbox, (
                                bullet.position, [bullet.position[0] + bullet.angle[0] * bullet.speed / 10,
                                                  bullet.position[1] + bullet.angle[1] * bullet.speed / 10])):
                                    takeDamage(i, bullet.parent.damage)
                                    self.Destroy(bullet)

                bullet.position = [bullet.position[0] + bullet.angle[0] * bullet.speed / 10,
                                   bullet.position[1] + bullet.angle[1] * bullet.speed / 10]
                bullet.counter += 1
            else:

                self.Destroy(bullet)

            rotBullet, bulletrect = rotate(bulletImage,bullet.RotAngle)

            adjustPosition = [bullet.position[0] - camera[0]-bulletrect.width/2, bullet.position[1] - camera[1]-bulletrect.height/2]
            screen.blit(rotBullet, adjustPosition)
        for obstacle in self.Naturals:

            if type(obstacle).__name__ == "Tree":

                point1 = (int(obstacle.position[0]+obstacle.radius-camera[0]), int(obstacle.position[1]+obstacle.radius-camera[1]))

                pygame.draw.circle(screen, (0,100,0), point1, int(obstacle.radius))
            elif type(obstacle).__name__ == "Rock":
                point1 = (obstacle.position[0]-camera[0], obstacle.position[1]-camera[1])
                pygame.draw.rect(screen, (100,100,100), (point1, (obstacle.width, obstacle.height)))

        pygame.draw.rect(screen, (255,0,0), ((-camera[0], -camera[1]), mapSize), 3)
        for object in self.healthb:

            redpart = pygame.draw.rect(screen, (255,0,0), ((object.position[0]-camera[0],object.position[1]-camera[1]), (20,2)))
            greenpart = pygame.draw.rect(screen,(0,255,0), ((object.position[0]-camera[0],object.position[1]-camera[1]), (20*object.health/object.maxhealth, 2)))

        TankPos = systemFont.render( "("+str(round(myTank.position[0],2))+", "+str(round(myTank.position[1],2))+")" , False, (0, 0, 0))
        screen.blit(TankPos, (0, 0))
        FPS = systemFont.render("FPS: " + str(round(clock.get_fps(), 2)), False, (0,0,0))
        screen.blit(FPS, (0, 20))
        pygame.display.flip()


    def Destroy(self, object):
        for i in self.healthb:
            if id(i) == id(object):
                self.healthb.remove(object)
                break

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
    def __init__(self, current, angle, speed,parent):

        self.position = current
        self.angle = angle
        self.speed = speed
        self.counter = 0
        self.parent= parent
        self.RotAngle = parent.rotation


        # currentMap.Destroy(self)


class Tree:
    def __init__(self, position):
        self.radius = 5
        self.health = 750
        self.maxhealth = 750
        self.position = position


class Rock:
    def __init__(self, position):
        self.width = 15
        self.height = 15
        self.health = 2000
        self.maxhealth = 2000
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
        self.width = tanksize[0]
        self.height = tanksize[1]
        self.lastFired = 0
        self.hitbox = pygame.Rect(0,0,0,0)
    def shoot(self, position, angle, speed,parent):
        if self.health > 0:
            angleCoord =[ math.cos((-1*angle) * 2 * math.pi / 360), math.sin((-1*angle) * 2 * math.pi / 360)]
            newBullet = Bullet(position,angleCoord,speed, parent)
            currentMap.AddObjects([newBullet])

def destroy(object):
    pass


def takeDamage(object, damage):
    if object.health > damage:
        object.health = object.health - damage
        print(object.health)
        for i in currentMap.healthb:
            if id(i) == id(object):
                return
        currentMap.addHealthBar([object])




    else:
        object.health = 0
        currentMap.Destroy(object)

ending = 0
def rotate(image, angle):
    """rotate a Surface, maintaining position."""

    loc = image.get_rect().center  #rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite, rot_sprite.get_rect()

def getCollision(rect, segment):
    a,b = segment[0]
    c,d = segment[1]
    for i in range(6):
        if rect.collidepoint(a+(a-c)*i/5, b+(b-d)*i/5):
            return True
    return False
def getStraightLineCollision(segment1, segment2):
    #Segment 1 is the straight line, segment 2 can be a tilted line
    a,b = segment1[0]
    c,d = segment1[1]
    w,x = segment2[0]
    y,z = segment2[1]
    print(a, b, c, d)
    print(w, x, y, z)
    ArbRect = pygame.Rect(segment1[0], (abs(a-b), 10))
    repetitions = int(math.sqrt((a-c)**2+(b-d)**2))
    for i in range(repetitions+1):

        if ArbRect.collidepoint(w+(w-y)*i/5, x+(x-z)*i/5):

            return True
    return False

#_START


intro()

currentMap = Map()
#health, damage, speed, bspeed, position, isPlayer
myTank = Tank(1000, 100, 300, 300, [(viewSize[0]-tanksize[0])/2,(viewSize[1]-tanksize[1])/2], True,5, 1200)
myTank.rpm = 300
# health, damage, speed, bspeed, position, isPlayer, rotation=0, rspeed = 3,rpm=180
eTanks = []
objects = [myTank, Tree((0,100)), Rock((10,30))]
for i in range(1  ):
    enemyTank = Tank(1000,100,100,100,[random.randint(0,mapSize[0]),random.randint(0,mapSize[1])], False, rpm = 60)
    objects.append(enemyTank)
    eTanks.append(enemyTank)
for i in range(50):
    if random.randint(0,1):
        objects.append(Tree([random.randint(0,mapSize[0]), random.randint(0,mapSize[1])]))
    else:
        objects.append(Rock([random.randint(0,mapSize[0]), random.randint(0,mapSize[1])]))

currentMap.AddObjects(objects)
currentMap.addWalls([ ( (0,0) , (0, mapSize[1]) ), ( (0,0),(mapSize[0], 0) ), ( (0,mapSize[1]), (mapSize[0], mapSize[1])), ( (mapSize[0], 0), (mapSize[0], mapSize[1]) ) ])
while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            break
    aliveTanks = 0
    for enemyTank in eTanks:
        if enemyTank.health > 0:
            aliveTanks += 1
        if enemyTank.position[0] > myTank.position[0] and enemyTank.position[1] > myTank.position[1]:
            #2nd quadrant
            enemyTank.rotation = 270 -math.asin(abs(myTank.position[1] - enemyTank.position[1]) / (math.sqrt(
                abs(myTank.position[1] - enemyTank.position[1]) ** 2 + abs(
                    myTank.position[0] - enemyTank.position[0]) ** 2))) * 360 / (2 * math.pi) - 90
        elif enemyTank.position[0] > myTank.position[0] and enemyTank.position[1] < myTank.position[1]:
            #2nd quadrant
            enemyTank.rotation = 270 +math.asin(abs(myTank.position[1] - enemyTank.position[1]) / (math.sqrt(
                abs(myTank.position[1] - enemyTank.position[1]) ** 2 + abs(
                    myTank.position[0] - enemyTank.position[0]) ** 2))) * 360 / (2 * math.pi) - 90
        elif enemyTank.position[0] < myTank.position[0] and enemyTank.position[1] < myTank.position[1]:
            enemyTank.rotation = 360-math.asin(abs(myTank.position[1] - enemyTank.position[1]) / (math.sqrt(
                abs(myTank.position[1] - enemyTank.position[1]) ** 2 + abs(
                    myTank.position[0] - enemyTank.position[0]) ** 2))) * 360 / (2 * math.pi)
        else:
            enemyTank.rotation = math.asin(abs(myTank.position[1]-enemyTank.position[1])/(math.sqrt(abs(myTank.position[1]-enemyTank.position[1])**2 + abs(myTank.position[0]-enemyTank.position[0])**2)))*360/(2*math.pi)
        if pygame.time.get_ticks() - enemyTank.lastFired >= 60000/enemyTank.rpm:
            enemyTank.lastFired = pygame.time.get_ticks()
            enemyTank.shoot(enemyTank.position, enemyTank.rotation, 20, enemyTank)
    keys_pressed = pygame.key.get_pressed()
    interval = myTank.speed/50
    theta = ((myTank.rotation) * 2 * math.pi / 360)
    print(aliveTanks)
    if aliveTanks == 0:
        break
    elif myTank.health == 0:
        ending = 1
        break
#(myTank.position[0] <= mapSize[0]-interval-tanksize[0]) and (myTank.position[0] >= interval) and (myTank.position[1] >= interval) and (myTank.position[1] <= mapSize[1]-interval-tanksize[1])
    if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
        myTank.rotation -= 1
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:

        myTank.rotation += 1
    xInterval = -1*interval*math.cos(theta)
    yInterval = interval*math.sin(theta)
    segment2 = (
        (myTank.position[0]-camera[0], myTank.position[1]-camera[1]), (myTank.position[0] + xInterval-camera[0], myTank.position[1] + yInterval-camera[1]))
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        # if (myTank.position[0] <= mapSize[0] - xInterval - tanksize[0]) and (myTank.position[0] >= xInterval) and (
        #         myTank.position[1] >= yInterval) and (myTank.position[1] <= mapSize[1] - yInterval - tanksize[1]):


        # if (myTank.position[0] <= mapSize[0] - xInterval - tanksize[0]) and (myTank.position[0] >= xInterval) and (
        #         myTank.position[1] >= yInterval) and (myTank.position[1] <= mapSize[1] - yInterval - tanksize[1]):
        hitsWall = False
        for segment1 in currentMap.walls:
            if getStraightLineCollision(segment1, segment2):
                hitsWall = True
        if not hitsWall:
            myTank.position[0] += xInterval
            myTank.position[1] += yInterval
            camera[0] += xInterval
            camera[1] += yInterval
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:

    # if (myTank.position[0] <= mapSize[0] - xInterval - tanksize[0]) and (myTank.position[0] >= xInterval) and (
    #         myTank.position[1] >= yInterval) and (myTank.position[1] <= mapSize[1] - yInterval - tanksize[1]):
        hitsWall = False
        for segment1 in currentMap.walls:
            if getStraightLineCollision(segment1, segment2):
                hitsWall = True
                break
        if not hitsWall:
            myTank.position[0] -= xInterval
            myTank.position[1] -= yInterval
            camera[0] -= xInterval
            camera[1] -= yInterval

    if keys_pressed[pygame.K_SPACE]:

        if pygame.time.get_ticks() - myTank.lastFired >= 60000/myTank.rpm:
            myTank.lastFired = pygame.time.get_ticks()
            myTank.shoot([camera[0]+viewSize[0]/2, camera[1]+viewSize[1]/2], myTank.rotation, myTank.bspeed, myTank)

    currentMap.Draw()
    clock.tick(61)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    font = pygame.font.SysFont("Agency FB Bold", 36, True, True)
    if ending == 0:
        endGame = "Game over! You won!"
    else:
        endGame = "Game over! You lost.."
    screen.fill((0,0,0))
    gameover = font.render(endGame, True, (255,255,255))
    screen.blit(gameover, [750,750])
    pygame.display.flip()
