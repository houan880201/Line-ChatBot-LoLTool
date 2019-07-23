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
#from bs4 import BeautifulSoup

counter_cols = ['Top Counter', 'Second Counter', 'Third Counter', 'Fourth Counter', 'Fifth Counter', 'Sixth Counter']
order_cols = ['First Counter', 'Second Counter', 'Third Counter', 'Fourth Counter', 'Fifth Counter', 'Sixth Counter']
against_cols = ['First Strong Against', 'Second Strong Against', 'Third Strong Against', 'Fourth Strong Against', 'Fifth Strong Against', 'Sixth Strong Against']
partner_cols = ['First Good Partner', 'Second Good Partner', 'Third Good Partner', 'Fourth Good Partner', 'Fifth Good Partner', 'Sixth Good Partner']
tips_cols = ['Counter Tip One','Counter Tip Two','Counter Tip Three','Counter Tip Four']

response = requests.get("https://api.myjson.com/bins/tkg0v")
data = response.json()

ERROR_MSG = "Type 'help' to learn... stupid..."

BULB = b"\x00\x10\x00\x77"

HELP_MSG = ("\uDBC0\uDC84 The following are working commands: 'counter' for finding countering champions against your opponent,"+
		" 'matchup' for finding good matchups for your pick, 'partner' for finding good "+
		"partner along with your pick, 'tips' for tips playing against your opponent's pick "+ 
		"and 'help' for getting help to use this bot...")

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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	input_str = event.message.text

	if input_str == "":
		reply_message = "Type something... \n" + ERROR_MSG
		message = TextSendMessage(reply_message)
		line_bot_api.reply_message(event.reply_token, message)
		return 0

	if input_str == "help":
		reply_message = HELP_MSG
		message = TextSendMessage(reply_message)
		line_bot_api.reply_message(event.reply_token, message)
		return 0

	if input_str == "yo":
		line_bot_api.reply_message(event.reply_token,
		{
		  "type": "carousel",
		  "contents": [
		    {
		      "type": "bubble",
		      "hero": {
		        "type": "image",
		        "size": "full",
		        "aspectRatio": "20:13",
		        "aspectMode": "cover",
		        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"
		      },
		      "body": {
		        "type": "box",
		        "layout": "vertical",
		        "spacing": "sm",
		        "contents": [
		          {
		            "type": "text",
		            "text": "Arm Chair, White",
		            "wrap": true,
		            "weight": "bold",
		            "size": "xl"
		          },
		          {
		            "type": "box",
		            "layout": "baseline",
		            "contents": [
		              {
		                "type": "text",
		                "text": "$49",
		                "wrap": true,
		                "weight": "bold",
		                "size": "xl",
		                "flex": 0
		              },
		              {
		                "type": "text",
		                "text": ".99",
		                "wrap": true,
		                "weight": "bold",
		                "size": "sm",
		                "flex": 0
		              }
		            ]
		          }
		        ]
		      },
		      "footer": {
		        "type": "box",
		        "layout": "vertical",
		        "spacing": "sm",
		        "contents": [
		          {
		            "type": "button",
		            "style": "primary",
		            "action": {
		              "type": "uri",
		              "label": "Add to Cart",
		              "uri": "https://linecorp.com"
		            }
		          },
		          {
		            "type": "button",
		            "action": {
		              "type": "uri",
		              "label": "Add to wishlist",
		              "uri": "https://linecorp.com"
		            }
		          }
		        ]
		      }
		    },
		    {
		      "type": "bubble",
		      "hero": {
		        "type": "image",
		        "size": "full",
		        "aspectRatio": "20:13",
		        "aspectMode": "cover",
		        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_6_carousel.png"
		      },
		      "body": {
		        "type": "box",
		        "layout": "vertical",
		        "spacing": "sm",
		        "contents": [
		          {
		            "type": "text",
		            "text": "Metal Desk Lamp",
		            "wrap": true,
		            "weight": "bold",
		            "size": "xl"
		          },
		          {
		            "type": "box",
		            "layout": "baseline",
		            "flex": 1,
		            "contents": [
		              {
		                "type": "text",
		                "text": "$11",
		                "wrap": true,
		                "weight": "bold",
		                "size": "xl",
		                "flex": 0
		              },
		              {
		                "type": "text",
		                "text": ".99",
		                "wrap": true,
		                "weight": "bold",
		                "size": "sm",
		                "flex": 0
		              }
		            ]
		          },
		          {
		            "type": "text",
		            "text": "Temporarily out of stock",
		            "wrap": true,
		            "size": "xxs",
		            "margin": "md",
		            "color": "#ff5551",
		            "flex": 0
		          }
		        ]
		      },
		      "footer": {
		        "type": "box",
		        "layout": "vertical",
		        "spacing": "sm",
		        "contents": [
		          {
		            "type": "button",
		            "flex": 2,
		            "style": "primary",
		            "color": "#aaaaaa",
		            "action": {
		              "type": "uri",
		              "label": "Add to Cart",
		              "uri": "https://linecorp.com"
		            }
		          },
		          {
		            "type": "button",
		            "action": {
		              "type": "uri",
		              "label": "Add to wish list",
		              "uri": "https://linecorp.com"
		            }
		          }
		        ]
		      }
		    },
		    {
		      "type": "bubble",
		      "body": {
		        "type": "box",
		        "layout": "vertical",
		        "spacing": "sm",
		        "contents": [
		          {
		            "type": "button",
		            "flex": 1,
		            "gravity": "center",
		            "action": {
		              "type": "uri",
		              "label": "See more",
		              "uri": "https://linecorp.com"
		            }
		          }
		        ]
		      }
		    }
		  ]
		})
		return 0

	splited = input_str.split(' ')

	if len(splited) == 1:
		reply_message = "One word only...? \n" + ERROR_MSG
		message = TextSendMessage(reply_message)
		line_bot_api.reply_message(event.reply_token, message)
		return 0

	command = splited[0].lower()
	champ = splited[1].capitalize()

	if command == "counter":
		reply_message = format_counter_msg(champ)

	elif command == "partner":
		reply_message = format_partner_msg(champ)

	elif command == "matchup":
		reply_message = format_against_msg(champ)

	elif command == 'tip':
		reply_message = format_tip_msg(champ)

	else:
		reply_message = "Type a valid command kid..." + ERROR_MSG

	message = TextSendMessage(reply_message)
	line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

