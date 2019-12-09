#!/usr/bin/env python3
# -*- coding: utf-8 -*-

INTERVAL = 60 * 24 * 60	

from telegram.ext import Updater, MessageHandler, Filters

import export_to_telegraph
from html_telegraph_poster import TelegraphPoster
import yaml
from telegram_util import splitCommand, log_on_fail, autoDestroy
from db import Subscription, Sent, Pool
import loop

with open('CREDENTIALS') as f:
    CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)

debug_group = tele.bot.get_chat(-1001198682178)

def msgTelegraphToken(msg):
	user_id = msg.from_user.id
	if user_id in TELEGRAPH_TOKENS:
		p = TelegraphPoster(access_token = TELEGRAPH_TOKENS[user_id])
	else:
		p = TelegraphPoster()
		r = p.create_api_token(msg.from_user.first_name, msg.from_user.username)
		TELEGRAPH_TOKENS[user_id] = r['access_token']
		saveTelegraphTokens()
	msgAuthUrl(msg, p)

def msgAuthUrl(msg, p):
	r = p.get_account_info(fields=['auth_url'])
	msg.reply_text('Use this url to login in 5 minutes: ' + r['auth_url'])

def getTelegraph(msg, url):
	user_id = msg.from_user.id
	if user_id not in TELEGRAPH_TOKENS:
		msgTelegraphToken(msg)
	export_to_telegraph.token = TELEGRAPH_TOKENS[user_id]
	return export_to_telegraph.export(url, True, force = True) # DEBUG, remove second param when go prod

@log_on_fail(debug_group)
def export(update, context):
	msg = update.message
	for item in msg.entities:
		if (item["type"] == "url"):
			url = msg.text[item["offset"]:][:item["length"]]
			if not '://' in url:
				url = "https://" + url
			u = getTelegraph(msg, url)
			msg.reply_text(u)
			if msg.from_user.id not in known_users:
				r = debug_group.send_message( 
					text=getDisplayUser(msg.from_user) + ': ' + u, 
					parse_mode='Markdown')

@log_on_fail(debug_group)
def command(update, context):
	msg = update.effective_message
    autoDestroy(msg)
    command, text = splitCommand(msg.text)
    if command == "cn_article_get":
    	pass # TODO
    elif command == "cn_article_subscribe":
    	pass # TODO
    elif command == "an_article_source_add":
    	sub_db.add(text)
    elif command == "an_article_source_delete":
    	sub_db.remove(text)
    else:
    	return
    autoDestroy(msg.reply_text("success"))

tele.dispatcher.add_handler(MessageHandler(Filters.update.channel_posts & Filters.command, command))

@log_on_fail(debug_group)
def loopImp():
    global queue
    queue_to_push_back = []
    while not queue.empty():
        item = queue.pop()
        subscriber, chat_id, message_id = item
        if not isReady(subscriber):
            queue_to_push_back.append(item)
            continue
        try:
            if item in cache:
                tryDeleteById(subscriber, cache[item])
            r = tele.bot.forward_message(
                chat_id = subscriber,
                from_chat_id = chat_id,
                message_id = message_id)
            cache[item] = r.message_id
            dup_msg = findDup(r)
            if dup_msg:
                tryDeleteById(subscriber, dup_msg)
            dbu.setTime(subscriber)
        except Exception as e:
            if str(e) not in ['Message to forward not found', 'Message_id_invalid']:
                print(e)
                tb.print_exc()
                print(item)
                debug_group.send_message(str(e))
                queue_to_push_back.append(item)
    for item in queue_to_push_back[::-1]:
        queue.append(item)

def loop():
    loopImp()
    threading.Timer(INTERVAL, loop).start() 

# threading.Timer(1, loop).start()

# tele.start_polling()
# tele.idle()