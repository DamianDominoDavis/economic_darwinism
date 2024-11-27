import random

class Player:
	def __init__(self, player_id):
		self.id = player_id
		self.money = 1500
		self.properties = []
		self.position = 0
		self.in_jail = False
		self.jail_turns = 0

	def roll_dice(self):
		return random.randint(1, 6), random.randint(1, 6)

	def move(self, steps):
		self.position = (self.position + steps) % 40

	def buy(self, property):
		if self.pay(property.cost):
			property.owner = self
			self.properties.append(property)
			return True
		return False

	def pay(self, amount, recipient=None):
		self.money -= amount
		if recipient:
			recipient.money += amount
		if self.money < 0:
			self.declare_bankruptcy()
			return False
		return True

	def earn(self, amount):
		self.money += amount

	def declare_bankruptcy(self):
		for property in self.properties:
			property.owner = None
		self.properties = []
		self.money = 0
