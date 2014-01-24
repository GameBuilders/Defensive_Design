"""
squareenemy.py - The most basic enemy in the game.
"""

import pygame
import os
import Queue
import maptile
import random

HEALTH = 100
SIZE = [20,40,60,80]
SPEED = [.08, .06, .02, .01] # This is in number of pixels per second
DIRECTION = [[0,-1],[0,1],[-1,0],[1,0],[1,-1],[-1,-1],[1,1],[-1,1]] #up, down, left, right, ur, ul, dr, dl


class octaEnemy:

    """
    Set to true if the images have been initialized already.
    """
    initialized = False

    """
    Stores the enemy's image file
    """
    enemy_image = None

    """
    Initializes a new enemy at the given x and y coordinates.
    This also adds the enemy's sprite to the given sprite group.
    """
    def __init__(self, x, y, group, size):
	self.deathAnimation = 6
	self.sizeClass = random.randrange(0, 4)
	self.size = [SIZE[self.sizeClass], SIZE[self.sizeClass]]
	self.speed = SPEED[1]
	self.direction = DIRECTION[3] #start right
	self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        if(not octaEnemy.initialized): # Load the images
            octaEnemy.enemy_image = pygame.image.load(os.path.join("images", "Octa_Red.png"))
            octaEnemy.enemy_image = pygame.transform.smoothscale(octaEnemy.enemy_image, self.size)
            octaEnemy.initialized = True
        self.health = HEALTH
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = octaEnemy.enemy_image
        self.sprite.rect = pygame.Rect(x, y, self.size[0], self.size[1])
        group.add(self.sprite)

    """
    Update the sprite. The time_elapsed parameter is how much time
    has passed since the last update of this sprite. The mapdata
    parameter is a map object.
    """
    def update(self, time_elapsed, mapdata):

	curCenter = (self.sprite.rect.centerx,self.sprite.rect.centery)
	if (curCenter[0] > 400 and curCenter[1] > 50 and curCenter[1] < 300 and curCenter[0] < 2000):
		self.health = 0
        deltaY = 0
        deltaX = 0
        # Update depending on the current direction
	deltaY = self.velocity[1] * time_elapsed
	deltaX = self.velocity[0] * time_elapsed

        # Update the coordinates and rectangle
        self.sprite.rect = self.sprite.rect.move(deltaX, deltaY)

        # If we need to update the direction we're going, do so
	self.Movementisvalid = False
	#while(not self.Movementisvalid):
	if(random.randrange(0,100) == 5):
		randDirec = random.randrange(0,100)
        	if(randDirec < 5):            
        		self.direction = DIRECTION[4]
        	elif(randDirec < 15):            
        		self.direction = DIRECTION[6]
        	elif(randDirec < 25):            
        		shrunk = 1#self.direction = DIRECTION[2]
        	elif(randDirec < 60):            
        		self.direction = DIRECTION[3]
        	elif(randDirec < 70):            
        		self.direction = DIRECTION[3]
        	elif(randDirec < 80):            
        		self.direction = DIRECTION[4]
        	elif(randDirec < 90):            
        		self.direction = DIRECTION[6]
        	else:            
        		self.direction = DIRECTION[3]
		self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
		#curCenter = (self.sprite.rect.centerx,self.sprite.rect.centery)
		#nextPos = (16*self.velocity[0]*curCenter[0],16*self.velocity[1]*curCenter[1])
		#nextCoords = mapdata.getTileCoordinates(nextPos)
		#if (not mapdata.tiles[nextCoords[0]][nextCoords[1]].type == 0):
			#self.Movementisvalid = True

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
    Determines if an enemy is dead or not.
    """
    def dead(self):
        if(self.health <= 0):
	    if(self.deathAnimation == 6):
	    	self.deathAnimation -= 1
        	self.sprite.image = pygame.image.load(os.path.join("images", "Explosion.01.png"))
		self.sprite.image = pygame.transform.smoothscale(self.sprite.image, self.size)
                self.velocity = [0,0]
		return False
	    if(self.deathAnimation == 5):
	    	self.deathAnimation -= 1
        	self.sprite.image = pygame.image.load(os.path.join("images", "Explosion.02.png"))
		self.sprite.image = pygame.transform.smoothscale(self.sprite.image, self.size)
                self.velocity = [0,0]
		return False
	    if(self.deathAnimation == 4):
	    	self.deathAnimation -= 1
        	self.sprite.image = pygame.image.load(os.path.join("images", "Explosion.03.png"))
		self.sprite.image = pygame.transform.smoothscale(self.sprite.image, self.size)
                self.velocity = [0,0]
		return False
	    if(self.deathAnimation == 3):
	    	self.deathAnimation -= 1
        	self.sprite.image = pygame.image.load(os.path.join("images", "Explosion.04.png"))
		self.sprite.image = pygame.transform.smoothscale(self.sprite.image, self.size)
                self.velocity = [0,0]
		return False
	    if(self.deathAnimation == 2):
	    	self.deathAnimation -= 1
        	self.sprite.image = pygame.image.load(os.path.join("images", "Explosion.05.png"))
		self.sprite.image = pygame.transform.smoothscale(self.sprite.image, self.size)
                self.velocity = [0,0]
		return False
	    if(self.deathAnimation == 1):
	    	self.deathAnimation -= 1
        	self.sprite.image = pygame.image.load(os.path.join("images", "Explosion.06.png"))
		self.sprite.image = pygame.transform.smoothscale(self.sprite.image, self.size)
                self.velocity = [0,0]
		return False
	    if(self.deathAnimation == 0):
		return True
        else:
            return False

    """
    Determines if the enemy is offscreen or not. This only
    returns true if all parts of the enemy are offscreen.
    """
    def offscreen(self, mapdata):
        tilesize = mapdata.getTileSize()
        mapsize = mapdata.getMapSize()
        coordinates = self.getCoordinates()
        if(coordinates[0] < -tilesize[0] or coordinates[0] > mapsize[0]):
            return True
        elif(coordinates[1] < -tilesize[1] or coordinates[1] > mapsize[1]):
            return True
        else:
            return False

    def getCoordinates(self):
        return (self.sprite.rect.left, self.sprite.rect.top)

    """
    Returns true if the enemy is at the destination.
    """
    def atDestination(self, mapdata):
        coordinates = self.getCoordinates()
        mapsize = mapdata.getMapSize()
        # Make sure the coordinates are valid
        if(coordinates[0] < 0 or coordinates[0] >= mapsize[0] or coordinates[1] < 0
           or coordinates[1] >= mapsize[1]):
            return False        
        tile_number = mapdata.getTileCoordinates(coordinates)
        if(mapdata.tiles[tile_number[0]][tile_number[1]].type == maptile.DESTINATION):
            return True
        else:
            return False

# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")

