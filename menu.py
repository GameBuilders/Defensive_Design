
import pygame
import os
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



class Menu(object):
	"""docstring for Menu"""
	def __init__(self):
		super(Menu, self).__init__()
		self.font = pygame.font.Font(os.path.join("UI", "larabie.ttf"), FONT_SIZE, )

	def draw(self, surface):
		self.start_text = self.font.render("Start", True, FONT_COLOR, FONT_BACKGROUND)
		surface.blit(self.start_text, ((surface.get_width()-self.start_text.get_width())/2,
                                       (surface.get_height()-self.start_text.get_height())/2))