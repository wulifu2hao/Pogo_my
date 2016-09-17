from rater import generate_pokemon_list_summary
from common import pokemon_base_stats
from pokedex import pokedex

excluded_pokemon_name_list = []



def find_bad_pokemons(pokemon_list):
	pokemon_summary = generate_pokemon_list_summary(pokemon_list)
	bad_pokemons_ids = []
	
	for pokemon_name in sorted(pokemon_summary.keys()):
		if pokemon_name in excluded_pokemon_name_list:
			continue
		if len(pokemon_summary[pokemon_name]) == 0:
			continue
		if pokedex.evolves[pokemon_summary[pokemon_name][0]['pokemon_info']['pokemon_id']] == 0:
			# print "skipping", pokemon_name
			continue
		best_cp_pokemons = sorted(pokemon_summary[pokemon_name], key=lambda pokemon:pokemon['pokemon_info']['cp'], reverse=True)[:1]
		best_score_pokemons = sorted(pokemon_summary[pokemon_name], key=lambda pokemon:pokemon['score'], reverse=True)[:2]
		pokemons_to_keep = best_cp_pokemons + best_score_pokemons
		pokemon_ids_to_keep = [pokemon['pokemon_info']['id'] for pokemon in pokemons_to_keep]

		good_pokemons, bad_pokemons = [], []
		for pokemon in pokemon_summary[pokemon_name]:
			if pokemon['pokemon_info']['id'] not in pokemon_ids_to_keep and pokemon['score'] < 90:
				bad_pokemons.append((pokemon['pokemon_info'], pokemon['score'], pokemon['power']))
				bad_pokemons_ids.append(pokemon['pokemon_info']['id'])
			else:
				good_pokemons.append((pokemon['pokemon_info'], pokemon['score'], pokemon['power']))
		
		# if len(good_pokemons) > 0:
		# 	print "good", pokemon_name
		# 	for (pokemon, score, cur_cp_wo_multi) in good_pokemons:
		# 		print "cp:", pokemon['cp'], "score:", score, "power:", cur_cp_wo_multi
		# if len(bad_pokemons) > 0:
		# 	print "bad", pokemon_name
		# 	for (pokemon, score, cur_cp_wo_multi) in bad_pokemons:
		# 		print "cp:", pokemon['cp'], "score:", score, "power:", cur_cp_wo_multi, "id:", pokemon['id']

	return bad_pokemons_ids