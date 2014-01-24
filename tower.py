import pygame
import os
from cardType import cardType
import math

FONT_SIZE = 10
FONT_PADDING = 10
FONT_COLOR = (0,0,0)
FONT_BACKGROUND =(255,255,255)
FONT_LINESPACE = 4

class tower:
	
	xCoord, yCoord = 0, 0
	projectile = None

	def __init__(self, ctype):
		self.ctype = ctype
		self.Damage = cardType.Damage[self.ctype]
		self.Range = cardType.Range[self.ctype] * 25
		self.Cooldown = cardType.Cooldown[self.ctype] * 50000

		self.cd = self.Cooldown

		self.last_update_time = pygame.time.get_ticks()
		self.image = cardType.imageName[ctype]

		
	
	def pos(self, x, y):
		print("setting tower coords")
		print(x,y)
		self.xCoord = x * 51
		self.yCoord = y * 51

	def animate(self, enemies, surface):
		self.cd -= pygame.time.get_ticks()-self.last_update_time
		if(self.cd < 0):
			self.cd += self.Cooldown
			for enemy in enemies:
				if(self.in_range(enemy)):
					enemy.health -= self.Damage
					pygame.draw.line(surface, FONT_COLOR, (self.xCoord + 25, self.yCoord + 25), (enemy.getCoordinates()[0] + 25, enemy.getCoordinates()[1] + 25) , 10)
					return
	def draw(self, surface):
		image = pygame.image.load(cardType.imageName[self.ctype]).convert()
		image = pygame.transform.scale(image, (51, 51))
		surface.blit(image, (self.xCoord, self.yCoord))

	def in_range(self, enemy):
		dist = math.sqrt((self.xCoord - enemy.getCoordinates()[0]) * (self.xCoord - enemy.getCoordinates()[0]) + (self.yCoord - enemy.getCoordinates()[1]) * (self.yCoord - enemy.getCoordinates()[1]))
		if(dist < self.Range):
			return True
		return False
