from common import tele, debug_group
from telegram_util import log_on_fail, getSoup
from db import Subscription, Source, Pool
from iterateMessage import iterateMessage
from bs4 import BeautifulSoup
import threading

INTERVAL = 60 * 24 * 60	

test_channel = -1001138008921

def getMaxMessageId(soup):
	r = 0
	for x in soup.find_all("div", class_="js-widget_message"):
		if x.get('data-post'):
			r = max(r, int(x['data-post'].split('/')[-1]))
	return r

@log_on_fail(debug_group)
def loopImp():
	print('here1')
	for chat_id in Source.source:
		print('here2')
		chat = tele.bot.getChat(chat_id)
		# soup = getSoup('https://telete.in/s/' + chat.username)
		max_message_id = 10 # getMaxMessageId(soup)
		print('here3', Source.iterate(chat_id, max_message_id))
		for message_id in Source.iterate(chat_id, max_message_id):
			print('here4')
			print(message_id)
			try:
				print('here')
				print(max_message_id, test_channel, tele.bot.getChat(chat_id).username, message_id)
				msg = tele.bot.forward_message(chat_id = test_channel, from_chat_id = chat_id, message_id = message_id)
			except Exception as e:
				print("Warning: forwarding error: " + str(e))
				return # testing
				continue
			print('here')
			for item in msg.entities:
				if (item["type"] == "url"):
					url = msg.text[item["offset"]:][:item["length"]]
					if not '://' in url:
						url = "https://" + url
					if '://telegra.ph' in url:
						Pool.add(url)
	for chat_id in Subscription.subscription:
		tele.bot.send_message(iterateMessage(chat_id))

def loop():
	loopImp()
	threading.Timer(INTERVAL, loop).start() 

loop()

