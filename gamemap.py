"""
gamemap.py - Definition of the Map class, which represents the game's map in
memory and contains functions for adding towers and enemies.
"""

import os
import maptile
import pygame
from math import floor
from tower import tower

class GameMap:
    mySurface = None
    """
    Constructor for the map class. This is called when a map is
    instantiated (declared in a program). This constructor requires
    the name of the map, which corresponds to a .txt file in the
    Maps directory.

    The map files are formatted as follows: The first integer is the
    number of rows in the map, and the second integer is the number
    of columns. The remaining characters represent the map itself:
    # = Spot where towers can be placed (and no enemies can step on)
    . = Spot where enemies can step on (and no towers can be placed)
    S = Where the enemies start coming in
    D = Where the enemies leave the map (their objective).
    """
    def __init__(self, mapname, surface):
        self.towers = []
        self.mySurface = surface
        # Read the file in the maps directory with the given name, line by line.
        # The "with" keyword opens the file while handling any exceptions.
        with open(os.path.join("Maps", mapname + ".txt"), "r") as file:
            for index, line in enumerate(file):
                # If this is the first line, we store it as numRows
                if(index == 0):
                    self.numRows = int(line)
                # If this is the second line, we store it as numColumns
                # and initialize the tile list
                elif(index == 1):
                    self.numColumns = int(line)
                    # The tile list is a 2 dimensional list
                    self.tiles = [[None for idx in range(0, self.numColumns)]
                                  for idx in range(0, self.numRows)]
                #Otherwise we read the line
                else:
                    # Put the line into the tile array
                    for x in range(0, self.numColumns):
                        self.tiles[x][index-2] = maptile.Tile(line[x], x, index-2)
                        # Save the start and the end tiles
                        if(self.tiles[x][index-2].type == maptile.START):
                            self.start = self.tiles[x][index-2]
                        elif(self.tiles[x][index-2].type == maptile.DESTINATION):
                            self.dest = self.tiles[x][index-2]
             # Initialize the tile size
            self.tilewidth = surface.get_width()/self.numColumns
            self.tileheight = (surface.get_height() - 133)/self.numRows
	    
            if(self.tilewidth < self.tileheight):
                self.tileheight = self.tilewidth
            else:
                self.tilewidth = self.tileheight
            print self.tilewidth, self.tileheight
            # Add the tiles to a sprite group
            self.spritegroup = pygame.sprite.Group()
            size = self.getTileSize()
            for tilelist in self.tiles:
                for tile in tilelist:
                    tile.getSprite(self.spritegroup, size)

           
    """
    Draws the map to the screen (passed in as a surface).
    """
    def draw(self, surface):
        self.spritegroup.draw(surface)

    """
    Updates the map. Currently this does nothing.
    """
    def update(self, surface):
            self.spritegroup = pygame.sprite.Group()
            size = self.getTileSize()

            for tilelist in self.tiles:
                for tile in tilelist:
                    tile.getSprite(self.spritegroup, size)
	    self.spritegroup.draw(surface)
            return

    """
    Get the starting tile for the map (where the enemies come in from).
    This returns a tuple (x, y).
    """
    def getStartingTile(self):
        return (self.start.x*self.start.sprite.image.get_width(),
                self.start.y*self.start.sprite.image.get_height())

    def getDestinationTile(self):
        return (self.dest.x, self.dest.y)

    def getTileSize(self):
        return (self.tilewidth, self.tileheight)

    def getMapSize(self):
        return (self.tilewidth*self.numColumns, self.tileheight*self.numRows)

    """
    Get the row and column number of the tile associated with the
    given coordinates.
    """
    def getTileCoordinates(self, coordinates):
        return (int(floor(coordinates[0]/self.tilewidth)),
                int(floor(coordinates[1]/self.tileheight)))

    """
    Determine if the given tile coordinates (row and column number) are valid.
    """
    def validCoordinates(self, x, y):
        return (x >= 0 and x < self.numColumns and y >= 0 and y < self.numRows)

    def checkIfCanPlace(self, x, y):
    	for tower in self.towers:
    		if((tower.xCoord/51 == x) and (tower.yCoord/51 == y)):
    			return False
    	if((x==4) and((y == 0) or (y == 1) or (y == 2))):
    		return False
    	if((x == 2) and ((y == 4) or (y == 5) or (y == 6))):
    		return False
    	if((x == 6) and ((y <= 9) and (y >= 6))):
    		return False
    	if((x == 6) and ((y==2) or (y == 3) or (y == 4))):
    		return False
    	if(((y == 4) or (y == 6)) and ((x >=2) and (x <= 6))):
    		return False
    	return True

    def placeTowerAt(self, x, y, towerType):
        x = int(x/51)
        y = int(y/51)
        if(self.checkIfCanPlace(x, y) == True):
            t = tower(towerType) #todo change
            t.pos(x, y)	
            self.towers.append(t)
            self.tiles[x][y] = maptile.Tile("T", x,y)
            self.update(self.mySurface)
            return towerType

        
# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
        

        
        
        
