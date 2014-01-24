
import random
import time
from card import card

class BuildDeck(object):
	"""docstring for BuildDeck"""
	def __init__(self, deck):
		super(BuildDeck, self).__init__()
		self.cards = []
		self.cards.append(card(random.randint(0, 19)))
		self.cards.append(card(random.randint(0, 19)))
		self.cards.append(card(random.randint(0, 19)))
		self.cards[0].position = (0, 133)
		self.cards[1].position = (300, 133)
		self.cards[2].position = (600, 133)
		self.cards[0].onScreen = True
		self.cards[1].onScreen = True
		self.cards[2].onScreen = True
		self.deck = deck
		random.seed(time.time)

	def draw(self, surface):
		self.cards[0].draw(surface)
		self.cards[1].draw(surface)
		self.cards[2].draw(surface) 
		
	#happens every time you select a card
	def getNewCards(self):
		self.cards[0] = card(random.randint(0, 19))
		self.cards[1] = card(random.randint(0, 19))
		self.cards[2] = card(random.randint(0, 19))
		self.cards[0].position = (0, 133)
		self.cards[1].position = (300, 133)
		self.cards[2].position = (600, 133)
		self.cards[0].onScreen = True
		self.cards[1].onScreen = True
		self.cards[2].onScreen = True

	def click(self, pos):
		if(self.cards[0].click_on(pos[0], pos[1])):
			# todo
			self.deck.add_card(self.cards[0])
			self.getNewCards()
		elif(self.cards[1].click_on(pos[0], pos[1])):
			# todo
			self.deck.add_card(self.cards[1])
			self.getNewCards()
		elif(self.cards[2].click_on(pos[0], pos[1])):
			# todo
			self.deck.add_card(self.cards[2])
			self.getNewCards()

