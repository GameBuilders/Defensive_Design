'''
Created on Nov 16, 2013

@author: zeno
'''
from cardType import cardType
import os
import pygame

"""
The size of the font to use in the user interface
"""
FONT_SIZE = 15

"""
The number of pixels of padding to use between the font
and the screen.
"""
FONT_PADDING = 10

"""
The color of the font (this is an RGB value)
"""
FONT_COLOR = (0, 0, 0)

"""
The color used for the background behind the font.
"""
FONT_BACKGROUND = (255, 255, 255, 0)

"""
The number of pixels between two lines of text on the screen.
"""
FONT_LINESPACE = 4

class card:
    '''
    classdocs
    '''

    
    
    def __init__(self, ctype):
        '''
        Constructor
        '''
        self.ctype = ctype
        self.images = []
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("UI", "larabie.ttf"), FONT_SIZE, )
        self.images.append(pygame.image.load("images/Card.png"))
        self.position = (-1, -1)
        self.onScreen = False
    
    def draw(self, surface):
        self.font = pygame.font.Font(os.path.join("UI", "larabie.ttf"), FONT_SIZE, )
        manaCostText = self.font.render(str(cardType.Cost[self.ctype]), True, FONT_COLOR, FONT_BACKGROUND)
        DamageText = self.font.render(str(cardType.Damage[self.ctype]), True, FONT_COLOR, FONT_BACKGROUND)
        RangeText = self.font.render(str(cardType.Range[self.ctype]), True, FONT_COLOR, FONT_BACKGROUND)
        CooldownText = self.font.render(str(cardType.Cooldown[self.ctype]), True, FONT_COLOR, FONT_BACKGROUND)

        surface.blit(self.images[0], (self.position[0], self.position[1]))    #base image
        
        image = pygame.image.load(cardType.imageName[self.ctype]).convert()
        image = pygame.transform.scale(image, (40, 37))
        surface.blit(image, (self.position[0] + 30 , self.position[1] + 32))

        surface.blit(manaCostText, (self.position[0] + 46, self.position[1] + 5))
        surface.blit(DamageText, (self.position[0] + 76, self.position[1] + 110))
        surface.blit(RangeText, (self.position[0] + 46, self.position[1] + 110))
        surface.blit(CooldownText, (self.position[0] + 16, self.position[1] + 110))


    def click_on(self, x, y):
        if(not self.onScreen):
            return False
        if(x > self.position[0] and y > self.position[1] and x < self.position[0] + 100 and y < self.position[1] + 133):
            return True
        return False
    
        
