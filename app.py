from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('JeJ+t2/bwCVSFVyBTdWPBO8VVeY826+LV3W/S/71XUygxI+4Epp8OXfzCXyFuucBoyCvfYED1aoH1AHXiUIzWB7FyQjFLHNQ+biWId8JAXrSRbwVyacCy/3z61LLHS/DfLyQUO9c/PJInwacasPflgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('88095fca9a435628a8522c92f8d601e9')

import urllib
import requests
import random

from bs4 import BeautifulSoup

#from bs4 import BeautifulSoup

counter_cols = ['Top Counter', 'Second Counter', 'Third Counter', 'Fourth Counter', 'Fifth Counter', 'Sixth Counter']
order_cols = ['First Counter', 'Second Counter', 'Third Counter', 'Fourth Counter', 'Fifth Counter', 'Sixth Counter']
against_cols = ['First Strong Against', 'Second Strong Against', 'Third Strong Against', 'Fourth Strong Against', 'Fifth Strong Against', 'Sixth Strong Against']
partner_cols = ['First Good Partner', 'Second Good Partner', 'Third Good Partner', 'Fourth Good Partner', 'Fifth Good Partner', 'Sixth Good Partner']
tips_cols = ['Counter Tip One','Counter Tip Two','Counter Tip Three','Counter Tip Four']
pos = ["Top", "Jg", "Mid", "Bottom", "Sup"]
roles = ["top", "jungle", "middle", "adc", "support"]

response = requests.get("https://api.myjson.com/bins/tkg0v")
data = response.json()

ERROR_MSG = "Type 'help' to learn... stupid..."

EMO = b"\xF0\x9F\x98\x81"
THUMB = b"\xF0\x9F\x91\x8D"
EYE = b"\xF0\x9F\x91\x80"
HANDS = b"\xF0\x9F\x99\x8C"
BULB = b"\xF0\x9F\x92\xA1"
FIRE = b"\xF0\x9F\x94\xA5"
TROPHY = b"\xF0\x9F\x8F\x86"

def get_emoji(code):
	return code.decode('utf-8')

HELP_MSG = (get_emoji(EMO) + "The following are working commands:" +
		"\n-counter > find counter champion against input champ, "+
		"\n-matchup > find easy matchups for input champ, " +
		"\n-partner > find good partner along with input champ, " +
		"\n-tips > find tips for playing against input champ " + 
		"\n-tier > find the god tier champions for (Top, Jg, Mid, Bottom, Sup)" +
		"\n-win > find the few highest win rates for (Top, Jg, Mid, Bottom, Sup)" +
		"\n-help for getting help to use this bot... " + 
		"\n \n Use correct champion name after each command except help!")

'''
TODO:

Find Builds for champions

Find level upgrading for champions

Find champion tiers

'''


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'


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
	EYE_STR = get_emoji(EYE)
	msg = "These champs counter {} ...".format(name)
	if counters == -1 or locs == -1:
		return "Invalid input"
	for i in range(len(counters)):
		msg += "\n{}{} at {}.".format(EYE_STR, counters[i], locs[i])
	return msg

def format_against_msg(name):
	against, locs = get_strong_against(name)
	THUMB_STR = get_emoji(THUMB)
	msg = "{} is strong against... ".format(name)
	if against == -1 or locs == -1:
		return "Invalid input"
	for i in range(len(against)):
		msg +=  "\n{}{} at {}.".format(THUMB_STR, against[i], locs[i])
	return msg

def format_partner_msg(name):
	partners = get_partner(name)
	HANDS_STR = get_emoji(HANDS)
	msg = "The following champs go well with {} ... ".format(name)
	if partners == -1:
		return "Invalid input"
	for i in range(len(partners)):
		msg += "\n{}... {}.".format(HANDS_STR, partners[i])
	return msg

def format_tip_msg(name):
	tips = get_tips(name)
	BULB_STR = get_emoji(BULB)
	if tips == -1:
		return "Invalid input"
	msg = "To beat {}... ".format(name)
	for i in range(len(tips)):
		msg +=  "\n{}{} ".format(BULB_STR, tips[i])
	return msg

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
	FIRE_STR = get_emoji(FIRE)
	if champs == -1:
		return "Invalid Input"
	msg = "The God Tier list for {} in the current patch...".format(pos)
	for champ in champs:
		msg += "\n{}{}...".format(FIRE_STR,champ)
	return msg

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

def get_lane_rates(lane):
	if lane not in pos:
		return -1
	rates = get_champ_win_rates()
	return rates[lane]

def format_rates_msg(pos):
	lane_rates = get_lane_rates(pos)
	TROPHY_STR = get_emoji(TROPHY)
	if lane_rates == -1:
		return "Invalid Input"
	msg = "The win rates for the champions at {}...".format(pos)
	for champ in lane_rates:
		msg += "\n{}{} -win rate- {}".format(TROPHY_STR, champ, lane_rates[champ])
	return msg


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	input_str = event.message.text
	input_str = input_str.strip()
	if input_str == "":
		reply_message = "Type something... \n" + ERROR_MSG
		message = TextSendMessage(reply_message)
		line_bot_api.reply_message(event.reply_token, message)
		return 0

	if input_str == 'image':
		url = "opgg-static.akamaized.net/images/lol/spell/SummonerDot.png?image=w_42&amp;v=15354684000"
		image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
		line_bot_api.reply_message(event.reply_token, image_message)

	if input_str == "help" or input_str == "Help":
		reply_message = HELP_MSG
		message = TextSendMessage(reply_message)
		line_bot_api.reply_message(event.reply_token, message)
		return 0

	splited = input_str.split(' ')

	if len(splited) == 1:
		reply_message = "One word only...? \n" + ERROR_MSG
		message = TextSendMessage(reply_message)
		line_bot_api.reply_message(event.reply_token, message)
		return 0

	command = splited[0].lower()
	obj = splited[1].capitalize()

	if command == "counter":
		reply_message = format_counter_msg(obj)

	elif command == "partner":
		reply_message = format_partner_msg(obj)

	elif command == "matchup":
		reply_message = format_against_msg(obj)

	elif command == 'tips':
		reply_message = format_tip_msg(obj)

	elif command == 'tier':
		reply_message = format_tier_msg(obj)

	elif command == 'win':
		reply_message = format_rates_msg(obj)

	else:
		reply_message = "Type a valid command kid..." + ERROR_MSG

	message = TextSendMessage(reply_message)
	line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

