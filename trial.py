

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

def get_tier_list_op():
	headers = {'Accept-Language': 'en-US,en;q=0.8'}
	target_url = 'https://na.op.gg/champion/statistics'
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True, headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')
	champNames = soup.find("div", {"class": "l-champion-index-content--side"}).findAll("div", {"class":"champion-index-table__name"})
	#table = side.select(".champion-index-table__name")
	champTier = soup.find("div", {"class": "l-champion-index-content--side"}).findAll('td', limit=7)
	content = champTier
	champs = []
	for name in champNames:
		champs.append(name.text)
	result = []
	for inside in champTier:
		result.append(inside.text)
	lala = soup.find("div", {"class":"l-champion-index-content--side"})
	return lala

pos = ["Top", "JG", "Mid", "Bottom", "Sup"]

def get_tier_list_moba():
	target_url = "https://www.mobachampion.com/tier-list/"
	headers = {'Accept-Language': 'en-US,en;q=0.8'}
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True, headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')
	champs = soup.findAll("h3", text="God Tier")
	tier = {}
	for i in range(len(pos)):
		curr = []
		for lane in champs[i].find_next_sibling("div").findAll("div",{"class":"caption"}):
			curr.append(lane.text)
		tier[pos[i]] = curr
	return tier

def get_lane_tier(lane):
	if lane not in pos:
		return -1
	tiers = get_tier_list_moba()
	return tiers[lane]

def format_tier_msg(pos):
	champs = get_lane_tier(pos)
	if champs == -1:
		return "Invalid Input"
	msg = "The God Tier list for {} ...\n".format(pos)
	for champ in champs:
		msg += "{}...".format(champ)
	return msg

if __name__ == '__main__':
	print(get_tier_list_moba())







