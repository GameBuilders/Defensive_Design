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
import tower
from tower import TOW_BOMB
import bullet
import globalutils
from sfxmanager import SFXManager
from math import sqrt

"""
The dimensions for the screen. These should remain constant.
"""
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

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
TITLE = "Defensive Design"

sfxmanager = None
imageLoader = None

running = True

"""
This performs initial setup of the game. Any global variables
should also be defined here (yes, I know most people say global
variables are bad, but there really isn't a simple solution).
"""
def setup():
    # Set the title of the game.
    pygame.display.set_caption(TITLE)
    # Set up a new window.
    #global sfxmanager
    #sfxman = sfxmanager.SFXManager()
    global ScreenSurface
    ScreenSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set up the map
    global Map
    # Set up the starting game data
    global Data
    Data = gamedata.GameData()
    # Set up the UI
    # Initialize the enemy manager
    global EnemyManager
    EnemyManager = enemymanager.EnemyManager(0)
    global UI
    Map = gamemap.GameMap(ScreenSurface, EnemyManager)
    EnemyManager.size = Map.getTileSize()
    global imageLoader
    imageLoader = globalutils.ImageLoader(Map.getTileSize())
    # Load the tower images.
    tower.load_towers(imageLoader)
    bullet.load_bullets(imageLoader)
    UI = userinterface.UserInterface(Map, imageLoader)
    global GameClock
    GameClock = pygame.time.Clock()

bullets = []

def title_screen(screen):
    running = True
    waiting = True
    pygame.mixer.music.load('music/haydn_7_1.ogg')
    pygame.mixer.music.play()
    title_img = pygame.image.load('images/title.png')
    title_img = title_img.convert()
    screen.blit(title_img, (0, 0))
    pygame.display.flip()
    while running and waiting:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            waiting = False
        pygame.time.wait(1)
    return running

"""
This is the main game loop, called as many times as
the computer allows.
"""
def main():
    global running
    global UI
    global Data
    global sfx
    
    towers = []
    setup()
    
    win_screen_image = pygame.image.load('images/winner.png')
    win_screen_image = win_screen_image.convert_alpha()
    running = title_screen(ScreenSurface)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/tam-g05_loop.ogg')
    pygame.mixer.music.play()
    paused_dt = 0.0
    dt = 0.0
    success_display_time = 0.0
    win_registered = False
    game_win = False
    proceed = False
    level = 0
    
    while(running):
        # Events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if win_registered:
                        proceed = True
                    else:
                        pos = pygame.mouse.get_pos()
                        UI.onClick(pos, Data, towers, sfx)
                elif event.button == 3:
                    #Data.paused = not Data.paused
                    pass
            elif not win_registered:
                    EnemyManager.spawnEnemy(event, Map.getStartingTile())
        
        # Update
        if not Data.paused and not win_registered:
            curr_time = pygame.time.get_ticks()
            success = update(Data, sfx, towers, curr_time, dt)
        
        # Drawing
        # Delete anything already on the surface.
        ScreenSurface.fill((0, 0, 0))
        if game_win:
            ScreenSurface.blit(win_screen_image, (0, 0))
        else:
            draw() # Draw all the game objects
            for tower in towers:
                ScreenSurface.blit(tower.image, tower.rect)
        pygame.display.flip()
        
        # Maintain the max frame rate
        dt = GameClock.tick(MAX_FPS)
        if Data.paused:
            paused_dt += dt
        # Check if there are no more enemies
        if len(EnemyManager.enemies) == 0 and Data.lives > 0:
            success_display_time += dt
            if success_display_time > 5500.0:
                proceed = True
                success_display_time = 0.0
            elif success_display_time > 1500.0:
                UI.showWin(True)
                win_registered = True
        else:
            UI.showWin(False)
        
        if proceed:
            # It's been displayed too long. Increment the level.
            proceed = False
            UI.showWin(False)
            win_registered = False
            level += 1
            if level <= 2:
                towers = []
                bullets = []
                Map.load(level, ScreenSurface, EnemyManager)
            else:
                game_win = True
    pygame.quit()

"""
Handles any updating of game objects. This is called
once per game loop.
"""
def update(gamedata, sfx, towers, dt=0.0, passed_time=0.0):
    # Update the towers
    kill_towers = []
    for tower in towers:
        tower.update()
        if not tower.canShoot():
            continue
        x1 = tower.rect.x
        y1 = tower.rect.y
        least_dist = tower.sight_range
        target_idx = None
        for i in range(len(EnemyManager.enemies)):
            enemy = EnemyManager.enemies[i]
            x2 = enemy.sprite.rect.x
            y2 = enemy.sprite.rect.y
            dist = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
            if dist < least_dist:
                dist = least_dist
                target_idx = i
        if target_idx is not None:
            enemy = EnemyManager.enemies[target_idx]
            if tower.form == TOW_BOMB:
                for enemy in EnemyManager.enemies:
                    enemy.health = 0
                kill_towers.append(tower)
            else:
                tower.shoot(enemy, enemy.sprite.rect, bullets)
                sfx.play('shoot')
    for tower in kill_towers:
        towers.remove(tower)

    dead_bullets = []
    for bullet in bullets:
        bullet.update(passed_time)
        if bullet.dead:
            enemy = bullet.target
            if enemy is not None:
                pre_health = enemy.health
                enemy.health -= bullet.DAMAGE
                if pre_health > 0 and enemy.dead():
                    # Get money, because this shot killed the enemy.
                    gamedata.resources += enemy.money
                    sfx.play('foe_exploded')
                else:
                    sfx.play('foe_damaged')
            dead_bullets.append(bullet)
    for bullet in dead_bullets:
        bullets.remove(bullet)

    # Update the enemies
    livesLost = EnemyManager.update(Map, dt)
    Data.lives -= livesLost
    # Update the UI
    UI.update(Data)
    
    # Check if the game is over
    if(Data.lives <= 0):
        UI.showDefeat()
        UI.showWin(False)
        return False
    return False

"""
Draws all game objects to the screen. This is called once
per game loop.
"""
def draw():
    # Draw the map
    Map.draw(ScreenSurface)
    # Draw the enemies
    EnemyManager.draw(ScreenSurface)
    # Draw the UI
    UI.draw(ScreenSurface)
    for b in bullets:
        b.draw(ScreenSurface)

pygame.mixer.quit()
pygame.mixer.pre_init(44100, -16, 2, 65536)
pygame.init()

sfx = SFXManager()
#setup()
main()
