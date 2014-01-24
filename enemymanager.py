"""
This module handles the spawning of enemies.
"""

import pygame
import pygame.mouse
import enemy
import Queue
import tower
import slowTower
import spreadTower
import gamemap as Map
import maptile
import random

class EnemyManager:

    """
    Global values, because ain't nobody got time for good design in 12 hours.
    """
    TOWER_COST = 50
    SLOW_TOWER_COST = 150
    SPREAD_TOWER_COST = 200

    """
    The event ID for a event to spawn a basic enemy. When a
    basic enemy is scheduled to spawn, an event with this ID
    is posted to the event queue.
    """
    SPAWN_EVENT_BASIC = pygame.USEREVENT

    """
    The time (in milliseconds) at which the last spawning of
    a wave of enemies occurred.
    """
    last_wave_time = 0

    """
    The amount of time between waves.
    """
    wave_interval = 2000

    """
    The number of basic enemies to spawn during a given wave.
    """
    basic_enemies = 1

    """
    The time between spawning two enemies during a wave. This
    is so that enemies don't overlap on the screen.
    """
    spawn_interval = 1500

    """
    The list of enemies in the game.
    """
    enemies = []

    """
    The time at which the last update to enemies occurred.
    """
    last_update_time = pygame.time.get_ticks()

    """
    The sprites of all enemies in the game.
    """
    spritegroup = pygame.sprite.Group()

    """
    The list of towers in the game.
    """
    towers = []
    
    """
    The time at which the last update to towers occurred.
    """
    tower_update_time = pygame.time.get_ticks()

    """
    The sprites of all towers in the game.
    """
    towergroup = pygame.sprite.Group()

    """
    The list of towers in the game.
    """
    spreadTowers = []
    
    """
    The time at which the last update to towers occurred.
    """
    spread_tower_update_time = pygame.time.get_ticks()

    """
    The sprites of all towers in the game.
    """
    spreadtowergroup = pygame.sprite.Group()

    """
    The list of towers in the game.
    """
    slowTowers = []
    
    """
    The time at which the last update to towers occurred.
    """
    slow_tower_update_time = pygame.time.get_ticks()

    """
    The sprites of all towers in the game.
    """
    slowtowergroup = pygame.sprite.Group()

    """
    The priority queue of enemies to be spawned. This queue is arranged
    on the scheduled time for an enemy to spawn. 
    """
    enemy_queue = Queue.PriorityQueue()

    """
    The last time something was spawned.
    """
    last_spawn_time = pygame.time.get_ticks()

    def __init__(self, size):
        self.last_wave_time = pygame.time.get_ticks()
        self.last_update_time = pygame.time.get_ticks()
        self.size = size
        

    """
    Updates the enemies and schedules waves, if necessary. This returns the number
    of enemies that have hit the destination.
    """
    def update(self, mapdata, score):
        retval = 0
        # Update the enemies
        for curr in EnemyManager.enemies:
            curr.update(pygame.time.get_ticks()-self.last_update_time, mapdata)
            if(curr.dead() or curr.offscreen(mapdata)):
                EnemyManager.enemies.remove(curr)
                curr.sprite.kill() # Remove the sprite from the sprite group
                retval += 1
            if(curr.atDestination(mapdata)):
                EnemyManager.enemies.remove(curr)
                curr.sprite.kill()
                retval += 1
        self.last_update_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
	# Update the towers
        for curr in EnemyManager.towers:
            curr.update(pygame.time.get_ticks()-self.last_update_time, mapdata, EnemyManager.enemies)
        self.tower_update_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
	# Update the slowTowers
        for curr in EnemyManager.slowTowers:
            curr.update(pygame.time.get_ticks()-self.last_update_time, mapdata, EnemyManager.enemies)
        self.slowTower_update_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
	# Update the spreadTowers
        for curr in EnemyManager.spreadTowers:
            curr.update(pygame.time.get_ticks()-self.last_update_time, mapdata, EnemyManager.enemies)
        self.spreadTower_update_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        # Spawn enemies that need to be spawned
        spawning = True
        while(spawning and not EnemyManager.enemy_queue.empty()):
            current_enemy = EnemyManager.enemy_queue.get()
            if(current_enemy[0] > current_time): # Then we don't need to spawn yet
                EnemyManager.enemy_queue.put(current_enemy)
                spawning = False
            else:
                EnemyManager.enemies.append(current_enemy[1])

        
        # If enough time has passed, and we're not spawning a wave, spawn a wave
        if(current_time - EnemyManager.last_wave_time >= EnemyManager.wave_interval):
            # Spawn a wave!
            start = mapdata.getStartingTile()
            size = mapdata.getTileSize()
            EnemyManager.last_wave_time = current_time
            for index in range(0, EnemyManager.basic_enemies):
		i = 0
		j = random.randint(1,5)
		if (score >= 50 and score < 100):	
			if (j==5):
				i = 1
		if (score >= 100 and score < 150):
			if (j==4):
				i = 1
			if (j ==5):
				i = 2
		if (score >= 150 and score < 200):
			if (j==3):
				i = 1
			if (j ==4):
				i = 2
			if (j==5):
				i = 3
		if (score >= 200 and score < 250):
			if (j==3 or j==2):
				i = 1
			if (j ==4):
				i = 2
			if (j==5):
				i = 3

		if (score >= 250 and score < 300):
			if (j==2):
				i = 1
			if (j ==4 or j==3):
				i = 2
			if (j==5):
				i = 3

		if (score >= 300):
			if (j==2):
				i = 1
			if (j==3):
				i = 2
			if (j==5 or j==4):
				i = 3
			
                new_enemy = enemy.Enemy(start[0], start[1], EnemyManager.spritegroup, size, i)
                scheduled_time = index*EnemyManager.spawn_interval+current_time
                EnemyManager.enemy_queue.put((scheduled_time, new_enemy))
            # Increase the difficulty!
            #EnemyManager.basic_enemies = 0
        return retval

    """
    Draw all enemies in the game to the screen.
    """
    def draw(self, surface):
        EnemyManager.spritegroup.draw(surface)
	EnemyManager.towergroup.draw(surface)
	EnemyManager.slowtowergroup.draw(surface)
	EnemyManager.spreadtowergroup.draw(surface)

    """
    Given a pygame event from the event queue, spawn an enemy (if necessary).
    The coordinates are the x and y coordinates of the starting tile (a tuple).
    """
    def spawnEnemy(self, event, coordinates):
	i = random.randint(0,3)
        if(event.type == EnemyManager.SPAWN_EVENT_BASIC):
            EnemyManager.enemies.append(enemy.Enemy(coordinates[0], coordinates[1],
                                                 EnemyManager.spritegroup, self.size, i))

    """
    Given a pygame event from the event queue, spawn a tower (if legal).
    Returns cost to resources
    """
    def spawnTower(self, resources, gMap):
	    mouseCoords = pygame.mouse.get_pos()
	    tileCoords = gMap.getTileCoordinates(mouseCoords)
	    if (tileCoords[0] != -1 and tileCoords[1] != -1):
		    tile = gMap.getTile(tileCoords)
		    if (tile.type == maptile.PLOT):
			    legal = True
			    """ Ensure that no two towers can be placed on the same tile"""
			    for placedTower in self.towers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    for placedTower in self.slowTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    for placedTower in self.spreadTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    if legal:
				    pixCoords = gMap.getPixelCoordinates(gMap.getTileCoordinates(mouseCoords))
				    if (resources - EnemyManager.TOWER_COST >= 0):				    
					freshTower = tower.Tower(pixCoords[0], pixCoords[1], EnemyManager.towergroup, self.size)
				    	EnemyManager.towers.append(freshTower)
					return EnemyManager.TOWER_COST
	    return 0

    """
    Given a pygame event from the event queue, spawn a tower (if legal).
    Returns cost to resources
    """
    def spawnSlowTower(self, resources, gMap):
	    mouseCoords = pygame.mouse.get_pos()
	    tileCoords = gMap.getTileCoordinates(mouseCoords)
	    if (tileCoords[0] != -1 and tileCoords[1] != -1):
		    tile = gMap.getTile(tileCoords)
		    if (tile.type == maptile.PLOT):
			    legal = True
			    """ Ensure that no two towers can be placed on the same tile"""
			    for placedTower in self.towers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    for placedTower in self.slowTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    for placedTower in self.spreadTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    if legal:
				    pixCoords = gMap.getPixelCoordinates(gMap.getTileCoordinates(mouseCoords))
				    if (resources - EnemyManager.SLOW_TOWER_COST >= 0):				    
					freshTower = slowTower.SlowTower(pixCoords[0], pixCoords[1], EnemyManager.slowtowergroup, self.size)
				    	EnemyManager.slowTowers.append(freshTower)
					return EnemyManager.SLOW_TOWER_COST
	    return 0

    """
    Given a pygame event from the event queue, spawn a spread tower (if legal).
    Returns cost to resources
    """
    def spawnSpreadTower(self, resources, gMap):
	    mouseCoords = pygame.mouse.get_pos()
	    tileCoords = gMap.getTileCoordinates(mouseCoords)
	    if (tileCoords[0] != -1 and tileCoords[1] != -1):
		    tile = gMap.getTile(tileCoords)
		    if (tile.type == maptile.PLOT):
			    legal = True
			    """ Ensure that no two towers can be placed on the same tile"""
			    for placedTower in self.towers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    for placedTower in self.slowTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    for placedTower in self.spreadTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    legal = False
			    if legal:
				    pixCoords = gMap.getPixelCoordinates(gMap.getTileCoordinates(mouseCoords))
				    if (resources - EnemyManager.SPREAD_TOWER_COST >= 0):				    
					freshTower = spreadTower.SpreadTower(pixCoords[0], pixCoords[1], EnemyManager.spreadtowergroup, self.size)
				    	EnemyManager.spreadTowers.append(freshTower)
					return EnemyManager.SPREAD_TOWER_COST
	    return 0

    """
    Given a pygame event from the event queue, speed up selected tower.
    Returns cost to resources
    """
    def speedUp(self, resources, gMap):
	    mouseCoords = pygame.mouse.get_pos()
	    tileCoords = gMap.getTileCoordinates(mouseCoords)
	    if (tileCoords[0] != -1 and tileCoords[1] != -1):
		    tile = gMap.getTile(tileCoords)
		    if (tile.type == maptile.PLOT):
			    towerOfPower = None
			    towerType = 0
			    for placedTower in self.towers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    towerOfPower = placedTower
					    towerType = 1
			    for placedTower in self.slowTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    towerOfPower = placedTower
					    towerType = 2
			    for placedTower in self.spreadTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    towerOfPower = placedTower
					    towerType = 3
			    if (towerOfPower is not None and towerType != 0):
				base_cost = 0
				if (towerType == 1):
					base_cost = 50
				if (towerType == 2):
					base_cost = 150
				if (towerType == 3):
					base_cost = 200
				if (resources - int(base_cost*towerOfPower.speedUpMult) >= 0):				    
					return int(towerOfPower.speedUp()*base_cost)
	    return 0

    """
    Given a pygame event from the event queue, speed up selected tower.
    Returns cost to resources
    """
    def powerUp(self, resources, gMap):
	    mouseCoords = pygame.mouse.get_pos()
	    tileCoords = gMap.getTileCoordinates(mouseCoords)
	    if (tileCoords[0] != -1 and tileCoords[1] != -1):
		    tile = gMap.getTile(tileCoords)
		    if (tile.type == maptile.PLOT):
			    towerOfPower = None
			    towerType = 0
			    for placedTower in self.towers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    towerOfPower = placedTower
					    towerType = 1
			    for placedTower in self.slowTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    towerOfPower = placedTower
					    towerType = 2
			    for placedTower in self.spreadTowers:
				    prevTileCoords = gMap.getTileCoordinates(placedTower.getCoordinates())
				    if prevTileCoords == tileCoords:
					    towerOfPower = placedTower
					    towerType = 3
			    if (towerOfPower is not None and towerType != 0):
				base_cost = 0
				if (towerType == 1):
					base_cost = 50
				if (towerType == 2):
					base_cost = 150
				if (towerType == 3):
					base_cost = 200
				if (resources - int(base_cost*towerOfPower.powerUpMult) >= 0):				    
					return int(towerOfPower.powerUp()*base_cost)
	    return 0



# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
        

