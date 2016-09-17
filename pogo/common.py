import json

def _get_pokemon_base_stats():
	f = open('poke_baseinfo.json','r')
	obj = json.load(f)
	f.close()
	return obj

def _get_moves_stats():
	f = open('moves.json','r')
	obj = json.load(f)
	f.close()
	return obj	

def _get_pokemon_moves():
	f = open('pokemon_moves.json','r')
	obj = json.load(f)
	f.close()
	return obj	

pokemon_possible_attrs = ['id', 'pokemon_id', 'cp','stamina','stamina_max','move_1','move_2','height_m','weight_kg','individual_attack','individual_defense','individual_stamina','cp_multiplier','pokeball','captured_cell_id','creation_time_ms','from_fort']        
pokemon_base_stats = _get_pokemon_base_stats()
pokemon_moves = _get_pokemon_moves()
move_stats = _get_moves_stats()
max_cp_multiplier = 0.7903


