"""
slowSlowTower.py - Slows down enemies in range
"""

import pygame
import os
import Queue
import maptile
import gamemap as Map
import enemy

DEFAULT_POWER = 2
DEFAULT_DELAY = 10000.0 # This is the delay between shots in millis

# The cardinal directions, used in pathfinding.
DIRECTION_NORTH = 1
DIRECTION_SOUTH = 2
DIRECTION_EAST = 3
DIRECTION_WEST = 4
DIRECTION_NONE = 5

class SlowTower:

    """
    Set to true if the images have been initialized already.
    """
    initialized = False

    """
    The images to use when going the given direction. These are kept as
    static variables to be drawn when needed.
    """
    up_image = None
    down_image = None
    left_image = None
    right_image = None

    """
    Initializes a new enemy at the given x and y coordinates.
    This also adds the enemy's sprite to the given sprite group.
    """
    def __init__(self, x, y, group, size):
        if(not SlowTower.initialized): # Load the images
            SlowTower.up_image = pygame.image.load(os.path.join("images", "bee.png"))
            SlowTower.up_image = pygame.transform.scale(SlowTower.up_image, size)
            SlowTower.down_image = pygame.image.load(os.path.join("images", "bee.png"))
            SlowTower.down_image = pygame.transform.scale(SlowTower.down_image, size)
            SlowTower.left_image = pygame.image.load(os.path.join("images", "bee.png"))
            SlowTower.left_image = pygame.transform.scale(SlowTower.left_image, size)
            SlowTower.right_image = pygame.image.load(os.path.join("images", "bee.png"))
            SlowTower.right_image = pygame.transform.scale(SlowTower.right_image, size)
            SlowTower.initialized = True
        self.power = DEFAULT_POWER
        self.delay = DEFAULT_DELAY
        self.sprite = pygame.sprite.Sprite()
        self.direction = DIRECTION_NONE
        self.sprite.image = SlowTower.down_image
        self.size = size
        self.sprite.rect = pygame.Rect(x, y, size[0], size[1])
	self.lastShotFired = pygame.time.get_ticks()
	self.powerUpMult = 0.5
	self.speedUpMult = 0.7
        group.add(self.sprite)

    def powerUp(self):
	self.power += 5
	self.powerUpMult += 0.1
	return (self.powerUpMult - 0.1)

    def speedUp(self):
	if(self.delay > 100):
		self.delay -= 100
		self.speedUpMult += 0.1
		return (self.speedUpMult - 0.1)
	return (self.speedUpMult + 0.1)

    def distance_squared(self, p1, p2):
    	return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

    """
    Update the sprite. The time_elapsed parameter is how much time
    has passed since the last update of this sprite. The mapdata
    parameter is a map object.
    """
    def update(self, time_elapsed, mapdata, enemies):

        # Update depending on the current direction
        if(self.direction == DIRECTION_NORTH):
            self.sprite.image = SlowTower.up_image
        elif(self.direction == DIRECTION_SOUTH):
            self.sprite.image = SlowTower.down_image
        elif(self.direction == DIRECTION_WEST):
            self.sprite.image = SlowTower.left_image
        elif(self.direction == DIRECTION_EAST):
            self.sprite.image = SlowTower.right_image
        # If the direction is NONE, do nothing

	self.getTarget(mapdata, enemies)
	self.shootAOE(mapdata, enemies)

    """
    Figure out which enemy to shoot at, if any
    """
    def getTarget(self, mapdata, enemies):
	self.target = None
	coordinates = self.getCoordinates()
        for curr in enemies:
		targCoords = mapdata.getTileCoordinates(curr.getCoordinates())
		towerCoords = mapdata.getTileCoordinates(self.getCoordinates())
		if self.distance_squared(targCoords, towerCoords) <= 2:
			self.target = curr
			self.sprite.image = SlowTower.left_image
    
    """
    Shoot at all enemies in range with slow effect, if a target is selected
    """
    def shootAOE(self, mapdata, enemies):
	    if self.target is not None and (pygame.time.get_ticks() - self.lastShotFired) > self.delay:
		effected = []
		coordinates = self.getCoordinates()
        	for curr in enemies:
			targCoords = mapdata.getTileCoordinates(curr.getCoordinates())
			towerCoords = mapdata.getTileCoordinates(self.getCoordinates())
			if self.distance_squared(targCoords, towerCoords) <= 2 and curr.speed >= enemy.DEFAULT_SPEED:
				effected.append(curr)
		for victim in effected:
			victim.speed /= 2
		self.lastShotFired = pygame.time.get_ticks()

    """
    Add the tile to the queue if the coordinates given are valid
    and if the tile hasn't been visited yet.
    """
    def addtoQueue(self, queue, x, y, mapdata, parent):
        # Make sure the coordinates are valid
        mapsize = mapdata.getMapSize()
        if(x >= 0 and x < mapdata.numColumns and y >= 0 and y < mapdata.numRows):
            tile = mapdata.tiles[x][y]
            # If this tile hasn't been visited yet, and it's not a plot, add it
            if(not tile.visited and tile.type != maptile.PLOT):
                # Update the parent
                tile.parent = parent
                queue.put(tile)

    """
    Find the direction from the first tile to the second tile.
    The tiles have to be adjacent for this to work.
    """
    def findDirection(self, first_tile, second_tile):
        if(first_tile.x > second_tile.x):
            return DIRECTION_WEST
        elif(first_tile.x < second_tile.x):
            return DIRECTION_EAST
        elif(first_tile.y > second_tile.y):
            return DIRECTION_NORTH
        elif(first_tile.y < second_tile.y):
            return DIRECTION_SOUTH
        else:
            return DIRECTION_NONE

    def getCoordinates(self):
        return (self.sprite.rect.left, self.sprite.rect.top)

# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
    
