"""
gamemap.py - Definition of the Map class, which represents the game's map in
memory and contains functions for adding towers and enemies.
"""

import os
import maptile
import pygame
import enemy
from math import floor

class GameMap:

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
    def __init__(self, surface, enemy_man):
        self.level = 0
        self.bg_img = pygame.image.load('images/bg1.png')
        self.bg_img = self.bg_img.convert()
        self.load(self.level, surface, enemy_man)
    
    def load(self, level, surface, enemy_man):
        enemy_lineup = []
        # Read the file in the maps directory with the given name, line by line.
        # The "with" keyword opens the file while handling any exceptions.
        with open(os.path.join("Maps", 'map' + str(level) + ".txt"), "r") as file:
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
                elif index == 2:
                    # Read the enemy queue.
                    line = line.strip()
                    for c in line:
                        c = int(c)
                        if c == enemy.EN_BIRD:
                            enemy_lineup.append(c)
                        elif c == enemy.EN_CROW:
                            enemy_lineup.append(c)
                        elif c == enemy.EN_FINCH:
                            enemy_lineup.append(c)
                #Otherwise we read the line
                else:
                    # Put the line into the tile array
                    for x in range(0, self.numColumns):
                        self.tiles[x][index-3] = maptile.Tile(line[x], x, index-3)
                        # Save the start and the end tiles
                        if(self.tiles[x][index-3].type == maptile.START):
                            self.start = self.tiles[x][index-3]
                        elif(self.tiles[x][index-3].type == maptile.DESTINATION):
                            self.dest = self.tiles[x][index-3]
             # Initialize the tile size
            self.tilewidth = surface.get_width()/self.numColumns
            self.tileheight = surface.get_height()/self.numRows
            if(self.tilewidth < self.tileheight):
                self.tileheight = self.tilewidth
            else:
                self.tilewidth = self.tileheight

            # Add the tiles to a sprite group
            self.spritegroup = pygame.sprite.Group()
            #self.spritegroup.add(self.bg_img)
            size = self.getTileSize()
            for tilelist in self.tiles:
                for tile in tilelist:
                    tile.getSprite(self.spritegroup, size)
        
        index = 0
        current_time = 0
        start = self.getStartingTile()
        size = self.getTileSize()
        en = None
        for e in enemy_lineup:
            if e == enemy.EN_BIRD:
                en = enemy.BirdEnemy
            elif e == enemy.EN_CROW:
                en = enemy.CrowEnemy
            elif e == enemy.EN_FINCH:
                en = enemy.FinchEnemy
            new_enemy = en(start[0], start[1], enemy_man.spritegroup, size)
            scheduled_time = index*enemy_man.spawn_interval+current_time
            enemy_man.enemy_queue.put((scheduled_time, new_enemy))
            index += 1

           
    """
    Draws the map to the screen (passed in as a surface).
    """
    def draw(self, surface):
        surface.blit(self.bg_img, (0,0))
        self.spritegroup.draw(surface)

    """
    Updates the map. Currently this does nothing.
    """
    def update(self):
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
    
    def getPixelCoordinates(self, coordinates):
        return (int(floor(coordinates[0]*self.tilewidth)),
                int(floor(coordinates[1]*self.tileheight)))
    tileToPixelCoords = getPixelCoordinates
    pixelToTileCoords = getTileCoordinates

    """
    Determine if the given tile coordinates (row and column number) are valid.
    """
    def validCoordinates(self, x, y):
        return (x >= 0 and x < self.numColumns and y >= 0 and y < self.numRows)
    
    def getTileByPixels(self, x, y):
        pos = self.pixelToTileCoords((x, y))
        return self.tiles[pos[0]][pos[1]].type
    
    def getTileByCoords(self, x, y):
        return self.tiles[x][y].type
    
    def setTile(self, x, y, tileType):
        self.tiles[x][y].type = tileType
        
# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
        

        
        
        
