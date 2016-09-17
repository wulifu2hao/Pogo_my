import json

from rater import rate_pokemon, generate_pokemon_list_summary
from common import pokemon_base_stats
from screener import find_bad_pokemons

f = open('output.txt', 'r')
pokemon_list = json.load(f)
f.close()

# res = {}

# for pokemon in pokemon_list:
# 	score, cur_cp_wo_multi = rate_pokemon(pokemon)
# 	pokemon_name = pokemon_base_stats[pokemon['pokemon_id']]['Name']
# 	if pokemon_name not in res:
# 		res[pokemon_name] = []
# 	res[pokemon_name].append((pokemon, score, cur_cp_wo_multi))

# for pokemon_name in sorted(res.keys()):
# 	specie_result = sorted(res[pokemon_name], key=lambda (pokemon, score, power):score, reverse=True)
# 	for (pokemon, score, cur_cp_wo_multi) in specie_result:
# 		print pokemon_name, "cp:", pokemon['cp'], "score:", score, "power:", cur_cp_wo_multi

# find_bad_pokemons(pokemon_list)

f = open('exmaple.json','w')
res = generate_pokemon_list_summary(pokemon_list)
json.dump(res, f)
f.close()