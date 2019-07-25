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

POS = ["Top", "Jg", "Mid", "Bottom", "Sup"]

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
	if name in data:
		return True
	else:
		return False

def get_counter_champs(champ):
	if not validate_champ(name):
		return -1, -1
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

def format_counter_msg(name):
	counters, locs = get_counter_champs(name)
	EYE_STR = get_emoji(EYE)
	msg = "These champs counter {} ...".format(name)
	if counters == -1 or locs == -1:
		return "Invalid input"
	for i in range(len(counters)):
		msg += "\n{}{} at {}.".format(EYE_STR, counters[i], locs[i])
	return msg

def get_against_champs(champ):
	if not validate_champ(name):
		return -1, -1
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

def format_against_msg(name):
	against, locs = get_against_champs(name)
	THUMB_STR = get_emoji(THUMB)
	msg = "{} is strong against... ".format(name)
	if against == -1 or locs == -1:
		return "Invalid input"
	for i in range(len(against)):
		msg +=  "\n{}{} at {}.".format(THUMB_STR, against[i], locs[i])
	return msg

def get_tgt_champs(champ):
	if not validate_champ(name):
		return -1, -1
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

def format_partner_msg(name):
	partners = get_tgt_champs(name)
	HANDS_STR = get_emoji(HANDS)
	msg = "The following champs go well with {} ... ".format(name)
	if partners == -1:
		return "Invalid input"
	for i in range(len(partners)):
		msg += "\n{}{}.".format(HANDS_STR, partners[i])
	return msg

def get_counter_tips(champ):
	if not validate_champ(name):
		return -1, -1
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

def format_tip_msg(name):
	tips = get_counter_tips(name)
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
	for i in range(len(POS)):
		curr = []
		for lane in champs[i].find_next_sibling("div").findAll("div",{"class":"caption"}):
			curr.append(lane.text)
		tier[pos[i]] = curr
	return tier

def get_lane_tier(lane):
	if lane not in POS:
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
	for i in range(len(POS)):
		lane = tb[i].findAll("li")
		lane_rates = {}
		for champ in lane:
			lane_rates[champ.find("a")['title']] = champ.find("span").text
		all_rates[POS[i]] = lane_rates
	return all_rates

def get_lane_rates(lane):
	if lane not in POS:
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

def format_all_champs():
	data = get_champs_list()
	msg = "Here are the available champs...\n"
	for champ in data:
		msg+= " {},".format(champ)
	msg = msg[:-1]
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
		url = "https://scontent.ftpe8-2.fna.fbcdn.net/v/t31.0-8/10928973_1529093804018213_3930372778290831110_o.png?_nc_cat=101&_nc_oc=AQlzdGY_qFaEN84UJnskm_4hKRbpUpYcS4L8I-N4QKRPvKm7l6bydftlQ5Q2E_NHAus&_nc_ht=scontent.ftpe8-2.fna&oh=1b3dfd30b799c696f40c53d5e1fe6b5a&oe=5DA8FBB6"
		image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
		line_bot_api.reply_message(event.reply_token, image_message)
		return 0

	if input_str == 'names' or input_str == "Names":
		reply_message = format_all_champs()
		message = TextSendMessage(reply_message)
		line_bot_api.reply_message(event.reply_token, message)
		return 0

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

