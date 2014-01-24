"""
tower.py - The most basic tower in the game.
"""

import pygame
import os
import Queue
import maptile
import gamemap as Map
import enemy

DEFAULT_POWER = 40
DEFAULT_DELAY = 1000.0 # This is the delay between shots in millis

# The cardinal directions, used in pathfinding.
DIRECTION_NORTH = 1
DIRECTION_SOUTH = 2
DIRECTION_EAST = 3
DIRECTION_WEST = 4
DIRECTION_NONE = 5

class Tower:

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
        if(not Tower.initialized): # Load the images
            Tower.up_image = pygame.image.load(os.path.join("images", "magnifying_glass.png"))
            Tower.up_image = pygame.transform.scale(Tower.up_image, size)
            Tower.down_image = pygame.image.load(os.path.join("images", "magnifying_glass.png"))
            Tower.down_image = pygame.transform.scale(Tower.down_image, size)
            Tower.left_image = pygame.image.load(os.path.join("images", "magnifying_glass.png"))
            Tower.left_image = pygame.transform.scale(Tower.left_image, size)
            Tower.right_image = pygame.image.load(os.path.join("images", "magnifying_glass.png"))
            Tower.right_image = pygame.transform.scale(Tower.right_image, size)
            Tower.initialized = True
        self.power = DEFAULT_POWER
        self.delay = DEFAULT_DELAY
        self.sprite = pygame.sprite.Sprite()
        self.direction = DIRECTION_NONE
        self.sprite.image = Tower.down_image
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
            self.sprite.image = Tower.up_image
        elif(self.direction == DIRECTION_SOUTH):
            self.sprite.image = Tower.down_image
        elif(self.direction == DIRECTION_WEST):
            self.sprite.image = Tower.left_image
        elif(self.direction == DIRECTION_EAST):
            self.sprite.image = Tower.right_image
        # If the direction is NONE, do nothing

	self.getTarget(mapdata, enemies)
	self.shoot()

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
			self.sprite.image = Tower.left_image
    
    """
    Shoot at an enemy, if a target is selected
    """
    def shoot(self):
	    if self.target is not None and (pygame.time.get_ticks() - self.lastShotFired) > self.delay:
  		pygame.mixer.music.load('jump.wav')
		self.target.health = self.target.health - self.power
		pygame.mixer.music.play(0)
		self.lastShotFired = pygame.time.get_ticks()    
		self.sprite.image = Tower.right_image
		coordinates = self.getCoordinates()
		targetCoord = self.target.getCoordinates()
		green = [ 0,255, 0]
		screen = pygame.display.set_mode((1000, 800))
#		background = pygame.Surface(screen.get_size())
#		background = background.convert()
#		background.fill((250, 250, 250))

		pygame.display.set_caption('Hello World!')

		alphasurface = screen.convert_alpha()

		alphasurface.fill((0,0,0,0))    # clear the drawing surface
		pygame.draw.line(screen,green,[coordinates[0],coordinates[1]],[targetCoord[0],targetCoord[1]],5)
		#rrect = pygame.draw.rect(alphasurface, (30,30,30,200), pygame.Rect(20,20,100,40))     # draw a rectangle  

		pygame.display.update(pygame.Rect(0, 0,coordinates[0] + targetCoord[0], coordinates[1] + targetCoord[1]) )

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
    
