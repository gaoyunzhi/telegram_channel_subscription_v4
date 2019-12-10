from common import tele, debug_group
from telegram_util import log_on_fail, getSoup
from db import Subscription, Source, Pool
from iterateMessage import iterateMessage
from bs4 import BeautifulSoup
import threading

INTERVAL = 60 * 12 * 60	

test_channel = -1001138008921

def getMaxMessageId(soup):
	r = 0
	for x in soup.find_all("div", class_="js-widget_message"):
		if x.get('data-post'):
			r = max(r, int(x['data-post'].split('/')[-1]))
	return r

@log_on_fail(debug_group)
def loopImp():
	requests_count = 0
	for chat_id in Source.db:
		chat = tele.bot.getChat(chat_id)
		soup = getSoup('https://telete.in/s/' + chat.username)
		max_message_id = getMaxMessageId(soup)
		username = tele.bot.getChat(chat_id).username
		for message_id in Source.iterate(chat_id, max_message_id):
			url = "https://telete.in/%s/%d?embed=1" % (username, message_id)
			soup = getSoup(url)
			text = soup.find('div', class_='tgme_widget_message_text')
			requests_count += 1
			if not text:
				continue
			for item in text.find_all():
				if not item or not item.text:
					continue
				for url in item.text.split():
					if not '://' in url:
						url = "https://" + url
					if '://telegra.ph' in url:
						Pool.add(url)
			if requests_count > 30:
				break
	for chat_id in Subscription.db:
		tele.bot.send_message(chat_id = chat_id, text = iterateMessage(chat_id))

def loop():
	loopImp()
	threading.Timer(INTERVAL, loop).start() 

loop()

