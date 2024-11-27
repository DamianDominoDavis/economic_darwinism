import os
import random
from datetime import datetime

import Player
import Board

class GameManager:
	def __init__(self, log_dir="logs"):
		self.board = Board()
		self.players = []
		self.current_player_index = 0
		self.bankruptcy_order = []
		self.turn_number = 0
		self.last_roll = [None,None]
		self.doubles = 0
		self.log_dir = log_dir
		self.log_file = None
		os.makedirs(self.log_dir, exist_ok=True)

	def add_player(self, player_id):
		player = Player(player_id)
		self.players.append(player)
		self.log(f"Added player {player}")

	def log(self, message):
		if self.log_file is None:
			timestamp = datetime.now().strftime("%Y%m%d%H%M")
			self.log_file = os.path.join(self.log_dir, f"game-{timestamp}.log")
			with open(self.log_file, "w") as file:
				file.write("Game Log Started\n")
		timestamp = datetime.now().strftime("[%H:%M:%S]")
		with open(self.log_file, "a") as file:
			file.write(f"{timestamp} {message}\n")

	def play_turn(self):
		self.turn_number += 1
		player = self.players[self.current_player_index]
		if self.doubles != 0:
			while player.money < 1:
				self.current_player_index = (self.current_player_index + 1) % len(self.players)
				player = self.players[self.current_player_index]
		last_roll = roll_dice()
		if last_roll[0] == last_roll[1]:
			self.doubles += 1
			if self.doubles >= 3:
				self.jail(player)
				self.doubles = 0
		else:
			player.move(sum(last_roll))
			self.log(f"{player} rolls {sum(last_roll)}, moves to {self.board.spaces[player.position]}")
			self.board.resolve_space(player, )

	def roll_dice(self):
		return random.randint(1, 6) + random.randint(1, 6)

	def resolve_space(self, player, space):
		space = self.board.get_space(player.position)
		if isinstance(space, Property):
			if space.owner is None:
				self.handle_unowned_property(player, space)
			elif space.owner != player.id:
				self.handle_rent_payment(player, space)

	def handle_unowned_property(self, player, space):
		if space.name == "chance" or space.name == "community chest":
			pass
		elif player.balance >= property.price:
			# decline trade? implement later
			player.buy(space)
			self.log(f"{player.name} bought {property.name} for ${property.price}.")

	def handle_rent_payment(self, player, property):
		rent = property.calculate_rent()
		if player.balance >= rent:
			player.balance -= rent
			owner = self.board.players[property.owner]
			owner.balance += rent
			self.log(f"{player.name} paid ${rent} in rent to {owner.name}.")
		else:
			self.log(f"{player.name} cannot afford the rent of ${rent} and goes bankrupt.")
			self.handle_bankruptcy(player)

	def handle_bankruptcy(self, player):
		"""Handle the logic for a bankrupt player."""
		player.is_bankrupt = True
		player.balance = 0
		for prop in self.board.list_owned_properties(player.id):
			prop.owner = None  # Free up properties for others to purchase
		self.log(f"{player.name} is bankrupt. All their properties are returned to the bank.")

		# Move player to the end of the player list to track bankruptcy order
		bankrupt_player = self.players.pop(self.current_player_index)
		self.bankruptcy_order.append(bankrupt_player.name)
		self.players.append(bankrupt_player)

		# Do not increment turn number for bankrupt players
		self.current_player_index -= 1  # Adjust index to account for the removed player

	def jail(self, player):
		pass

	def run_game(self):
		"""Run the main game loop until a winner is determined."""
		random.shuffle(self.players)
		self.turn_number = 1
		while len([p for p in self.players if not p.is_bankrupt]) > 1:
			self.play_turn()
		winner = next(p for p in self.players if not p.is_bankrupt)
		self.log(f"The game is over. {winner.name} wins!")
		self.log(f"Bankruptcy order: {', '.join(self.bankruptcy_order)}")
