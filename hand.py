
STARTING_CARDS = 4


class Hand(object):
	"""docstring for Hand"""
	def __init__(self, deck, surface):
		super(Hand, self).__init__()
		self.deck = deck

		self.cards = []

		for i in range(STARTING_CARDS):
			self.add_card(self.deck.draw_card(), surface)

	def add_card(self, card, surface):
		self.cards.append(card)
		card.position = self.index_to_pos(len(self.cards) - 1, surface)

# returns card at index 
	def select_card(self, index):
		return self.cards[index]

	def remove_card(self, index, surface):
		self.cards.remove(self.cards[index])
		for i in range(len(self.cards)):
			card = self.cards[i]
			card.position = self.index_to_pos(i, surface)

	def draw(self, surface):
		for i in range(len(self.cards)):
			card = self.cards[i]
			card.draw(surface)

	def index_to_pos(self, index, surface):
		y = surface.get_height() - 133
		x = index * 100
		return (x,y)

	def check(self, x, y):
		for i in range(len(self.cards)):
			card = self.cards[i]
			if(card.click_on(x, y)):
				return i
		return -1
