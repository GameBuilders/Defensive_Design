"""
userinterface.py - Handles the game's user interface (UI) and draws it to the
screen.
"""

import os
import pygame
from pygame.colordict import THECOLORS

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
FONT_COLOR = (0, 0, 0, 255)
#FONT_COLOR = THECOLORS["gray"]

"""
The color used for the background behind the font.
"""
FONT_BACKGROUND = (255, 255, 255, 0)
#FONT_BACKGROUND = THECOLORS["white"]

"""
The number of pixels between two lines of text on the screen.
"""
FONT_LINESPACE = 4

import pygame
from tower import *
import maptile

class UserInterface:
    def __init__(self, gamemap, imageLoader):
        # Define a font object to use
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("UI", "larabie.ttf"), FONT_SIZE)
        self.bigfont = pygame.font.Font(os.path.join("UI", "larabie.ttf"), 42)
        self.bigfont.set_bold(True)
        self.gamestate = True # The game is running
        self.selection_bar = SelectionBar(gamemap, imageLoader)
        self.gamemap = gamemap
        self.selected_tower = TOW_NONE
        self.selection_pos = (1000, 1000)
        self.selection_img = imageLoader.load('images/towers/selected.png')
        self.show_win = False

    def update(self, gamedata):
        # We save a surface containing the text we want to show.
        self.score = self.font.render("Score: " + str(gamedata.score),
                                      True, FONT_COLOR)
        self.score = self.score.convert_alpha()
        self.lives = self.font.render("Lives: " + str(gamedata.lives),
                                      True, FONT_COLOR)
        self.resources = self.font.render("Resources: " + str(gamedata.resources),
                                          True, FONT_COLOR)
        self.defeat = self.font.render("You have been defeated!", True,
                                       FONT_COLOR)
        self.win = self.bigfont.render("SUCCESS!", True, FONT_COLOR)

    def onClick(my, pos, gamedata, towers, sfx):
        indices = my.gamemap.pixelToTileCoords(pos)
        true_pos = my.gamemap.tileToPixelCoords(indices)
        if my.selection_bar.towerarrow.rect.collidepoint(pos):
            my.selected_tower = TOW_ARROW
            my.selection_pos = true_pos
        elif my.selection_bar.towerrock.rect.collidepoint(pos):
            my.selected_tower = TOW_ROCK
            my.selection_pos = true_pos
        elif my.selection_bar.towerbomb.rect.collidepoint(pos):
            my.selected_tower = TOW_BOMB
            my.selection_pos = true_pos
        elif indices[1] < my.gamemap.numColumns - 1:
            # Check if we can place a tower
            tileType = my.gamemap.getTileByPixels(*pos)
            if tileType == maptile.PLOT and my.selected_tower != TOW_NONE:
#                selected_pos = my.selection_pos
#                selected_tower = my.selection_tower
                # Try to place a tower.
                # A type of tower is selected. We know what to place.
                do_sound = False
                if my.selected_tower == TOW_ARROW and \
                        gamedata.resources >= ArrowTower.cost:
                    my.gamemap.setTile(indices[0], indices[1], maptile.PLOT_TOW_ARROW)
                    gamedata.resources -= ArrowTower.cost
                    tower = ArrowTower(pygame.Rect(true_pos,
                        (my.gamemap.tilewidth, my.gamemap.tileheight)))
                    towers.append(tower)
                    do_sound = True
                elif my.selected_tower == TOW_ROCK and \
                        gamedata.resources >= RockTower.cost:
                    my.gamemap.setTile(indices[0], indices[1], maptile.PLOT_TOW_ROCK)
                    gamedata.resources -= RockTower.cost
                    tower = RockTower(pygame.Rect(true_pos,
                        (my.gamemap.tilewidth, my.gamemap.tileheight)))
                    towers.append(tower)
                    do_sound = True
                elif my.selected_tower == TOW_BOMB and \
                        gamedata.resources >= BombTower.cost:
                    my.gamemap.setTile(indices[0], indices[1], maptile.PLOT_TOW_BOMB)
                    gamedata.resources -= BombTower.cost
                    tower = BombTower(pygame.Rect(true_pos,
                        (my.gamemap.tilewidth, my.gamemap.tileheight)))
                    towers.append(tower)
                    do_sound = True
                if do_sound:
                    sfx.play('tower_made')

    def draw(self, surface):
        # Draw the score in the upper left corner
        surface.blit(self.score, (FONT_PADDING, FONT_PADDING))
        # Put the number of lives below the score
        surface.blit(self.lives, (FONT_PADDING, FONT_SIZE+FONT_PADDING+FONT_LINESPACE))
        # Put the resources in the top right corner
        surface.blit(self.resources, (surface.get_width()-FONT_PADDING-self.resources.get_width(),
                                      FONT_PADDING))
        self.selection_bar.draw(surface)
        surface.blit(self.selection_img, self.selection_pos)

        # If the game has ended, show a defeat message
        if(not self.gamestate):
            surface.blit(self.defeat, ((surface.get_width()-self.defeat.get_width())/2,
                                       (surface.get_height()-self.defeat.get_height())/2))
        if self.show_win:
            surface.blit(self.win, ((surface.get_width()-self.win.get_width())/2,
                                       (surface.get_height()-self.win.get_height())/2))

    def showDefeat(self):
        self.gamestate = False # The game is 
    
    def showWin(self, show):
        self.show_win = show

class SelectionBar(object):
    def __init__(my, gamemap, imageLoader):
        rect = pygame.Rect(
            gamemap.tileToPixelCoords(
                (gamemap.numRows - 1, gamemap.numColumns - 1)),
            (gamemap.tilewidth, gamemap.tileheight))
        my.towerarrow = ArrowTower(rect)
        rect = rect.copy()
        rect.topleft = gamemap.tileToPixelCoords(
                (gamemap.numRows - 2, gamemap.numColumns - 1))
        my.towerrock = RockTower(rect)
        rect = rect.copy()
        rect.topleft = gamemap.tileToPixelCoords(
                (gamemap.numRows - 3, gamemap.numColumns - 1))
        my.towerbomb = BombTower(rect)
        #towerfire = FireTower()
    
    def draw(my, surface):
        my.towerarrow.draw(surface)
        my.towerrock.draw(surface)
        my.towerbomb.draw(surface)

# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
        
