

import json
import time
import unidecode

counter_cols = ['1st Counter', '2nd Counter', '3rd Counter', '4th Counter', '5th Counter', '6th Counter']
against_cols = ['1st Strong Against', '2nd Strong Against', '3rd Strong Against', '4th Strong Against', '5th Strong Against', '6th Strong Against']
partner_cols = ['1st Good Partner', '2nd Good Partner', '3rd Good Partner', '4th Good Partner', '5th Good Partner', '6th Good Partner']
tips_cols = ['Counter Tip One','Counter Tip Two','Counter Tip Three','Counter Tip Four']

def valid_champ(name):
	champs = get_all_champions()
	name
	if name in champs or name.capitalize() in champs:
		return True
	else:
		return False

def get_all_champions():
    # JSON is hosted at myjson.com as well just in case
    # url = 'https://api.myjson.com/bins/tkg0v'
    with open('champs.json') as json_data:
        data = json.load(json_data)
      	allChampions = []
      	for champ in allChampions:
      		allChampions.append(champ['Champion Names'])
        return allChampions

def parse_name(url):
	return url.split('/')[-1]

def get_loc_names(counter_cols):
	loc_names = []
	for col in counter_cols:
		loc_names.append(col + " Location")
	return loc_names

def get_counter(name):
    with open('champs.json') as json_data:
        data = json.load(json_data)
        counters = []
        locs = []
        for champs in data:
        	if champs['Champion Names'] == name:
        		for col in counter_cols:
        			counters.append(parse_name(champs[col]))
        		for col in get_loc_names(counter_cols):
        			locs.append(champs[col])
        return counters, locs

def get_strong_against(name):
    with open('champs.json') as json_data:
        data = json.load(json_data)
        against = []
        locs = []
        for champs in data:
        	if champs['Champion Names'] == name:
        		for col in against_cols:
        			against.append(parse_name(champs[col]))
        		for col in get_loc_names(against_cols):
        			locs.append(champs[col])
        return against, locs

def get_partner(name):
	with open('champs.json') as json_data:
		data = json.load(json_data)
		parters = []
		for champs in data:
			if champs['Champion Names'] == name:
				for col in partner_cols:
					parters.append(parse_name(champs[col]))
		return parters	

def get_tips(name):
	with open('champs.json') as json_data:
		data = json.load(json_data)
		tips = []
		for champs in data:
			if champs['Champion Names'] == name:
				for col in tips_cols:
					tips.append(parse_name(champs[col]))	
		return tips

def format_counter_msg(name):
	counters, locs = get_counter(name)
	msg = ""
	for i in range(len(counters)):
		msg += "{} counters {} at {}. \n".format(counters[i], name, locs[i])
	return msg

def format_against_msg(name, against, locs):
	msg = ""
	for i in range(len(against)):
		msg += "{} is strong against {} at {}. \n".format(name, against[i], locs[i])
	return msg

def format_partner_msg(name, partners):
	msg = ""
	for i in range(len(partners)):
		msg += "{} goes well with {}. \n".format(partners[i], name)
	return msg

def format_tip_msg(name, tips):
	msg = "To beat {}... \n".format(name)
	for i in range(len(tips)):
		msg += "{} \n".format(tips[i])
	return msg

if __name__ == '__main__':
	qryChamp = 'sss'
	if valid_champ(qryChamp):
		message = format_counter_msg(qryChamp.capitalize())
		print(message)
	else:
		message = "Invalid Champion... Don't play League if you can't type..."
		print(message)
	









