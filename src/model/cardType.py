'''
Created on Nov 16, 2013

@author: zeno
'''
import pygame
import towerType
class cardType:
    '''
    classdocs
    '''

    image = None
    imageName = []
    isTower = False
    tType = None
    effects = []
    
    def __init__(self, it, tT):
        '''
        Constructor
        Set up the images for each card and make it of a certain tower type        
        '''
        self.isTower = it
        #if it's a tower, then it gets the tower type
        if(self.isTower == True):
            self.tType = tT
        
    
    def draw(self):
        if(self.tType != None):            
            self.image = pygame.image.load(self.tType.type).convert()
            