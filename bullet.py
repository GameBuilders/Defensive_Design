import pygame
import math

class BulletImages(object):
	def __init__(my, imageLoader):
		my.arrow = imageLoader.load('images/bullets/arrow.png')
		my.rock = imageLoader.load('images/bullets/rock.png')

bullet_images = None

class Bullet(pygame.sprite.Sprite):
	SPEED = 1.0
	DAMAGE = 1
	def __init__(my, target, aim, rect=None, image=None):
		super(Bullet, my).__init__()
		my.contact_time = 9999.0
		my.rect = rect
		my.image = image
		my.dead = False
		my.aim_at(aim.x, aim.y)
		my.target = target
		# When the bullet will hit.
	
	def aim_at(my, x, y, speed=None):
		if speed is None:
			speed = my.SPEED
		x1 = my.rect.x
		y1 = my.rect.y
		my.dx = x - x1
		my.dy = y - y1
		# Normalize the direction
		length = math.sqrt(my.dx * my.dx + my.dy * my.dy)
		my.dx /= length
		my.dy /= length
		if my.image is not None:
			my.image = pygame.transform.rotozoom(my.image,
				-math.atan2(my.dy, my.dx) * 180.0 / math.pi, 1.0)
		# Add the speed
		my.dx *= speed
		my.dy *= speed
		my.contact_time = length / speed
		#print my.contact_time
	
	def set_direction(my, dx, dy):
		my.dx = x
		my.dy = y
	
	def update(my, dt=0.0):
		my.rect.x += my.dx
		my.rect.y += my.dy
		my.contact_time -= 1
		if my.contact_time <= 0.0:
			my.dead = True
	
	def draw(my, surface):
		surface.blit(my.image, my.rect)

class ArrowBullet(Bullet):
	SPEED = 8.0
	DAMAGE = 25
	def __init__(my, target, aim, rect=None, image=None):
		super(ArrowBullet, my).__init__(target, aim, rect)
		global bullet_images
		my.image = bullet_images.arrow
		my.aim_at(aim.x, aim.y, my.SPEED)
	
	def aim_at(my, x, y, speed=None):
		super(ArrowBullet, my).aim_at(x, y, my.SPEED)

class RockBullet(Bullet):
	SPEED = 3.5
	DAMAGE = 65
	def __init__(my, target, aim, rect=None, image=None):
		super(RockBullet, my).__init__(target, aim, rect)
		global bullet_images
		my.image = bullet_images.rock
		my.aim_at(aim.x, aim.y, my.SPEED)
	
	def aim_at(my, x, y, speed=None):
		super(RockBullet, my).aim_at(x, y, my.SPEED)

def load_bullets(imageLoader):
	global bullet_images
	if bullet_images is None:
		bullet_images = BulletImages(imageLoader)
