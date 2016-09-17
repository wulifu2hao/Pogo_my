import json
import string
import urllib

def _get_pokemon_moves():
	f = open('moves.json','r')
	obj = json.load(f)
	f.close()
	return obj	

def extract_moves(moves_raw):
	res = {}
	for idx, move_raw in enumerate(moves_raw):
		start = string.find(move_raw, "target=\"_blank\">") + len("target=\"_blank\">")
		end = string.find(move_raw, "</a>", start)
		move_name = move_raw[start:end].lower()
		if "w/" in move_name or len(move_name) == 0:
			continue

		start = string.rfind(move_raw, "www.pokemongodb.net/2016/05/") + len("www.pokemongodb.net/2016/05/")
		end = string.find(move_raw, "-", start)
		move_type = move_raw[start:end]

		start = string.find(move_raw, "middle;\">") + len("middle;\">")
		start = string.find(move_raw, "middle;\">", start) + len("middle;\">")
		end = string.find(move_raw, "</", start)
		dps = move_raw[start:end]

		start = string.find(move_raw, "middle;\">", start) + len("middle;\">")
		end = string.find(move_raw, "</", start)
		power = move_raw[start:end]

		start = string.find(move_raw, "middle;\">", start) + len("middle;\">")
		end = string.find(move_raw, "</", start)
		seconds = move_raw[start:end]

		start = string.find(move_raw, "middle;\">", start) + len("middle;\">")
		end = string.find(move_raw, "</", start)
		energy = move_raw[start:end]

		dps, power, seconds, energy = float(dps), int(power), float(seconds), int(energy)

		if move_name in res:
			print "duplicate move ", move_name
		res[move_name] = {
			"move_name":move_name, 
			"move_type":move_type,
			"dps":dps, 
			"power":power, 
			"seconds":seconds, 
			"energy":energy
			}
		# print idx, move_name, move_type, dps, power, seconds, energy
	return res

def parse_and_store_moves():
	f = open('fast.htm','r')
	content = f.read()
	f.close()
	fast_moves_raw = content.split('<tr')
	f = open('charge.htm','r')
	content = f.read()
	f.close()
	charge_moves_raw = content.split('<tr')


	fast_moves = extract_moves(fast_moves_raw)
	charge_moves = extract_moves(charge_moves_raw)
	res = {
		'fast_moves':fast_moves,
		'charge_moves':charge_moves
	}

	f = open('moves.json','w')
	json.dump(res, f)
	f.close()

def parse_and_store_pokemon_moves():
	f = open('link_to_pokemon.htm','r')
	content = f.read()
	f.close()
	pokemons_raw = content.split('<tr')

	res = []
	for pokemon_raw in pokemons_raw:
		start = string.find(pokemon_raw, "<a class=\"in-cell-link\" href=") + len("<a class=\"in-cell-link\" href=\"")
		end = string.find(pokemon_raw, "\" target", start)
		link =pokemon_raw[start:end]		
		if len(link) > 0:
			res.append(link)
	
	print len(res)

	pokemon_moves = {}
	moves = _get_pokemon_moves()
	for link in res:	
		content = urllib.urlopen(link).read()
		
		start = string.find(content, "Pokedex Entry #") + len("Pokedex Entry #")
		end = string.find(content,":", start)
		pokemon_id = int(content[start:end])

		fast_moves, charge_moves = [], []
		start = string.find(content, "Charge Moves:") + len("Charge Moves:")
		for i in range(5):
			start = string.find(content, "target=\"_blank\">", start) + len("target=\"_blank\">")
			end = string.find(content, "</a>", start)
			move_name = content[start:end].lower()

			if move_name in moves['fast_moves']:
				fast_moves.append(move_name)
			elif move_name in moves['charge_moves']:
				charge_moves.append(move_name)
			else:
				print move_name

		print pokemon_id, fast_moves, charge_moves
		pokemon_moves[pokemon_id] = {
			"pokemon_id":pokemon_id,
			"fast_moves":fast_moves,
			"charge_moves":charge_moves
		}

	f = open('pokemon_moves.json','w')
	json.dump(pokemon_moves, f)
	f.close()


parse_and_store_pokemon_moves()
		
