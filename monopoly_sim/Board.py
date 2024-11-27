import json
import Property

class Board:
	def __init__(self, properties_file="themes/properties.json"):
		self.spaces = [None] * 40
		self.spaces[0] = self.get_property("go")
		self.spaces[20] = self.get_property("free parking")
		properties = Property.all(properties_file)
		for space in [2,17,33]:
			self.spaces = self.get_property("community chest")
		for space in [7,22,36]:
			self.spaces = self.get_property("chance")
		prop_iter = iter(properties)
		for element in self.spaces:
			if element is None:
				try:
					element = next(prop_iter)
				except StopIteration:
					raise ValueError("Bad properties file {properties_file} (too few)")
		if any(element is not None for element in prop_iter):
			raise ValueError("Bad properties file {properties_file} (too many)")

	def get_property(self, property_name):
		for prop in self.properties:
			if prop.name == property_name:
				return prop
		raise ValueError("Property not found.")

	def get_space(self, position):
		space = self.board.spaces[position]

	def get_state(self):
		pass
