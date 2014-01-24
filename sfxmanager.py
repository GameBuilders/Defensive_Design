import pygame

class SFXManager(object):
	def __init__(my):
		my.sfx = {
			'core_damaged':pygame.mixer.Sound('core_damaged.ogg'),
			'enemy_made':pygame.mixer.Sound('enemy_made.wav'),
			'foe_damaged':pygame.mixer.Sound('foe_damaged.wav'),
			'foe_exploded':pygame.mixer.Sound('foe_exploded.wav'),
			'tower_made':pygame.mixer.Sound('tower_made.wav'),
			'next_stage':pygame.mixer.Sound('menu_select.wav'),
			'shoot':pygame.mixer.Sound('menu_cancel.wav'),
		}
	
	def play(my, name):
		return
		my.sfx[name].play()
