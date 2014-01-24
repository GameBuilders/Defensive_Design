import pygame
import os

class ImageLoader(object):
	def __init__(my, size):
		my.size = size
		
	def load(my, filename):
		img = pygame.image.load(os.path.join(filename))
		img = pygame.transform.scale(img, my.size)
		img = img.convert_alpha()
		return img
