from utils import *

class Team:
	def __init__(self):
		self.team = []
		self.current_pokemon = None

	def add_pokemon_name(self, pokemon_name, item=None, ability=None):
		if len(self.team) == 6:
			print("ERROR: Max number of Pokemon reached.")
			return
		if self.check_pokemon(pokemon_name):
			return False
		self.team.append(Pokemon(pokemon_name.lower(), item, ability))

	def add_pokemon(self, pokemon):
		if len(self.team) == 6:
			print("ERROR: Max number of Pokemon reached.")
			return
		if any(p == pokemon for p in self.team):
			return False
		self.team.append(pokemon)

	def check_pokemon(self, pokemon_name):
		return any(pokemon_name.replace(' ', '-').lower() in p.name.lower() for p in self.team)

	def get_pokemon(self, pokemon_name):
		for p in range(len(self.team)):
			if self.team[p].get_name().lower() is pokemon_name.lower():
				return p

	def get_team(self):
		return self.team

	def set_current(self, pokemon_name):
		for p in self.team:
			if p.get_name().lower() == pokemon_name.lower():
				self.current_pokemon = p
				break

	def get_current(self):
		return self.current_pokemon

	def remove_pokemon(self, pokemon_name):
		for p in range(len(self.team)):
			if self.team[p].get_name().lower() is pokemon_name.lower():
				del(self.team[p])
				break

	def set_pokemon_item(self, pokemon_name, item):
		for p in self.team:
			if p.get_name().lower() is pokemon_name.lower():
				p.set_item(item)
				break

	def set_pokemon_ability(self, pokemon_name, ability):
		for p in self.team:
			if p.get_name().lower() is pokemon_name.lower():
				p.set_ability(ability)
				break

class Pokemon:
	def __init__(self, name=None, item=None, ability=None):
		self.name = name
		self.item = item
		self.type, self.base_stat = get_pokemon_info(name)
		self.ability = ability
		self.moves = []
		self.hp = 100.0 #by %?
		self.status = None #Para, poisoned, asleep, etc

	def set_name(self, name):
		self.name = name
		self.type, self.base_stat = get_pokemon_info(name)

	def get_name(self):
		return self.name

	def set_item(self, item):
		self.item = item

	def get_item(self):
		return self.item

	def set_ability(self, ability):
		self.ability = ability

	def get_ability(self):
		return self.ability

	def add_move(self, move_name):
		self.moves.append(Move(move_name))

	def get_moves(self):
		return self.moves

	def set_type(self, type_name1, type_name2=None):
		self.type = [type_name1]
		if type_name2:
			self.type.append(type_name2)

	def get_type(self):
		return self.type

	def get_base_stat(self):
		return self.base_stat

	def set_hp(self, hp):
		self.hp = hp

	def get_hp(self):
		return self.hp

	def change_hp(self, amount):
		self.hp += amount

	def set_status(self, status):
		self.status = status

	def get_status(self, status):
		return self.status

class Move:
	def __init__(self, name=None):
		self.name = name
		stat_dict = get_move_info(name)
		self.power = None
		self.accuracy = None
		self.pp = None
		self.max_pp = None
		self.priority = None
		self.damage_type = None
		self.stat_changes = None
		self.type = None
		self.meta = None
		if stat_dict:
			self.power = stat_dict["power"]
			self.accuracy = stat_dict["accuracy"]
			self.pp = stat_dict["pp"]
			self.max_pp = stat_dict["max_pp"]
			self.priority = stat_dict["priority"]
			self.damage_type = stat_dict["dmg_type"]
			self.stat_changes = stat_dict["stat_changes"]
			self.type = stat_dict["type"]
			self.meta = stat_dict["meta"]

	def set_name(self, name):
		self.name = name
		stat_dict = get_move_info(name)
		self.power = stat_dict["power"]
		self.accuracy = stat_dict["accuracy"]
		self.pp = stat_dict["pp"]
		self.max_pp = stat_dict["max_pp"]
		self.priority = stat_dict["priority"]
		self.damage_type = stat_dict["dmg_type"]
		self.stat_changes = stat_dict["stat_changes"]
		self.type = stat_dict["type"]
		self.meta = stat_dict["meta"]

	def get_power(self):
		return self.power

	def get_accuracy(self):
		return self.accuracy

	def set_pp(self, pp):
		self.pp = pp

	def get_pp(self):
		return self.pp

	def change_pp(self, pp_amount):
		self.pp += pp_amount

	def get_max_pp(self):
		return self.max_pp

	def get_priority(self):
		return self.priority

	def get_damage_type(self):
		return self.damage_type

	def get_stat_changes(self):
		return self.stat_changes

	def get_type(self):
		return self.type

	def get_meta(self):
		return self.meta
