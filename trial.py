

import json
import time
import unidecode
import urllib.request
import requests

counter_cols = ['Top Counter', 'Second Counter', 'Third Counter', 'Fourth Counter', 'Fifth Counter', 'Sixth Counter']
order_cols = ['First Counter', 'Second Counter', 'Third Counter', 'Fourth Counter', 'Fifth Counter', 'Sixth Counter']
against_cols = ['First Strong Against', 'Second Strong Against', 'Third Strong Against', 'Fourth Strong Against', 'Fifth Strong Against', 'Sixth Strong Against']
partner_cols = ['First Good Partner', 'Second Good Partner', 'Third Good Partner', 'Fourth Good Partner', 'Fifth Good Partner', 'Sixth Good Partner']
tips_cols = ['Counter Tip One','Counter Tip Two','Counter Tip Three','Counter Tip Four']

response = requests.get("https://api.myjson.com/bins/tkg0v")
data = json.loads(response.text)

from bs4 import BeautifulSoup

def valid_champ(name):
	champs = get_all_champions()
	if name in champs or name.capitalize() in champs:
		return True
	else:
		return False

def get_all_champions():
	# JSON is hosted at myjson.com as well just in case
	# url = 'https://api.myjson.com/bins/tkg0v'
	allChampions = []
	for champ in data:
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
	if not valid_champ(name):
		print("input " + name)
		return -1, -1
	counters = []
	locs = []
	for champs in data:
		if champs['Champion Names'] == name:
			for col in counter_cols:
				counters.append(parse_name(champs[col]))
			for col in get_loc_names(order_cols):
				locs.append(champs[col])
	return counters, locs

def get_strong_against(name):
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
	parters = []
	for champs in data:
		if champs['Champion Names'] == name:
			for col in partner_cols:
				parters.append(parse_name(champs[col]))
	return parters	

def get_tips(name):
	tips = []
	for champs in data:
		if champs['Champion Names'] == name:
			for col in tips_cols:
				tips.append(parse_name(champs[col]))	
	return tips

def format_counter_msg(name):
	counters, locs = get_counter(name)
	if counters == -1 or locs == -1:
		return "Invalid input"
	else:
		msg = ""
		for i in range(len(counters)):
			msg += "{} counters {} at {}. \n".format(counters[i], name, locs[i])
		return msg

def format_against_msg(name):
	against, locs = get_strong_against(name)
	if against == -1 or locs == -1:
		return "Invalid input"
	msg = ""
	for i in range(len(against)):
		msg += "{} is strong against {} at {}. \n".format(name, against[i], locs[i])
	return msg

def format_partner_msg(name):
	partners = get_partner(name)
	if partners == -1:
		return "Invalid input"
	msg = ""
	for i in range(len(partners)):
		msg += "{} goes well with {}. \n".format(partners[i], name)
	return msg

def format_tip_msg(name):
	tips = get_tips(name)
	if tips == -1:
		return "Invalid input"
	msg = "To beat {}... \n".format(name)
	for i in range(len(tips)):
		msg += "{} \n".format(tips[i])
	return msg

def get_tier_list():
    target_url = 'http://www.eyny.com/forum-205-1.html'
    print('Start parsing website...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ''
    return content



if __name__ == '__main__':
	db = get_all_champions()
	print(format_counter_msg("Garen"))








