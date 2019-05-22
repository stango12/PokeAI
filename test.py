import json
from functools import reduce

# test = '>battle-gen7randombattle-899698725\n|request|{"active":[{"moves":[{"move":"Dragon Pulse","id":"dragonpulse","pp":16,"maxpp":16,"target":"any","disabled":false},{"move":"Dragon Tail","id":"dragontail","pp":16,"maxpp":16,"target":"normal","disabled":false},{"move":"Roar","id":"roar","pp":32,"maxpp":32,"target":"normal","disabled":false},{"move":"Shadow Ball","id":"shadowball","pp":24,"maxpp":24,"target":"normal","disabled":false}]}],"side":{"name":"testBot218","id":"p1","pokemon":[{"ident":"p1: Giratina","details":"Giratina, L78","condition":"362/362","active":true,"stats":{"atk":201,"def":232,"spa":201,"spd":232,"spe":185},"moves":["dragonpulse","dragontail","roar","shadowball"],"baseAbility":"pressure","item":"leftovers","pokeball":"pokeball","ability":"pressure"},{"ident":"p1: Articuno","details":"Articuno, L88","condition":"301/301","active":false,"stats":{"atk":154,"def":226,"spa":217,"spd":270,"spe":200},"moves":["icebeam","roost","toxic","hurricane"],"baseAbility":"pressure","item":"leftovers","pokeball":"pokeball","ability":"pressure"},{"ident":"p1: Banette","details":"Banette, L84, M","condition":"245/245","active":false,"stats":{"atk":241,"def":157,"spa":188,"spd":154,"spe":157},"moves":["taunt","knockoff","willowisp","shadowclaw"],"baseAbility":"cursedbody","item":"banettite","pokeball":"pokeball","ability":"cursedbody"},{"ident":"p1: Blissey","details":"Blissey, L82, F","condition":"552/552","active":false,"stats":{"atk":21,"def":64,"spa":170,"spd":269,"spe":137},"moves":["softboiled","thunderwave","flamethrower","seismictoss"],"baseAbility":"naturalcure","item":"leftovers","pokeball":"pokeball","ability":"naturalcure"},{"ident":"p1: Weezing","details":"Weezing, L86, F","condition":"252/252","active":false,"stats":{"atk":159,"def":256,"spa":195,"spd":170,"spe":152},"moves":["painsplit","willowisp","toxicspikes","sludgebomb"],"baseAbility":"levitate","item":"blacksludge","pokeball":"pokeball","ability":"levitate"},{"ident":"p1: Bewear","details":"Bewear, L84, M","condition":"339/339","active":false,"stats":{"atk":258,"def":183,"spa":141,"spd":149,"spe":149},"moves":["hammerarm","doubleedge","icepunch","swordsdance"],"baseAbility":"fluffy","item":"lifeorb","pokeball":"pokeball","ability":"fluffy"}]},"rqid":2}'

# temp = test.split("|")
# y = json.loads(temp[2])
# print(y['rqid'])

y = ['NORMAL', 'FIRE', 'FIGHTING', 'WATER', 'FLYING', 'GRASS', 'POISON', 'ELECTRIC', 'GROUND', 'PSYCHIC', 'ROCK', 'ICE', 'BUG', 'DRAGON', 'GHOST', 'DARK', 'STEEL', 'FAIRY']
move_conversion = {}

fo = open("move_list.txt")

string = fo.readline()
while string:
	idx = reduce(lambda a,b: a if b==-1 or (a <= b and a>=0) else b, list(map(lambda x: string.find(x),y)))
	#print(string[:idx-1])
	res = string[:idx-1]
	showdown = res.replace(' ','').replace('-', '').lower()
	result = res.replace(' ','-').lower()
	move_conversion[showdown] = result
	string = fo.readline()

with open('move_convert.json', 'w') as out:
	json.dump(move_conversion, out)