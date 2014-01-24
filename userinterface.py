"""
userinterface.py - Handles the game's user interface (UI) and draws it to the
screen.
"""


import os

"""
The size of the font to use in the user interface
"""
FONT_SIZE = 25

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
FONT_BACKGROUND = (255, 255, 255)

"""
The number of pixels between two lines of text on the screen.
"""
FONT_LINESPACE = 4

import pygame
import hand

class UserInterface:

    def __init__(self):
        # Define a font object to use
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("UI", "larabie.ttf"), FONT_SIZE, )
        self.gamestate = False # The game is running

    def start(self, deck, surface):
        self.gamestate = True
        self.hand = hand.Hand(deck, surface)
        self.card_selected = False

    def update(self, gamedata):
        # We save a surface containing the text we want to show.
        self.score = self.font.render("Score: " + str(gamedata.score),
                                      True, FONT_COLOR, FONT_BACKGROUND)
        self.lives = self.font.render("Lives: " + str(gamedata.lives),
                                      True, FONT_COLOR, FONT_BACKGROUND)
        self.resources = self.font.render("Resources: " + str(gamedata.resources),
                                          True, FONT_COLOR, FONT_BACKGROUND)
        self.defeat = self.font.render("You have been defeated!", True,
                                       FONT_COLOR, FONT_BACKGROUND)

        if(self.card_selected):
            self.current_mouse_pos = pygame.mouse.get_pos()
            new_position = (self.hand.cards[self.clicked_on].position[0] + self.current_mouse_pos[0] - self.prev_mouse_pos[0], self.hand.cards[self.clicked_on].position[1] + self.current_mouse_pos[1] - self.prev_mouse_pos[1])
            self.hand.cards[self.clicked_on].position = new_position
            self.prev_mouse_pos = self.current_mouse_pos
    
    def click(self, x, y):
        self.clicked_on = self.hand.check(x, y)
        if(self.clicked_on == -1):
            return
        self.card_selected = True
        self.prev_mouse_pos = (x, y)

    def click_up(self, surface, map):
        if(self.card_selected):
            self.card_selected = False
            self.hand.cards[self.clicked_on].position = self.hand.index_to_pos(self.clicked_on, surface)
            if(map.checkIfCanPlace(self.prev_mouse_pos[0], self.prev_mouse_pos[1])):
                t = map.placeTowerAt(self.prev_mouse_pos[0], self.prev_mouse_pos[1], self.hand.cards[self.clicked_on].ctype)
                pygame.display.update()
                print(self.clicked_on)
                self.hand.remove_card(self.clicked_on, surface)
                if(not len(self.hand.deck.deck) < 1):
                    self.hand.add_card(self.hand.deck.draw_card(), surface)
		return t
	return -1

	

    def draw(self, surface):
        width = surface.get_width()
        height = surface.get_height()
        # Draws the hand below the bottom of the map
        
        # for card in self.hand.cards :
        #     surface.blit(self.basecard, card.position.x, card.position.y)

        self.hand.draw(surface)

        # Draw the score in the upper left corner
        surface.blit(self.score, (FONT_PADDING, FONT_PADDING))
        # Put the number of lives below the score
        surface.blit(self.lives, (FONT_PADDING, FONT_SIZE+FONT_PADDING+FONT_LINESPACE))
        # Put the resources in the top right corner
        surface.blit(self.resources, (surface.get_width()-FONT_PADDING-self.resources.get_width(),
                                      FONT_PADDING))

        # If the game has ended, show a defeat message
        if(not self.gamestate):
            surface.blit(self.defeat, ((surface.get_width()-self.defeat.get_width())/2,
                                       (surface.get_height()-self.defeat.get_height())/2))

		

    def showDefeat(self):
        self.gamestate = False # The game is 
        
# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
        
