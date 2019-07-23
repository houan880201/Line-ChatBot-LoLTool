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

counter_cols = ['1st Counter', '2nd Counter', '3rd Counter', '4th Counter', '5th Counter', '6th Counter']
against_cols = ['1st Strong Against', '2nd Strong Against', '3rd Strong Against', '4th Strong Against', '5th Strong Against', '6th Strong Against']
partner_cols = ['1st Good Partner', '2nd Good Partner', '3rd Good Partner', '4th Good Partner', '5th Good Partner', '6th Good Partner']
tips_cols = ['Counter Tip One','Counter Tip Two','Counter Tip Three','Counter Tip Four']

def valid_champ(name):
	champs = get_all_champions()
	if name in champs or name.capitalize() in champs:
		return True
	else:
		return False

def get_all_champions():
	# JSON is hosted at myjson.com as well just in case
	# url = 'https://api.myjson.com/bins/tkg0v'
	response = requests.get("https://api.myjson.com/bins/tkg0v")
	data = json.loads(response.text)
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
	response = requests.get("https://api.myjson.com/bins/tkg0v")
	data = json.loads(response.text)
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
	response = requests.get("https://api.myjson.com/bins/tkg0v")
	data = json.loads(response.text)
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
	response = requests.get("https://api.myjson.com/bins/tkg0v")
	data = json.loads(response.text)
	parters = []
	for champs in data:
		if champs['Champion Names'] == name:
			for col in partner_cols:
				parters.append(parse_name(champs[col]))
	return parters	

def get_tips(name):
	response = requests.get("https://api.myjson.com/bins/tkg0v")
	data = json.loads(response.text)
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

def format_against_msg(name):
	against, locs = get_strong_against(name)
	msg = ""
	for i in range(len(against)):
		msg += "{} is strong against {} at {}. \n".format(name, against[i], locs[i])
	return msg

def format_partner_msg(name):
	partners = get_partner(name)
	msg = ""
	for i in range(len(partners)):
		msg += "{} goes well with {}. \n".format(partners[i], name)
	return msg

def format_tip_msg(name):
	tips = get_tips(name)
	msg = "To beat {}... \n".format(name)
	for i in range(len(tips)):
		msg += "{} \n".format(tips[i])
	return msg


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



# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	input_str = event.message.text
	command = input_str.split[0]
	name = input_str.split[1]

	message = TextSendMessage("Hi " + command + " " + name)
	line_bot_api.reply_message(event.reply_token, message)

	#msg = TextSendMessage(str(res))
	#line_bot_api.reply_message(event.reply_token, msg)

	'''
	if valid_champ(qryChamp):
		line_bot_api.reply_message(event.reply_token, message)
		name = event.message.text
		line_bot_api.reply_message(event.reply_token, message)
		message = format_counter_msg(name.capitalize())
		line_bot_api.reply_message(event.reply_token, message)
	else:
		line_bot_api.reply_message(event.reply_token, message)
		message = TextSendMessage("Invalid Champion... Don't play League if you can't type...")
		line_bot_api.reply_message(event.reply_token, message)
	'''


import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

