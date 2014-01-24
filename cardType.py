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
    baseImage = "images/Card.png"
    isTower = False
    tType = None
    effects = []
    Cost = [1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6]
    Range = [5, 7, 3, 4, 5, 11, 7, 5, 7, 7, 7, 12, 11, 10, 14, 7, 7, 8, 6, 15]
    Damage = [3, 2, 6, 2, 10, 4, 5, 9, 5, 3, 2, 4, 5, 6, 3, 3, 15, 20, 2, 7]
    Cooldown = [12, 9, 10, 13, 23, 13, 12, 12, 7, 15, 2, 6, 10, 10, 15, 10, 12, 19, 15, 10]
    imageName.append("Symbols/symbol_1.png")
    imageName.append("Symbols/symbol_2.png")
    imageName.append("Symbols/symbol_3.png")
    imageName.append("Symbols/symbol_4.png")
    imageName.append("Symbols/symbol_5.png")
    imageName.append("Symbols/symbol_6.png")
    imageName.append("Symbols/symbol_7.png")
    imageName.append("Symbols/symbol_8.png")
    imageName.append("Symbols/symbol_9.png")
    imageName.append("Symbols/symbol_10.png")
    imageName.append("Symbols/symbol_11.png")
    imageName.append("Symbols/symbol_12.png")
    imageName.append("Symbols/symbol_13.png")
    imageName.append("Symbols/symbol_14.png")
    imageName.append("Symbols/symbol_15.png")
    imageName.append("Symbols/symbol_16.png")
    imageName.append("Symbols/symbol_17.png")
    imageName.append("Symbols/symbol_18.png")
    imageName.append("Symbols/symbol_19.png")
    imageName.append("Symbols/symbol_20.png")
    imageName.append("Symbols/symbol_21.png")
    
    def __init__(self):
        '''
        Constructor
        Set up the images for each card and make it of a certain tower type        
        '''
