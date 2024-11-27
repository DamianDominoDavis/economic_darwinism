class Property:
	"""load property from JSON"""
	def all(properties_file="themes/standard_theme.json"):
		try:
			with open(properties_file, "r") as file:
				properties_data = json.load(file)
			return [
				Property(
					name=prop["name"],
					color_group=prop["color_group"],
					price=prop["price"],
					base_rent=prop["base_rent"],
					house_rent=prop.get("house_rent", []),
					hotel_rent=prop.get("hotel_rent", 0),
					mortgage_value=prop.get("mortgage_value", 0)
				)
				for prop in properties_data
			]
		except FileNotFoundError:
			raise ValueError(f"Error: {properties_file} not found.")
		except KeyError as e:
			raise ValueError(f"Bad properties file {properties_file} (missing field {e})")

	def __init__(self, name, color_group, price, rents, can_improve, improvement_price):
		self.name = name
		self.color_group = color_group
		self.price = price
		self.rents = rents
		self.improvement_price = improvement_price
		self.owner = None
		self.is_mortgaged = False
		self.can_improve = can_improve
		self.improvement = 0

	def calculate_rent(self):
		if self.is_mortgaged:
			return 0  # No rent if mortgaged
		if self.can_improve:
			if self.improvement > 0:
				return self.rents[self.improvement]
			group = [prop for prop in all() if prop.color_group == self.color_group]
			if all(self.owner == prop.owner for prop in group):
				return self.rents[0] * 2
		return self.rents[0]

	def mortgage_value(self):
		return self.price / 2

	def mortgage(self):
		if not self.is_mortgaged and self.owner is not None:
			self.is_mortgaged = True
			self.owner.earn(self.mortgage_value)
		return self.is_mortgaged

	def unmortgage(self):
		if self.is_mortgaged and self.owner.pay(self.mortgage_value):
			self.is_mortgaged = False
		return not self.is_mortgaged

	def improve(self):
		if not self.can_improve or self.improvement >= 5:
			raise ValueError("Can't improve {self}")
		if self.owner.pay(self.improvement_price):
			self.improvement += 1

	def downgrade(self):
		if self.improvement < 1:
			raise ValueError("Can't downgrade {self}")
		self.num_houses -= 1
		self.owner.earn(self.improvement_price / 2)
