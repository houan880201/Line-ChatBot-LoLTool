

import json
import time
import unidecode
import urllib.request
import requests
import numpy as np

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

roles = ["top", "jungle", "middle", "adc", "support"]

def get_champ_win_rates():
	target_url = "https://www.lolrift.com/statistics"
	headers = {'Accept-Language': 'en-US,en;q=0.8'}
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True, headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')
	tb = soup.findAll("ul", {"class":"stats_ratesChampList"}, limit=5)
	all_rates = {}
	for i in range(len(pos)):
		lane = tb[i].findAll("li")
		lane_rates = {}
		for champ in lane:
			lane_rates[champ.find("a")['title']] = champ.find("span").text
		all_rates[pos[i]] = lane_rates
	return all_rates

def get_op_build(champion, lane):
	target_url = "https://tw.op.gg/champion/{}/statistics/{}".format(champion.lower(), lane.lower())
	headers = {'Accept-Language': 'en-US'}
	print('Start parsing website...')
	rs = requests.session()
	rs.headers.update({"Accept-Language": "en-US,en;q=0.5"})
	res = rs.get(target_url, verify=True, headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')
	thead = soup.find("div", {"class":"l-champion-statistics-content__main"}).findAll("table")[0].findAll('thead')[0]
	tbody = soup.find("div", {"class":"l-champion-statistics-content__main"}).findAll("table")[0].findAll('tbody')[0]
	content = tbody
	return content

def get_counter_tips(champ):
	target_url = "https://lolcounter.com/champions/{}".format(champ)
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True)
	soup = BeautifulSoup(res.text, 'html.parser')
	tips = soup.findAll("span",{"class": "_tip"})
	content = []
	for tip in tips:
		content.append(tip.text.rstrip('\n'))
	return content

def get_counter_champs(champ):
	target_url = "https://lolcounter.com/champions/{}".format(champ)
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True)
	soup = BeautifulSoup(res.text, 'html.parser')
	champs = soup.findAll("div",{"class": "champ-block"},limit=7)[1:]
	content = []
	locs = []
	for counter in champs:
		content.append(counter.find("div",{"class":"name"}).text.rstrip('\n'))
		locs.append(counter.find("div",{"class":"lane"}).text)
	return content, locs

def get_against_champs(champ):
	target_url = "https://lolcounter.com/champions/{}".format(champ)
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True)
	soup = BeautifulSoup(res.text, 'html.parser')
	champs = soup.find("div",{"class": "strong-block"}).findAll("div", {"class":"champ-block"}, limit=6)
	names = []
	locs = []
	for champ in champs:
		names.append(champ.find("div",{"class":"name"}).text)
		locs.append(champ.find("div",{"class":"lane"}).text)
	return names, locs

def get_tgt_champs(champ):
	target_url = "https://lolcounter.com/champions/{}".format(champ)
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True)
	soup = BeautifulSoup(res.text, 'html.parser')
	champs = soup.find("div",{"class": "good-block"}).findAll("div", {"class":"champ-block"}, limit=6)
	names = []
	for champ in champs:
		names.append(champ.find("div",{"class":"name"}).text)
	return names

def get_champs_list():
	target_url = "https://leagueoflegends.fandom.com/wiki/List_of_champions"
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True)
	soup = BeautifulSoup(res.text, 'html.parser')
	tds = soup.findAll("td", {"style":"text-align:left;"})
	content = []
	for td in tds:
		content.append(td.find("span", {"style":"white-space:normal;"}).find("a")['title'])
	return content

def validate_champ(name):
	name = name.capitalize()
	data = get_champs_list()
	print(type(data))
	if name in data:
		return True
	else:
		return False

def get_level_order(name, pos):
	if not validate_champ(name):
		return -1
	target_url = ""
	if pos == -1:
		target_url = "https://champion.gg/champion/{}".format(name)
	else:
		target_url = "https://champion.gg/champion/{}/{}".format(name, pos)
	print('Start parsing website...')
	rs = requests.session()
	res = rs.get(target_url, verify=True)
	soup = BeautifulSoup(res.text, 'html.parser')
	content = soup.find("div",{"class":"skill-order"}).findAll("div",{"class":"skill-selections"})[1:]
	skill = ["" for x in range(18)]
	for row in content:
		spans = [words.text for words in row.findAll("span")]
		for i in range(len(spans)):
			if spans[i]:
				skill[i] = spans[i]
	return skill

def format_leveling_msg(name, pos):
	order = get_level_order(name, pos)
	if order == -1:
		return "Invalid Input"
	if pos == -1:
		msg = "The skills order for {} is...".format(name)
	else:
		msg = "The skills order for {} at {} is...".format(name, pos)
	for i in range(len(order)):
		msg += "\n{} -- {}".format(i+1, order[i])
	return msg


if __name__ == '__main__':
	a = 18 / 2
	print(type(int(a)))








