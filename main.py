"""
main.py - The entry point into the game. This runs the main game loop.
"""

import pygame
import sys
import gamemap
import os
import gamedata
import userinterface
import enemymanager
import maptile
import random
#from sets import Set


"""
The dimensions for the screen. These should remain constant.
"""
SCREEN_WIDTH = 19 * 32
SCREEN_HEIGHT = 19 * 32

"""
The max number of frames per second for the game.
"""
MAX_FPS = 60

"""
The game clock
"""
GameClock = None

"""
The title of the game. This should remain constant.
"""
TITLE = "Cats"

"""
This performs initial setup of the game. Any global variables
should also be defined here (yes, I know most people say global
variables are bad, but there really isn't a simple solution).
"""
def setup():
   
    # Set the title of the game.
    pygame.display.set_caption(TITLE)
    # Set up a new window.
    global ScreenSurface
    ScreenSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set up the map
    global Map
    # Set up the starting game data
    global Data
    Data = gamedata.GameData()
    # Set up the UI
    global UI
    UI = userinterface.UserInterface()
    Map = gamemap.GameMap("map1", ScreenSurface)
    # Initialize the enemy manager
    global EnemyManager
    EnemyManager = enemymanager.EnemyManager(Map.getTileSize())
    global GameClock
    GameClock = pygame.time.Clock()
    global GameState
    GameState = True
    global characterX
    characterX = 10
    global characterY
    characterY = 10

    global buildMode
    buildMode = 0
    global targetX
    targetX = 0
    global targetY
    targetY = 0

    global time
    time = 0

    global ROUNDS
    ROUNDS = [0, 1, 0, 2, 0, 0, 3, 0, 4, 0, 5, 0, 6, 0, 0, 7, 0]
    global currentRound
    currentRound = 0

    global money
    money = 15
    global lives
    lives = 8

    global facing
    facing = 0

    global ENEMIES
    ENEMIES = []

    global ANIMATIONS
    ANIMATIONS = []
    global buffz
    buffz = 0

    global hitSound
    global buildSound
    global shootSound
    global coinSound
    global loseSound
    hitSound = pygame.mixer.Sound("sound/Hit_Hurt.wav")
    buildSound = pygame.mixer.Sound("sound/Jump.wav")
    shootSound = pygame.mixer.Sound("sound/Laser_Shoot.wav")
    coinSound = pygame.mixer.Sound("sound/Pickup_Coin.wav")
    loseSound = pygame.mixer.Sound("sound/Explosion.wav")

"""
This handles a single pygame event.
"""
def handleEvent(event):
    if(event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
        handleKeyEvent(event)
    if event.type == pygame.QUIT:
        # Quit the program safely
        pygame.quit()
        sys.exit()
    else:
        EnemyManager.spawnEnemy(event, Map.getStartingTile())

"""
This is the main game loop, called as many times as
the computer allows.
"""
def main():
    while(1):
        #Handle the event queue
        event = pygame.event.poll()
        # The event queue returns an event of type NOEVENT if the queue is empty
        while(event.type != pygame.NOEVENT):
            handleEvent(event)
            event = pygame.event.poll()
        # Delete anything already on the surface.
        ScreenSurface.fill((0, 0, 0))
        # update() # Update the game objects
        updateAnimation()
        draw() # Draw all the game objects[0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6]
        pygame.display.flip()

        # Maintain the max frame rate
        GameClock.tick(MAX_FPS)
       

"""
Handles any updating of game objects. This is called
once per game loop.
"""
def update():
    global GameState
    if(GameState):
        # Update the enemies
        # livesLost = EnemyManager.update(Map)
        # Data.lives -= livesLost
        # Update the UI
        # UI.update(Data)
        # Check if the game is over
        if(Data.lives <= 0):
            GameState = False # The game is over
            UI.showDefeat()
       

"""
Draws all game objects to the screen. This is called once
per game loop.
"""
def draw():
    # Draw the map
    Map.draw(ScreenSurface)
    drawMoney()
    # Draw the enemies
    # EnemyManager.draw(ScreenSurface)
    drawEnemies()

    global buffz
    if (buffz <= 0): drawCharacter1()
    drawTowers1()

    drawAnims()

    Map.drawAbove(ScreenSurface)
    
    if (buffz <= 0): drawCharacter2()
    drawTowers2()

    drawGUI()

    buffz -= 1
    
    # Draw the UI
    #UI.draw(ScreenSurface)
    

"""
Handles a single keyboard event (both key down and key up).
The event passed in is assumed to be a key event, or else
nothing happens.
"""
def handleKeyEvent(event):
    global characterX
    global characterY
    global buildMode
    global lives
    if(event.type == pygame.KEYDOWN):
        # If the escape key has been pressed, quit the game safely
        if(event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        prevX = characterX
        prevY = characterY
        if (buildMode == 0 and lives > 0):
            slap = 0
            if (event.key == pygame.K_KP8 or event.key == pygame.K_8):
                characterY -= 1
            elif (event.key == pygame.K_KP7 or event.key == pygame.K_7):
                characterY -= 1
                characterX -= 1
                facing = 0
            elif (event.key == pygame.K_KP2 or event.key == pygame.K_k):
                characterY += 1
            elif (event.key == pygame.K_KP1 or event.key == pygame.K_j):
                characterY += 1
                characterX -= 1
                facing = 0
            elif (event.key == pygame.K_KP3 or event.key == pygame.K_l):
                characterY += 1
                characterX += 1
                facing = 1
            elif (event.key == pygame.K_KP4 or event.key == pygame.K_u):
                characterX -= 1
                facing = 0
            elif (event.key == pygame.K_KP6 or event.key == pygame.K_o):
                characterX += 1
                facing = 1
            elif (event.key == pygame.K_KP9 or event.key == pygame.K_9):
                characterX += 1
                characterY -= 1
                facing = 1
            elif (event.key == pygame.K_KP5 or event.key == pygame.K_i):
                slap = 1
            elif (event.key == pygame.K_SPACE):
                buildMode = 1
            if characterX < 0: characterX = 0
            if characterY < 0: characterY = 0
            if characterX >= 19: characterX = 18
            if characterY >= 19: characterY = 18            


            tile = Map.tiles[characterX][characterY]
            if (tile.above > 0):
                characterX = prevX
                characterY = prevY

            if (tile.tower.t):
                tx = characterX + (characterX - prevX)
                ty = characterY + (characterY - prevY)
                if (tx < 0 or ty < 0 or tx >= 19 or ty >= 19 or Map.tiles[tx][ty].tower.t or Map.tiles[tx][ty].enemy or Map.tiles[tx][ty].above):
                    characterX = prevX
                    characterY = prevY
                else:
                    Map.tiles[tx][ty].tower = tile.tower
                    tile.tower = maptile.Tower(0)

            if (tile.enemy):
                characterX = prevX
                characterY = prevY
                tile.enemy.health -= 1 - tile.enemy.scrape
                global hitSound
                hitSound.play()
                step()
            elif (prevX != characterX or prevY != characterY): step()
            elif (slap): step()

            tile = Map.tiles[characterX][characterY]
            if (tile.money):
                global money
                money += tile.money
                tile.money = 0
                global coinSound
                coinSound.play()

            anim = Animation(2, 1. / float(MAX_FPS) * 4 + .00001, (prevX, prevY), (characterX, characterY))
            anim.imX, anim.imY = 6, 7
            ANIMATIONS.append(anim)
            anim2 = Animation(2, 1. / float(MAX_FPS) * 4 + .00001, (prevX, prevY - 1), (characterX, characterY - 1))
            anim2.imX, anim2.imY = 6, 6
            ANIMATIONS.append(anim2)
        elif (buildMode == 1 and lives > 0):
            if (event.key == pygame.K_SPACE):
                buildMode = 0
            elif (event.key == pygame.K_KP8 or event.key == pygame.K_8):
                buildTower(2, characterX, characterY - 1)
            elif (event.key == pygame.K_KP7 or event.key == pygame.K_7):
                buildTower(1, characterX - 1, characterY - 1)
            elif (event.key == pygame.K_KP2 or event.key == pygame.K_k):
                buildTower(2, characterX, characterY + 1)
            elif (event.key == pygame.K_KP1 or event.key == pygame.K_j):
                buildTower(1, characterX - 1, characterY + 1)
            elif (event.key == pygame.K_KP3 or event.key == pygame.K_l):
                buildTower(1, characterX + 1, characterY + 1)
            elif (event.key == pygame.K_KP4 or event.key == pygame.K_u):
                buildTower(2, characterX - 1, characterY)
            elif (event.key == pygame.K_KP6 or event.key == pygame.K_o):
                buildTower(2, characterX + 1, characterY)
            elif (event.key == pygame.K_KP9 or event.key == pygame.K_9):
                buildTower(1, characterX + 1, characterY - 1)
        elif (buildMode == 2 and lives > 0):
            if (event.key == pygame.K_SPACE):
                buildMode = 0
            elif (event.key == pygame.K_KP8 or event.key == pygame.K_8 or event.key == pygame.K_KP7 or event.key == pygame.K_7):
                upgradeTower(targetX, targetY)
            elif (event.key == pygame.K_KP9 or event.key == pygame.K_9 or event.key == pygame.K_KP6 or event.key == pygame.K_o):
                rightUpgrade(targetX, targetY)
            elif (event.key == pygame.K_KP4 or event.key == pygame.K_u or event.key == pygame.K_KP1 or event.key == pygame.K_j):
                leftUpgrade(targetX, targetY)
            elif (event.key == pygame.K_KP3 or event.key == pygame.K_l or event.key == pygame.K_KP2 or event.key == pygame.K_k):
                destroyTower(targetX, targetY)
                step()

        anim = Animation(2, 1. / float(MAX_FPS) * 4 + .00001, (prevX, prevY), (characterX, characterY))
        anim.imX, anim.imY = 6, 7
        ANIMATIONS.append(anim)
        anim2 = Animation(2, 1. / float(MAX_FPS) * 4 + .00001, (prevX, prevY - 1), (characterX, characterY - 1))
        anim2.imX, anim2.imY = 6, 6
        ANIMATIONS.append(anim2)
    else:
        if(event.type == pygame.KEYUP):
            return # TODO: Add stuff for key up events here

def screenDraw(x, y, imX, imY):
    ScreenSurface.blit(Map.IMAGE, (x * 32, y * 32, 32, 32), (imX * 32, imY * 32, 32, 32))

def drawCharacter1():
    if (buildMode > 0):
        screenDraw(characterX, characterY, 7, 7)
    else:
        screenDraw(characterX, characterY, 6, 7)
        #ScreenSurface.blit(Map.IMAGE, (characterX * 32, characterY * 32, 32, 32), (6 * 32, 7 * 32, 32, 32))
def drawCharacter2():
    ScreenSurface.blit(Map.IMAGE, (characterX * 32, (characterY - 1) * 32, 32, 32), (6 * 32, 6 * 32, 32, 32))

def drawMoney():
    for x in range(0, 20 - 1):
        for y in range(0, 20 - 1):
            soot = Map.tiles[x][y].soot
            if (soot):
                screenDraw(x, y, 4, 4)
            mons = Map.tiles[x][y].money
            if (mons >= 1):
                ScreenSurface.blit(Map.IMAGE, (x * 32 + 12, y * 32 + 12, 8, 10), (6 * 32 + 1, 0, 8, 10))
            if (mons >= 2):
                ScreenSurface.blit(Map.IMAGE, (x * 32 + 18, y * 32 + 18, 8, 10), (6 * 32 + 1, 0, 8, 10))
            if (mons >= 3):
                ScreenSurface.blit(Map.IMAGE, (x * 32 + 10, y * 32 + 18, 8, 10), (6 * 32 + 1, 0, 8, 10))
def drawEnemies():
    global ENEMIES
    global Map
    global buffz
    if (buffz <= 0):
        for enemy in ENEMIES:
            #enemType, foo, position = enemy
            #x, y = position
            ScreenSurface.blit(Map.IMAGE, (enemy.x * 32, enemy.y * 32, 32, 32), (enemy.imX * 32, enemy.imY * 32, 32, 32))
            if (enemy.health < enemy.maxHealth):
                x = enemy.health * 32 / enemy.maxHealth
                pygame.draw.rect(ScreenSurface, pygame.Color(255, 0, 0), (enemy.x * 32, enemy.y * 32 + 1, x, 2))

def drawTowers1():
    global time
    for x in range(0, 20 - 1):
        for y in range(0, 20 - 1):
            tower = Map.tiles[x][y].tower
            if (tower.t == 1 or tower.t == 5 or tower.t == 6):
                if (tower.foom == 1):
                    if (tower.t == 1): screenDraw(x, y, 0 + time % 2, 7)
                    elif (tower.t == 5): screenDraw(x, y, 0 + time % 2, 5)
                    elif (tower.t == 6): screenDraw(x, y, 8 + time % 2, 7)
                else:
                    screenDraw(x, y, 2, 5)
                if (tower.up):
                    screenDraw(x, y, 2, 7)
            elif (tower.t == 2 or tower.t == 3 or tower.t == 4):
                if (tower.up == 0):
                    screenDraw(x, y, 5, 6)
                else:
                    screenDraw(x, y, 5, 7)
            if (tower.t == 2 or tower.t == 3 or tower.t == 4):
                kx = tower.energy * 32 / tower.maxEnergy
                pygame.draw.rect(ScreenSurface, pygame.Color(127, 0, 255), (x * 32, y * 32 + 24, kx, 2))

def drawTowers2():
    for x in range(0, 20 - 1):
        for y in range(0, 20 - 1):
            tower = Map.tiles[x][y].tower
            if (tower.t == 1 or tower.t == 5 or tower.t == 6):
                if (tower.foom == 1):
                    if (tower.t == 1): screenDraw(x, y - 1, 0 + time % 2, 6)
                    elif (tower.t == 5): screenDraw(x, y - 1, 0 + time % 2, 4)
                    elif (tower.t == 6): screenDraw(x, y - 1, 8 + time % 2, 6)
                else:
                    screenDraw(x, y - 1, 2, 4)
            elif (tower.t == 2):
                screenDraw(x, y - 1, 5, 5)
            elif (tower.t == 3):
                screenDraw(x, y - 1, 6, 5)
            elif (tower.t == 4):
                screenDraw(x, y - 1, 4, 5)

class Animation:
    def __init__(self, t, duration, startPos, endPos):
        self.cur = float(0)
        self.duration = duration
        self.x, self.y = startPos
        self.destX, self.destY = endPos
        #self.imX, self.imY = imPpos
        self.t = t
    def draw(self):
        if (self.t == 1):
            dx, dy = float(self.destX - self.x) / float(8), float(self.destY - self.y) / float(8)
            curx, cury = float(self.x), float(self.y)
            for i in range(0, 8):
                curx += dx
                cury += dy
                pygame.draw.rect(ScreenSurface, self.color, (int(curx) - 2, int(cury) - 2, 3, 3))
        elif (self.t == 2):
            foost = float(self.cur) / float(self.duration)
            curx = float(self.destX - self.x) * foost + self.x
            cury = float(self.destY - self.y) * foost + self.y
            ScreenSurface.blit(Map.IMAGE, (int(curx * 32), int(cury * 32), 32, 32), (self.imX * 32, self.imY * 32, 32, 32))

def updateAnimation():
    global ANIMATIONS
    for anim in ANIMATIONS:
        anim.cur += 1. / float(MAX_FPS)
    ANIMATIONS = [x for x in ANIMATIONS if not x.cur >= x.duration]

class Enemy:
    def __init__(self, t):
        self.x = 4
        self.y = 0
        self.dx = 0
        self.dy = 1
        self.t = t
        self.suck = 0
        if (self.t == 4 or self.t == 7): self.suck = 1
        self.scrape = 0
        if (self.t == 5): self.scrape = 1
        self.health = 4
        if (self.t == 1): self.health = 3
        if (self.t == 6 or self.t == 7): self.health = 10
        self.maxHealth = self.health
        self.speed = 1
        if (self.t == 3 or self.t == 7): self.speed = 2

        self.imX, self.imY = 0, 0
        if (self.t == 1): self.imX, self.imY = 0, 3
        elif (self.t == 2): self.imX, self.imY = 1, 3
        elif (self.t == 3): self.imX, self.imY = 2, 3
        elif (self.t == 4): self.imX, self.imY = 3, 3
        elif (self.t == 5): self.imX, self.imY = 3, 4
        elif (self.t == 6): self.imX, self.imY = 3, 5
        elif (self.t == 7): self.imX, self.imY = 2, 8

def absorbSoul(x, y):
    done = 0
    for x0 in range(-2, 3):
        if (done): break
        for y0 in range(-2, 3):
            if (done): break
            x1 = x0 + x
            y1 = y0 + y
            if (x1 >= 0 and x1 < 19 and y1 >= 0 and y1 < 19):
                tower = Map.tiles[x1][y1].tower
                if (tower.t == 5):
                    for a0 in range(-2, 3):
                        if (done): break
                        for b0 in range(-2, 3):
                            a1 = x1 + a0
                            b1 = y1 + b0
                            if (a1 >= 0 and a1 < 19 and a1 >= 0 and a1 < 19):
                                chargeTower = Map.tiles[a1][b1].tower
                                if ((chargeTower.t == 2 or chargeTower.t == 3 or chargeTower.t == 4) and chargeTower.energy < chargeTower.maxEnergy):
                                    chargeTower.energy += 2 + tower.up * 2
                                    if (chargeTower.energy > chargeTower.maxEnergy): chargeTower.energy = chargeTower.maxEnergy
                                    tower.foom = 1
                                    done = 1
                                    break
def step():
    global time
    global ENEMIES
    global characterX
    global characterY
    global currentRound
    global ROUNDS
    global Map
    global lives
    global ANIMATIONS
    global buffz
    time += 1
    buffz = 4

    randomX = random.randint(0, 18)
    randomY = random.randint(0, 18)
    randomTile = Map.tiles[randomX][randomY]
    if (randomTile.burn > 0): randomTile.burn -= 1

    #for enemy in ENEMIES:
    #    if (enemy.health <= 0):
    #        Map.tiles[enemy.x][enemy.y].enemy = 0
    #        if (random.randint(1, 2) == 2): Map.tiles[enemy.x][enemy.y].money += enemy.t / 2 + 1
    #        absorbSoul(enemy.x, enemy.y)
    #ENEMIES[:] = [x for x in ENEMIES if x.health <= 0]
    for enemy in ENEMIES:
        if (enemy.health <= 0):
            Map.tiles[enemy.x][enemy.y].enemy = 0
            if (random.randint(1, 2) == 2): Map.tiles[enemy.x][enemy.y].money += enemy.t / 2 + 1
            absorbSoul(enemy.x, enemy.y)
    ENEMIES[:] = [x for x in ENEMIES if x.health > 0]

    for enemy in ENEMIES:
            prevX, prevY = enemy.x, enemy.y
            for i in range(0, enemy.speed):
                if (enemy.suck):
                    done = 0
                    for x0 in range(-1, 2):
                        if (done): break
                        for y0 in range(-1, 2):
                            x1 = x0 + enemy.x
                            y1 = y0 + enemy.y
                            if (x1 >= 0 and x1 < 19 and y1 >= 0 and y1 < 19):
                                tower = Map.tiles[x1][y1].tower
                                if ((tower.t == 2 or tower.t == 3 or tower.t == 4) and tower.energy > 0):
                                    tower.energy -= 1
                                    done = 1
                                    break
                tope = Map.tiles[enemy.x + enemy.dx][enemy.y + enemy.dy]
                if (tope.grassy == 1):
                    dx1, dy1 = enemy.dy, -enemy.dx
                    dx2, dy2 = -enemy.dy, enemy.dx
                    tope1 = Map.tiles[enemy.x + dx1][enemy.y + dy1]
                    if (tope1.grassy == 0):
                        enemy.dx = dx1
                        enemy.dy = dy1
                    else:
                        enemy.dx = dx2
                        enemy.dy = dy2
                Map.tiles[enemy.x][enemy.y].enemy = 0
                enemy.x += enemy.dx
                enemy.y += enemy.dy
                if (enemy.x == characterX and enemy.y == characterY):
                    characterX -= enemy.dx
                    characterY -= enemy.dy
                if Map.tiles[enemy.x][enemy.y].tower.t > 0: destroyTower(enemy.x, enemy.y)
                if (tope.type == 23):
                    lives = lives - 1
                    global loseSound
                    loseSound.play()
                    if (lives == 0):
                        spark = "You lose! Score: "
                        spark += str(time)
                        print(spark)
                    ENEMIES = [x for x in ENEMIES if not x == enemy]
                    break
                else: Map.tiles[enemy.x][enemy.y].enemy = enemy
            anim = Animation(2, 1. / float(MAX_FPS) * 4 + .00001, (prevX, prevY), (enemy.x, enemy.y))
            anim.imX = enemy.imX
            anim.imY = enemy.imY
            ANIMATIONS.append(anim)

    for x in range(0, 20 - 1):
        for y in range(0, 20 - 1):
            tile = Map.tiles[x][y]
            if (tile.tower.t == 2 or tile.tower.t == 3 or tile.tower.t == 4):
                energyCost = 1
                up = tile.tower.up
                if (tile.tower.t == 3): energyCost = 2
                if (tile.tower.energy < energyCost):
                    if (up):
                        up = 0
                        energyCost -= 1
                    if (tile.tower.energy < energyCost): continue
                done = 0
                spin = 1
                if (tile.tower.t == 4): spin = 2
                for x0 in range(-spin, spin + 1):
                    if (done): break
                    for y0 in range(-spin, spin + 1):
                        if (not (x0 == 0 and y0 == 0)):
                            x1 = x0 + x
                            y1 = y0 + y
                            if (x1 >= 0 and x1 < 19 and y1 >= 0 and y1 < 19):
                                if (Map.tiles[x1][y1].enemy):
                                    Map.tiles[x1][y1].enemy.health -= 1 + up - Map.tiles[x1][y1].enemy.scrape
                                    tile.tower.energy -= energyCost
                                    anim = Animation(1, 0.1, (x * 32 + 16, y * 32 - 6), (x1 * 32 + 16, y1 * 32 + 16))
                                    if (tile.tower.t == 2): anim.color = pygame.Color(127, 0, 255)
                                    elif (tile.tower.t == 3): anim.color = pygame.Color(255, 0, 0)
                                    elif (tile.tower.t == 4): anim.color = pygame.Color(0, 0, 255)
                                    ANIMATIONS.append(anim)
                                    global shootSound
                                    shootSound.play()
                                    if (tile.tower.t != 3):
                                        done = 1
                                        break
                                    else: energyCost = 0
            elif (tile.tower.t == 1):
                done = 0
                tile.tower.foom = 0
                for x0 in range(-2, 3):
                    if (done): break
                    for y0 in range(-2, 3):
                        if (not (x0 == 0 and y0 == 0)):
                            x1 = x0 + x
                            y1 = y0 + y
                            if (x1 >= 0 and x1 < 19 and y1 >= 0 and y1 < 19):
                                tower = Map.tiles[x1][y1].tower
                                if ((tower.t == 2 or tower.t == 3 or tower.t == 4) and tower.energy < tower.maxEnergy):
                                    needed = 3
                                    posXs = [0, 0, 0]
                                    posYs = [0, 0, 0]
                                    for i in range(0, 7):
                                        randx = random.randint(x - 2, x + 2)
                                        randy = random.randint(y - 2, y + 2)
                                        grasses = Map.tiles[randx][randy]
                                        if (grasses.grassy and grasses.burn < 3):
                                            #grasses.burn += 1
                                            needed -= 1
                                            posXs[needed] = randx
                                            posYs[needed] = randy
                                            #tower.energy += .34
                                            if (needed <= 0 or tower.energy >= tower.maxEnergy): break
                                    if (needed <= 0):
                                        for i in range(0, 3):
                                            Map.tiles[posXs[i]][posYs[i]].burn += 1
                                        tile.tower.foom = 1
                                        tower.energy += 1 + tile.tower.up
                                        done = 1
                                        break
            elif (tile.tower.t == 5):
                tile.tower.foom = 0
            elif (tile.tower.t == 6):
                tile.tower.foom = 0
                fork = 3
                if (tile.tower.up): fork = 2
                done = 0
                if (time % fork == 0):
                    for x0 in range(-1, 2):
                        if (done): break
                        for y0 in range(-1, 2):
                            if (not (x0 == 0 and y0 == 0)):
                                x1 = x0 + x
                                y1 = y0 + y
                                if (x1 >= 0 and x1 < 19 and y1 >= 0 and y1 < 19):
                                    tower = Map.tiles[x1][y1].tower
                                    if ((tower.t == 2 or tower.t == 3 or tower.t == 4) and tower.energy < tower.maxEnergy):
                                        tower.energy += 1
                                        tile.tower.foom = 1

    for enemy in ENEMIES:
        if (enemy.health <= 0):
            Map.tiles[enemy.x][enemy.y].enemy = 0
            if (random.randint(1, 2) == 2): Map.tiles[enemy.x][enemy.y].money += enemy.t / 2 + 1
            absorbSoul(enemy.x, enemy.y)
    ENEMIES[:] = [x for x in ENEMIES if x.health > 0]

    f = time % 20
    if (f == 19):
        currentRound += 1
        if currentRound == len(ROUNDS): currentRound -= 1
    if (ROUNDS[currentRound] > 0 and f % 2 == 0):
        enemy = Enemy(ROUNDS[currentRound])
        Map.tiles[enemy.x][enemy.y].enemy = enemy
        ENEMIES.append(enemy)
                                

def drawGUI():
    global lives
    if (buildMode == 1 and lives > 0):
        ScreenSurface.blit(Map.IMAGE, ((characterX - 1) * 32, (characterY - 1) * 32, 96, 96), (0, 0, 96, 96))
    elif (buildMode == 2 and lives > 0):
        ScreenSurface.blit(Map.IMAGE, (targetX * 32, (targetY + 1) * 32, 64, 32), (4 * 32, 2 * 32, 64, 32))
        tower =  Map.tiles[targetX][targetY].tower
        if (tower.up == 0):
            ScreenSurface.blit(Map.IMAGE, ((targetX - 1) * 32, (targetY - 1) * 32, 64, 32), (3 * 32, 0, 64, 32))
        if (tower.t == 1 or tower.t == 2):
            ScreenSurface.blit(Map.IMAGE, ((targetX - 1) * 32, targetY * 32, 32, 64), (3 * 32, 32, 32, 64))
        if (tower.t == 1 or tower.t == 2):
            ScreenSurface.blit(Map.IMAGE, ((targetX + 1) * 32, (targetY - 1) * 32, 32, 64), (5 * 32, 0, 32, 64))
        #destroy
        # upgrade
        # ScreenSurface.blit(Map.IMAGE, ((targetX - 1) * 32, (targetY - 1) * 32, 96, 96), (96, 0, 96, 96))
    for i in range(0, money):
        ScreenSurface.blit(Map.IMAGE, (i * 8 + 2, 2, 8, 10), (6 * 32 + 1, 0, 8, 10))
    for i in range(0, lives / 2):
        ScreenSurface.blit(Map.IMAGE, (i * 8 + 1 + 17 * 32, 15 * 32, 8, 6), (193, 10, 8, 6))
    if lives % 2 == 1 and lives > 0:
        ScreenSurface.blit(Map.IMAGE, ((lives / 2) * 8 + 1 + 17 * 32, 15 * 32, 8, 6), (193, 17, 8, 6))
    if lives == 0:
        ScreenSurface.blit(Map.IMAGE, (19 * 32 / 2 - 70, 19 * 32 / 2 - 47, 140, 94), (258, 2, 140, 94))

def drawAnims():
    global ANIMATIONS
    for anim in ANIMATIONS:
        anim.draw()

def buildTower(towerInd, x, y):
    global money
    global targetX
    global targetY
    global buildMode
    if (Map.tiles[x][y].above > 0):
        buildMode = 0
    elif (Map.tiles[x][y].tower.t > 0):
        buildMode = 2
        targetX = x
        targetY = y
        step()
    else:
        if (Map.tiles[x][y].tower.t == 0):
            if (money >= 4):
                Map.tiles[x][y].tower = maptile.Tower(towerInd)
                money -= 4
        buildMode = 0
        global buildSound
        buildSound.play()
        step()

def upgradeTower(x, y):
    global money
    global buildMode
    cost = 6
    if (Map.tiles[x][y].tower.t == 1 or Map.tiles[x][y].tower.t == 5): cost = 6
    if (money >= cost and Map.tiles[x][y].tower.up == 0):
        money -= cost
        Map.tiles[x][y].tower.up = 1
        global buildSound
        buildSound.play()
    buildMode = 0
    step()

def rightUpgrade(x, y):
    global money
    global buildMode
    global buildSound
    if (money >= 4 and Map.tiles[x][y].tower.t == 2):
        money -= 4
        Map.tiles[x][y].tower.t = 3
        buildSound.play()
    if (money >= 6 and Map.tiles[x][y].tower.t == 1):
        money -= 6
        Map.tiles[x][y].tower.t = 6
        buildSound.play()
    buildMode = 0
    step()

def leftUpgrade(x, y):
    global money
    global buildMode
    global buildSound
    if (money >= 3 and Map.tiles[x][y].tower.t == 2):
        money -= 3
        Map.tiles[x][y].tower.t = 4
        buildSound.play()
    elif (money >= 1 and Map.tiles[x][y].tower.t == 1):
        money -= 1
        Map.tiles[x][y].tower.t = 5
        buildSound.play()
    buildMode = 0
    step()

def destroyTower(x, y):
    global money
    global buildMode
    tile = Map.tiles[x][y]
    tile.soot = 1
    tile.tower = maptile.Tower(0)
    money += 2
    buildMode = 0
    global hitSound
    hitSound.play()
pygame.init()
setup()
main()
