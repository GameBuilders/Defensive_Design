import pygame
import bullet

(TOW_NONE,
TOW_ARROW,
TOW_BOMB,
TOW_ROCK,
TOW_NUM_TOWERS) = range(5)

class TowerImages(object):
	def __init__(my, imageLoader):
		my.images = []
		my.images.append(None)
		my.images.append(imageLoader.load('images/towers/arrow.png'))
		my.images.append(imageLoader.load('images/towers/bomb.png'))
		my.images.append(imageLoader.load('images/towers/rock.png'))

tower_images = None

class Tower(pygame.sprite.Sprite):
	cooldown = 120
	cost = 10
	
	def __init__(my, rect=None, image=None):
		super(Tower, my).__init__()
		my.rect = rect
		my.image = image
		my.hp = 10
		my.time_til_action = my.cooldown
		my.form = TOW_NONE
		my.sight_range = 9999.0
	
	def canShoot(my):
		return my.time_til_action <= 0
	
	def shoot(my, enemy, bullets):
		my.time_til_action = my.cooldown
		return None
	
	def update(my, dt=0.0):
		# Restore the cooldown time by 1 for each update cycle.
		if my.time_til_action > 0:
			my.time_til_action -= 1
	
	def draw(my, surface):
		surface.blit(my.image, my.rect)

class ArrowTower(Tower):
	cooldown = 20
	cost = 20
	
	def __init__(my, rect=None, image=None):
		super(ArrowTower, my).__init__(rect)
		my.hp = 20
		my.form = TOW_ARROW
		my.time_til_action = my.cooldown
		my.sight_range = 400.0
		global tower_images
		my.image = tower_images.images[my.form]
	
	def shoot(my, enemy, dest, bullets):
		my.time_til_action = my.cooldown
		bullets.append(bullet.ArrowBullet(enemy, dest, my.rect.copy()))

class RockTower(Tower):
	cooldown = 50
	cost = 30
	
	def __init__(my, rect=None, image=None):
		super(RockTower, my).__init__(rect)
		my.hp = 30
		my.form = TOW_ROCK
		my.time_til_action = my.cooldown
		my.sight_range = 150.0
		global tower_images
		my.image = tower_images.images[my.form]
	
	def shoot(my, enemy, dest, bullets):
		my.time_til_action = my.cooldown
		bullets.append(bullet.RockBullet(enemy, dest, my.rect.copy()))

class BombTower(Tower):
	cooldown = 300
	cost = 100
	
	def __init__(my, rect=None, image=None):
		super(BombTower, my).__init__(rect)
		my.hp = 20
		my.form = TOW_BOMB
		my.time_til_action = my.cooldown
		my.sight_range = 800.0
		global tower_images
		my.image = tower_images.images[my.form]
	
	def shoot(my, enemy, bullets):
		my.time_til_action = my.cooldown

def load_towers(imageLoader):
	global tower_images
	if tower_images is None:
		tower_images = TowerImages(imageLoader)
