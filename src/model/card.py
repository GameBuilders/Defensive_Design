'''
Created on Nov 16, 2013

@author: zeno
'''
import cardType

class card:
    '''
    classdocs
    '''

    cType = None
    images = []
    onScreen = False
    position = -1
    
    
    def __init__(self, t):
        '''
        Constructor
        '''
        self.cType = cardType(t)
        self.getImage    
    
    def draw(self):
        if(self.onScreen == True):
            self.tType.draw()
            
    
        