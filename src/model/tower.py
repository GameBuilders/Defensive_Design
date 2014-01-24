import towerType, pygame

class tower:
	
	tType = None
	xCoord, yCoord = 0, 0
	projectile = None
	
	def __init__(self, t):
		self.tType = towerType(t)
		
	
	def pos(self, x, y):
		self.xCoord = x
		self.yCoord = y
	
	