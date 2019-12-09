#!/usr/bin/env python3
# -*- coding: utf-8 -*-

INTERVAL = 60 * 24 * 60	

from telegram.ext import Updater, MessageHandler, Filters

import export_to_telegraph
from html_telegraph_poster import TelegraphPoster
from telegram_util import splitCommand, log_on_fail, autoDestroy, formatChat
from db import Subscription, Sent, Pool
import loop
from .common import tele, debug_group


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


def commandImp(msg):
	autoDestroy(msg)
	command, text = splitCommand(msg.text)
	if command == "s4_get":
		pass # TODO
	elif command == "s4_subscribe":
		# subscription mode
		pass # TODO
	elif command == "s4_source_add":
		sub_db.add(tele.bot.getChat(text).id)
	elif command == "s4_source_delete":
		sub_db.remove(tele.bot.getChat(text).id)
	elif command == "s4_source_list":
		pass # intentional
	else:
		return
	if command.startswith(s4_source):
		sources = [str(index) + ': ' + formatChat(tele.bot, chat_id) for \
            index, chat_id in enumerate(subscriptions)]
		autoDestroy(msg.reply_text('Source list: \n\n' + '\n'.join(sources), 
            parse_mode='Markdown', 
            disable_web_page_preview=True))
	else:
		autoDestroy(msg.reply_text("success"))

def command(update, context):
	msg = update.effective_message
	try:
		commandImp(msg)
	except Exception as e:
		autoDestroy(msg.reply_text(str(e)))
		raise e

tele.dispatcher.add_handler(MessageHandler(Filters.update.channel_posts & Filters.command, command))

tele.start_polling()
tele.idle()