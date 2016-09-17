import math

from common import pokemon_possible_attrs, pokemon_base_stats, max_cp_multiplier, pokemon_moves, move_stats

def _calc_cp(base_att, base_def, base_stm, ind_att, ind_def, ind_stm, cp_multiplier):
	return (base_att + ind_att) * math.sqrt(base_def + ind_def) * math.sqrt(base_stm + ind_stm) * math.pow(cp_multiplier,2) / 10

def _calc_cp_v2(base_att, base_def, base_stm, ind_att, ind_def, ind_stm, cp_multiplier):
	max_cp_v2 = 9199.00263469
	return (base_att + ind_att) * (base_def + ind_def) * (base_stm + ind_stm) * math.pow(cp_multiplier,2) / 10	/ max_cp_v2

def rate_pokemon(pokemon):
	if pokemon is None:
		return 0
	for attr in pokemon_possible_attrs:
		if attr not in pokemon:
			return 0
	pokemon_id = int(pokemon['pokemon_id'])
	if pokemon_id == 0 or pokemon_id >= len(pokemon_base_stats):
		return 0

	pokemon_base_stat = pokemon_base_stats[pokemon_id]
	base_att, base_def, base_stm = pokemon_base_stat['BaseAttack'], pokemon_base_stat['BaseDefense'], pokemon_base_stat['BaseStamina']
	ind_att, ind_def, ind_stm = pokemon['individual_attack'], pokemon['individual_defense'], pokemon['individual_stamina']
	min_cp_wo_multi = _calc_cp(base_att, base_def, base_stm, 0, 0, 0, max_cp_multiplier)
	max_cp_wo_multi = _calc_cp(base_att, base_def, base_stm, 15, 15, 15, max_cp_multiplier)
	cur_cp_wo_multi = _calc_cp(base_att, base_def, base_stm, ind_att, ind_def, ind_stm, max_cp_multiplier)
	score = int(100 * (cur_cp_wo_multi - min_cp_wo_multi) / (max_cp_wo_multi - min_cp_wo_multi))

	return score, cur_cp_wo_multi

def generate_pokemon_list_summary(pokemon_list):
	res = {}
	for pokemon in pokemon_list:
		score, cur_cp_wo_multi = rate_pokemon(pokemon)
		pokemon_name = pokemon_base_stats[pokemon['pokemon_id']]['Name']
		if pokemon_name not in res:
			res[pokemon_name] = []
		res[pokemon_name].append({"pokemon_info":pokemon, "score":score, "power":cur_cp_wo_multi})
		# res[pokemon_name].append((pokemon, score, cur_cp_wo_multi))
	return res

def summary_to_readable(pokemon_summary):
	res = []
	for pokemon_name in sorted(pokemon_summary.keys()):
		specie_result = sorted(pokemon_summary[pokemon_name], key=lambda pokemon:pokemon['power'], reverse=True)
		for pokemon in specie_result:
			res.append("%15s cp: %4s score: %3s power: %s id: %s"%(pokemon_name, pokemon['pokemon_info']['cp'], pokemon['score'], pokemon['power'], pokemon['pokemon_info']['id']))
	return '\n'.join(res)

def generate_specie_report():
	res = []
	for idx, pokemon_base_stat in enumerate(pokemon_base_stats):
		if idx == 0:
			continue
		base_att, base_def, base_stm = pokemon_base_stat['BaseAttack'], pokemon_base_stat['BaseDefense'], pokemon_base_stat['BaseStamina']
		max_cp_wo_multi = _calc_cp_v2(base_att, base_def, base_stm, 15, 15, 15, max_cp_multiplier)
		res.append((pokemon_base_stat['Name'], max_cp_wo_multi))
	for (name, power) in sorted(res, key=lambda (name, power):power, reverse=True):
		print name, power

def generate_specie_capture_report():
	res = []
	for idx, pokemon_base_stat in enumerate(pokemon_base_stats):
		if idx == 0:
			continue
		res.append((pokemon_base_stat['Name'], pokemon_base_stat['BaseCaptureRate'], pokemon_base_stat['BaseFleeRate']))
		# print pokemon_base_stat['BaseCaptureRate']	
	for (name, capture_rate, fleet_rate) in sorted(res, key=lambda (name, capture_rate, fleet_rate):capture_rate, reverse=True):
		print name, "capture rate:", capture_rate, "fleet rate:", fleet_rate

def moves_combination_report():
	res = []
	for pokemon_id in pokemon_moves:
		pokemon_info = pokemon_moves[pokemon_id]
		pokemon_stat = pokemon_base_stats[int(pokemon_id)]
		for i in range(len(pokemon_info['fast_moves'])):
			for j in range(len(pokemon_info['charge_moves'])):
				fast_move_name, charge_move_name = pokemon_info['fast_moves'][i], pokemon_info['charge_moves'][j]				
				fast_move, charge_move = move_stats['fast_moves'][fast_move_name], move_stats['charge_moves'][charge_move_name]
				fast_power, charge_power = fast_move['power'], charge_move['power']
				
				# calc STAB
				if fast_move['move_type'] == pokemon_stat['Type1'].lower() or fast_move['move_type'] == pokemon_stat['Type2'].lower():
					fast_power *= 1.25
				if charge_move['move_type'] == pokemon_stat['Type1'].lower() or charge_move['move_type'] == pokemon_stat['Type2'].lower():
					charge_power *= 1.25

				fast_dps, charge_dps = float(fast_power)/fast_move['seconds'], float(charge_power)/charge_move['seconds']
				final_dps, total_time = fast_dps, 0
				if fast_dps < charge_dps:
					energy_needed = -(charge_move['energy'])
					fast_move_num = float(energy_needed)/fast_move['energy']
					total_power = fast_move_num*fast_power + charge_power
					total_time = fast_move_num*fast_move['seconds'] + charge_move['seconds']
					final_dps = float(total_power/total_time)

				res.append({
					"name":pokemon_stat['Name'], 
					"fast_move_name":fast_move['move_name'],
					"fast_dps": fast_dps,
					"charge_move_name":charge_move['move_name'],
					"charge_dps":charge_dps,
					"final_dps":final_dps,
					"cycle_time":total_time
					})
	
	# res = sorted(res, key=lambda poke_with_moves: poke_with_moves['final_dps'], reverse=True)
	for poke_with_moves in res:
		print poke_with_moves['name'], "final_dps:%f"%poke_with_moves['final_dps'], "cycle_time:%f secs"%poke_with_moves['cycle_time'], "%s(%f)"%(poke_with_moves['fast_move_name'], poke_with_moves['fast_dps']), "%s(%f)"%(poke_with_moves['charge_move_name'], poke_with_moves['charge_dps'])

# moves_combination_report()
#generate_specie_capture_report()
