'''
Created on Nov 16, 2013

@author: zeno
'''
import pygame
class towerType:
    '''
    classdocs
    '''
    image = None
    imageName = []
    type = 0
    cost = 0
    damage = 0
    cooldown = 0
    towerRange = 0
    special = ""
    

    def __init__(self, t):
        '''
        Constructor
        '''
        self.type = t  
        self.draw()     
       
        
    def draw(self):
        if(self.type < len(self.imageName)): 
            self.image = pygame.image.load(self.imageName[self.type]).convert()
        if(self.type == 0):
            self.cost = 1
            self.range = 5
            self.damage = 3
            self.cooldown = 12
            self.special = ""
        elif(self.type == 1):
            self.cost = 1
            self.range = 7
            self.damage = 2
            self.cooldown = 9
            self.special = ""
        elif(self.type == 2):
            self.cost = 1
            self.range = 3
            self.damage = 6
            self.cooldown = 10
            self.special = ""
        elif(self.type == 3):
            self.cost = 2
            self.range = 4
            self.damage = 2
            self.cooldown = 13
            self.special = "Multishot"
        elif(self.type == 4):
            self.cost = 2
            self.range = 5
            self.damage = 10
            self.cooldown = 23
            self.special = ""
        elif(self.type == 5):
            self.cost = 2
            self.range = 11
            self.damage = 4
            self.cooldown = 13
            self.special = ""
        elif(self.type == 6):
            self.cost = 2
            self.range = 7
            self.damage = 5
            self.cooldown = 12
            self.special = ""
        elif(self.type == 7):
            self.cost = 3
            self.range = 5
            self.damage = 9
            self.cooldown = 12
            self.special = ""
        elif(self.type == 8):
            self.cost = 3
            self.range = 7
            self.damage = 5
            self.cooldown = 7
            self.special = ""
        elif(self.type == 9):
            self.cost = 3
            self.range = 7
            self.damage = 3
            self.cooldown = 15
            self.special = "Slow"
        elif(self.type == 10):
            self.cost = 4
            self.range = 7
            self.damage = 2
            self.cooldown = 2
            self.special = ""
        elif(self.type == 11):
            self.cost = 4
            self.range = 12
            self.damage = 4
            self.cooldown = 6
            self.special = ""
        elif(self.type == 12):
            self.cost = 4
            self.range = 11
            self.damage = 5
            self.cooldown = 10
            self.special = "Draw a card"
        elif(self.type == 13):
            self.cost = 5
            self.range = 10
            self.damage = 6
            self.cooldown = 10
            self.special = ""
        elif(self.type == 14):
            self.cost = 5
            self.range = 14
            self.damage = 3
            self.cooldown = 15
            self.special = "Slow"
        elif(self.type == 15):
            self.cost = 5
            self.range = 7
            self.damage = 3
            self.cooldown = 10
            self.special = "Multishot"
        elif(self.type == 16):
            self.cost = 6
            self.range = 7
            self.damage = 15
            self.cooldown = 12
            self.special = ""
        elif(self.type == 17):
            self.cost = 6
            self.range = 8
            self.damage = 20
            self.cooldown = 19
            self.special = ""
        elif(self.type == 18):
            self.cost = 6
            self.range = 6
            self.damage = 2
            self.cooldown = 15
            self.special = "Multishot Slow"
        elif(self.type == 19):
            self.cost = 6
            self.range = 15
            self.damage = 7
            self.cooldown = 10
            self.special = ""
            