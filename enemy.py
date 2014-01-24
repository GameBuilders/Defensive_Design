"""
enemy.py - The most basic enemy in the game.
"""

import pygame
import os
import Queue
import maptile

DEFAULT_HEALTH = 100
DEFAULT_SPEED = 0.1 # This is in number of pixels per second

# The cardinal directions, used in pathfinding.
DIRECTION_NORTH = 1
DIRECTION_SOUTH = 2
DIRECTION_EAST = 3
DIRECTION_WEST = 4
DIRECTION_NONE = 5

(EN_BIRD,
EN_CROW,
EN_FINCH) = range(3)

class Enemy(object):

    """
    Set to true if the images have been initialized already.
    """
    initialized = False
    
    money = 1

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
        if(not Enemy.initialized): # Load the images
            Enemy.up_image = pygame.image.load(os.path.join("images", "enemies", "crow.png"))
            Enemy.up_image = pygame.transform.scale(Enemy.up_image, size)
            Enemy.down_image = pygame.transform.rotozoom(Enemy.up_image, 180.0, 1.0)
            Enemy.left_image = pygame.transform.rotozoom(Enemy.up_image, 90.0, 1.0)
            Enemy.right_image = pygame.transform.rotozoom(Enemy.up_image, 270.0, 1.0)
        self.health = DEFAULT_HEALTH
        self.speed = DEFAULT_SPEED
        self.size = size
        self.direction = DIRECTION_NONE
        self.sprite = pygame.sprite.Sprite()

    """
    Update the sprite. The time_elapsed parameter is how much time
    has passed since the last update of this sprite. The mapdata
    parameter is a map object.
    """
    def update(self, time_elapsed, mapdata):
        
        deltaY = 0
        deltaX = 0
        # Update depending on the current direction
        if(self.direction == DIRECTION_NORTH):
            deltaY = -self.speed*time_elapsed # Go up the screen
            self.sprite.image = Enemy.up_image
        elif(self.direction == DIRECTION_SOUTH):
            deltaY = self.speed*time_elapsed
            self.sprite.image = Enemy.down_image
        elif(self.direction == DIRECTION_WEST):
            deltaX =-self.speed*time_elapsed
            self.sprite.image = Enemy.left_image
        elif(self.direction == DIRECTION_EAST):
            deltaX = self.speed*time_elapsed
            self.sprite.image = Enemy.right_image
        # If the direction is NONE, do nothing

        # Update the coordinates and rectangle
        self.sprite.rect = self.sprite.rect.move(deltaX, deltaY)

        # If we need to update the direction we're going, do so
        if(self.shouldChangeDirection(mapdata)):            
            self.direction = self.determineDirection(mapdata)

    """
    Determine if we should change direction or not. We change direction
    if we've passed through the tile we're on.
    """
    def shouldChangeDirection(self, mapdata):
        coordinates = self.getCoordinates()
        tile_coord = mapdata.getTileCoordinates(coordinates)
        tile = mapdata.tiles[tile_coord[0]][tile_coord[1]]
        if(self.direction == DIRECTION_NONE):
            return True # Always try to move!
        elif(tile.type == maptile.PLOT): # If we've gone off the path, we need to adjust
            return True
        elif(self.direction == DIRECTION_NORTH):
            # Find the tile below this one
            if(mapdata.validCoordinates(tile_coord[0], tile_coord[1]+1)):
                tile = mapdata.tiles[tile_coord[0]][tile_coord[1]+1]
                if(coordinates[1]+self.size[1] <= tile.y*mapdata.tileheight):
                    return True
            return False
        elif(self.direction == DIRECTION_SOUTH):
            return True
        elif(self.direction == DIRECTION_EAST):
            return True
        elif(self.direction == DIRECTION_WEST):
            # Find the tile to the right of this one
            if(mapdata.validCoordinates(tile_coord[0]+1, tile_coord[1])):
                tile = mapdata.tiles[tile_coord[0]+1][tile_coord[1]]
                if(coordinates[0]+self.size[0] <= tile.x*mapdata.tilewidth):
                    return True
            return False
        else:
            return False

    """
    Figure out which direction we should go. This uses a breadth-first
    search to find the goal. Be careful, this can take a while on open maps.
    """
    def determineDirection(self, mapdata):
        
        tilequeue = Queue.Queue()
        # Get the tile we're on
        pixel_coordinates = self.getCoordinates()
        coordinates = mapdata.getTileCoordinates((pixel_coordinates[0],
                                                  pixel_coordinates[1]))
        start_tile = mapdata.tiles[coordinates[0]][coordinates[1]]
        start_tile.visited = True
        tilequeue.put(start_tile)
        while(not tilequeue.empty()):
            tile = tilequeue.get()
            tile.visited = True
            if(tile.type == maptile.DESTINATION):
                # Go backwards until we hit the tile before the start
                while(tile.parent != None and tile.parent != start_tile):
                    tile = tile.parent
                # Figure out the direction
                retval = self.findDirection(start_tile, tile)
                # Clear the tile list of parent and visited status
                for tilelist in mapdata.tiles:
                    for curr in tilelist:
                        curr.visited = False
                        curr.parent = None
                return retval
            else:
                # Get the row and column numbers
                # Queue the neighboring tiles
                self.addtoQueue(tilequeue, tile.x-1, tile.y, mapdata, tile)
                self.addtoQueue(tilequeue, tile.x+1, tile.y, mapdata, tile)
                self.addtoQueue(tilequeue, tile.x, tile.y+1, mapdata, tile)
                self.addtoQueue(tilequeue, tile.x, tile.y-1, mapdata, tile)
        
                

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
            # Any type greater than 100 refers to a tower.
            # Don't allow walking over it.
            if not tile.visited and tile.type < 100 and tile.type not in [maptile.PLOT]:
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
        

    """
    Determines if an enemy is dead or not.
    """
    def dead(self):
        if(self.health <= 0):
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

class BirdEnemy(Enemy):
    initialized = False
    money = 5
    
    def __init__(my, x, y, group, size):
        super(BirdEnemy, my).__init__(x, y, group, size)
        if not BirdEnemy.initialized:
            BirdEnemy.up_image = pygame.image.load(os.path.join("images", "enemies", "enemy_up.png"))
            BirdEnemy.up_image = pygame.transform.scale(BirdEnemy.up_image, size)
            BirdEnemy.down_image = pygame.image.load(os.path.join("images", "enemies", "enemy_down.png"))
            BirdEnemy.down_image = pygame.transform.scale(BirdEnemy.down_image, size)
            BirdEnemy.left_image = pygame.image.load(os.path.join("images", "enemies", "enemy_left.png"))
            BirdEnemy.left_image = pygame.transform.scale(BirdEnemy.left_image, size)
            BirdEnemy.right_image = pygame.image.load(os.path.join("images", "enemies", "enemy_right.png"))
            BirdEnemy.right_image = pygame.transform.scale(BirdEnemy.right_image, size)
        my.health = 100
        my.speed = 0.175
        my.sprite.image = BirdEnemy.down_image
        my.sprite.rect = pygame.Rect(x, y, size[0], size[1])
        group.add(my.sprite)

    def update(self, time_elapsed, mapdata):
       super(BirdEnemy, self).update(time_elapsed, mapdata)
       # Update depending on the current direction
       if(self.direction == DIRECTION_NORTH):
           self.sprite.image = BirdEnemy.up_image
       elif(self.direction == DIRECTION_SOUTH):
           self.sprite.image = BirdEnemy.down_image
       elif(self.direction == DIRECTION_WEST):
           self.sprite.image = BirdEnemy.left_image
       elif(self.direction == DIRECTION_EAST):
           self.sprite.image = BirdEnemy.right_image

class CrowEnemy(Enemy):
    initialized = False
    money = 15
    
    def __init__(my, x, y, group, size):
        super(CrowEnemy, my).__init__(x, y, group, size)
        if not CrowEnemy.initialized:
            CrowEnemy.up_image = pygame.image.load(os.path.join("images", "enemies", "crow.png"))
            CrowEnemy.up_image = pygame.transform.scale(CrowEnemy.up_image, size)
            CrowEnemy.down_image = pygame.transform.rotozoom(CrowEnemy.up_image, 180.0, 1.0)
            CrowEnemy.left_image = pygame.transform.rotozoom(CrowEnemy.up_image, 90.0, 1.0)
            CrowEnemy.right_image = pygame.transform.rotozoom(CrowEnemy.up_image, 270.0, 1.0)
        my.health = 200
        my.speed = 0.15
        my.sprite.image = CrowEnemy.down_image
        my.sprite.rect = pygame.Rect(x, y, size[0], size[1])
        group.add(my.sprite)

    def update(self, time_elapsed, mapdata):
        super(CrowEnemy, self).update(time_elapsed, mapdata)
        # Update depending on the current direction
        if(self.direction == DIRECTION_NORTH):
            self.sprite.image = CrowEnemy.up_image
        elif(self.direction == DIRECTION_SOUTH):
            self.sprite.image = CrowEnemy.down_image
        elif(self.direction == DIRECTION_WEST):
            self.sprite.image = CrowEnemy.left_image
        elif(self.direction == DIRECTION_EAST):
            self.sprite.image = CrowEnemy.right_image

class FinchEnemy(Enemy):
    initialized = False
    money = 35
    
    def __init__(my, x, y, group, size):
        super(FinchEnemy, my).__init__(x, y, group, size)
        if not FinchEnemy.initialized:
            FinchEnemy.up_image = pygame.image.load(os.path.join("images", "enemies", "finch.png"))
            FinchEnemy.up_image = pygame.transform.scale(FinchEnemy.up_image, size)
            FinchEnemy.down_image = pygame.transform.rotozoom(FinchEnemy.up_image, 180.0, 1.0)
            FinchEnemy.left_image = pygame.transform.rotozoom(FinchEnemy.up_image, 90.0, 1.0)
            FinchEnemy.right_image = pygame.transform.rotozoom(FinchEnemy.up_image, 270.0, 1.0)
        my.health = 450
        my.speed = 0.4
        my.sprite.image = FinchEnemy.down_image
        my.sprite.rect = pygame.Rect(x, y, size[0], size[1])
        group.add(my.sprite)

    def update(self, time_elapsed, mapdata):
        super(FinchEnemy, self).update(time_elapsed, mapdata)
        # Update depending on the current direction
        if(self.direction == DIRECTION_NORTH):
            self.sprite.image = FinchEnemy.up_image
        elif(self.direction == DIRECTION_SOUTH):
            self.sprite.image = FinchEnemy.down_image
        elif(self.direction == DIRECTION_WEST):
            self.sprite.image = FinchEnemy.left_image
        elif(self.direction == DIRECTION_EAST):
            self.sprite.image = FinchEnemy.right_image

# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
    
