import pokebase as pb

all_types = set(['normal', 'fire', 'fighting', 'water', 'flying', 'grass', 'poison', 'electric', 'ground', 'psychic', 'rock', 'ice', 'bug', 'dragon', 'ghost', 'dark', 'steel', 'fairy'])

"""
	Method to get a pokemon's typing and base stats based on name

	Args:
		pokemon_name (string): the name of the desired pokemon to get info for
	Output:
		type_names: list of type as strings
		stats_dict(string, int): dictionary of base stats key:string value:int
"""
def get_pokemon_info(pokemon_name):
	if not pokemon_name:
		return None, None
	p = pb.pokemon(pokemon_name.lower())
	types = p.types
	type_names = []
	stats_dict = {}
	for t in types:
		type_names.append(str(t.type))
	stats = p.stats
	for s in stats:
		name = s.stat
		base_stat = s.base_stat
		stats_dict[str(name)] = base_stat

	return type_names, stats_dict

"""
	Calculates the strengths and weaknesses of a pokemon type. 
	If only one type given, gives the x2, x1, x0.5 and x0 for defending and attacking
	If two types given, gives the x4, x2, x1, x0.5, x0.25, x0 for defending

	DOES NOT TAKE INTO ACCOUNT ABILITIES

	Args:
		type_list (array[string]): Array of size 1 or 2 of the type or duo type 

	Output:
		relations (String, List[String]): dictionary of attack and defense relations
"""
def get_weaknesses_and_strengths(type_list):
	t = pb.type_(type_list[0].lower())
	damage = t.damage_relations

	half_from = type_to_name(damage.half_damage_from)
	double_from = type_to_name(damage.double_damage_from)
	no_from = type_to_name(damage.no_damage_from)

	half_to = type_to_name(damage.half_damage_to)
	double_to = type_to_name(damage.double_damage_to)
	no_to = type_to_name(damage.no_damage_to)

	if len(type_list) == 2:
		t = pb.type_(type_list[1].lower())
		damage = t.damage_relations

		half_from2 = type_to_name(damage.half_damage_from)
		double_from2 = type_to_name(damage.double_damage_from)
		no_from2 = type_to_name(damage.no_damage_from)

		quad_from = set(double_from).intersection(set(double_from2))
		quarter_from = set(half_from).intersection(set(half_from2))
		no_combined_from = set(no_from + no_from2)
		double_combined_from = set(double_from + double_from2) - quad_from - set(half_from) - set(half_from2) - no_combined_from
		half_combined_from = set(half_from + half_from2) - quarter_from - set(double_from) - set(double_from2) - no_combined_from
		normal_damage = all_types - quad_from - double_combined_from - half_combined_from - quarter_from - no_combined_from

		relations = {
			"defense" : {
				"x4" : list(quad_from),
				"x2" : list(double_combined_from),
				"x1" : list(normal_damage),
				"x0.5" : list(half_combined_from),
				"x0.25" : list(quarter_from),
				"x0" : list(no_combined_from)
			}
		}


	else:	
		normal_damage_from = all_types - set(double_from) - set(half_from) - set(no_from)
		normal_damage_to = all_types - set(double_to) - set(half_to) - set(no_to)
		relations = {
			"defense" : {
				"x2" : double_from,
				"x1" : list(normal_damage_from),
				"x0.5" : half_from,
				"x0" : no_from 
			},
			"attack": {
				"x2" : double_to,
				"x1" : list(normal_damage_to),
				"x0.5" : half_to,
				"x0": no_to
			}
		}

	return relations

"""
	Get info of given move name such as type, effects, effect chance, pp, priority, base power, stat changes

	Args:
		name(String): Name of move to check

	Output:
		dict (String, ANYTHING): Returns dictionary of info
"""
def get_move_info(name):
	if not name:
		return None
	move = pb.move(name.lower())
	stat_dict = {
		"power": move.power,
		"accuracy": move.accuracy,
		"pp": move.pp,
		"max_pp": int(move.pp * 8.0 / 5.0),
		"priority": move.priority,
		"dmg_type": str(move.damage_class.name),
		"stat_changes": move.stat_changes,
		"type": str(move.type.name),
		"meta": move.meta
		#{
		# 	"ailment": move.meta['ailment']['name'],
		# 	"ailment_chance": move.meta['ailment_chance'],
		# 	#min/max hits is none of only hits once
		# 	"min_hits": move.meta['min_hits'],
		# 	"max_hits": move.meta['max_hits'],
		# 	#min/max turns effect lasts is null if one turn
		# 	"min_turns": move.meta['min_turns'],
		# 	"max_turns": move.meta['max_turns'],
		# 	#% of hp drain(positive) or recoil(negative)
		# 	"drain": move.meta['drain'],
		# 	#% of healing gained by % of max hp
		# 	"healing": move.meta['healing'],
		# 	"crit_rate": move.meta['crit_rate'],
		# 	"flinch_chance": move.meta['flinch_chance'],
		# 	"stat_chance": move.meta['stat_chance']
		# }
	}
	return stat_dict

"""
	Get info of Pokemon ability

	Args:
		name(String): Name of ability to check

	Output:
		tbh not too sure yet, think of good way to implement abilities that affect battles
"""
def get_ability_info(name):
	ability = pb.ability(name.lower())

"""
	Converts type array to string array of names of types

	Args:
		type_list (array[type_]): array of types to be converted to strings
	Output:
		names (list[String]): list of input types to strings
"""
def type_to_name(type_list):
	names = []
	for t in type_list:
		names.append(str(t['name']))
	return names

#print(get_move_info("breakneck-blitz"))

# t, s = get_pokemon_info('charmander')
# t.append('water')
# print(t)
# print(s)

# r = get_weaknesses_and_strengths(t)
# print(r)

