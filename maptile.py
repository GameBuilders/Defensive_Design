# -*- coding: utf-8 -*-
"""
maptile.py - Definition of a map tile. Every map is divided into a grid of
tiles. Tiles can hold an enemy or a tower.
"""

import pygame
import os

"""
Constants used to define the type of map tile this is.
"""
PLOT = 31 # A tower can be built on this tile, and no enemy can access it
PATHVERT = 22 # Enemies can access this tile, and no tower can be built on it
PATHHORZ = 29
PATHUPLEFT = 30
PATHDOWNLEFT = 15
PATHUPRIGHT = 28
PATHDOWNRIGHT = 14

START = 2 # Enemies spawn from this tile, and nothing can be present on it
DESTINATION = 23 # Enemies go towards this tile, and nothing can be present on it

#IMAGE = pygame.image.load(os.path.join("images", "rogueliketowerdefensewithcats.png"))

NOTOWER = 0
GEN = 1
POW = 2
class Tower:
    def __init__(self, t):
        self.t = t
        self.up = 0
        self.energy = 5
        self.maxEnergy = self.energy
        self.foom = 0

class Tile:

    """
    This is the sprite associated with this tile.
    """
    sprite = None
    
    def __init__(self, character, x, y):
        self.x = x
        self.y = y
        self.tower = Tower(NOTOWER)
        self.grassy = 0
        self.above = 0
        self.enemy = 0
        self.money = 0
        self.soot = 0
        self.burn = 0
        self.visited = False # Used in searches
        # Decode the character for the type of the plot
        if(character == "|"):
            self.type = PATHVERT
        elif(character == '-'):
            self.type = PATHHORZ
        elif(character == 'L'):
            self.type = PATHUPRIGHT
        elif(character == 'J'):
            self.type = PATHUPLEFT
        elif(character == '/'):
            self.type = PATHDOWNRIGHT
        elif(character == '\\'):
            self.type = PATHDOWNLEFT
        elif(character == 'S'):
            self.type = START
        elif(character == 'D'):
            self.type = DESTINATION
        elif(character == 'T'):
            self.type = PLOT
            self.grassy = 1
            self.above = 1
        elif(character == 'B'):
            self.type = PLOT
            self.grassy = 1
            self.above = 2
        else:
            self.grassy = 1
            self.type = PLOT # By default we can build towers on it

    def blocks(self):
        if (self.above > 0): return 1
        return 0

    """
    Add the sprite associated with this tile to the group.
    """
    def getSprite(self, group, size):
        """        
        if (self.sprite == None):
            self.sprite = pygame.sprite.Sprite(group)
            self.sprite.image = IMAGE
            width = self.sprite.image.get_width()
            height = self.sprite.image.get_height()
            self.sprite.image = pygame.transform.scale(self.sprite.image, (2, 2))
            self.sprite.rect = pygame.Rect(self.x * 32, self.y * 32, 32, 32) #((self.type % 8) * 32, (self.type / 8) * 32, 32, 32)
        group.add(self.sprite)
        """

        """
        if(self.sprite == None): # Generate the sprite from an image
            self.sprite = pygame.sprite.Sprite(group)
            name = None # The name of the image to use
            if(self.type == START):
                name = "start.png"
            elif(self.type == DESTINATION):
                name = "end.png"
            elif(self.type == PLOT):
                name = "plot.png"

            if (name == None):
		# The os.path.join() function is used for cross platform compatibility
		self.sprite.image = pygame.image.load(os.path.join("images", name))
		self.sprite.image = pygame.transform.scale(self.sprite.image, size)
		# Set the position of the sprite using a rectangle
		width = self.sprite.image.get_width()
		height = self.sprite.image.get_height()
		spriterect = pygame.Rect(self.x*width, self.y*height, width, height)
		self.sprite.rect = spriterect
        # Add the sprite to the sprite group
        group.add(self.sprite)
        """
        
# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
                
