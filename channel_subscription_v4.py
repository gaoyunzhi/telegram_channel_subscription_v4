#!/usr/bin/env python3
# -*- coding: utf-8 -*-

INTERVAL = 60 * 24 * 60	

from telegram.ext import Updater, MessageHandler, Filters

from telegram_util import splitCommand, log_on_fail, autoDestroy, formatChat
from db import Source
import loop
from .common import tele, debug_group

def commandImp(msg):
	autoDestroy(msg)
	command, text = splitCommand(msg.text)
	if command == "s4_get":
		pass # TODO
	elif command == "s4_subscribe":
		# subscription mode
		pass # TODO
	elif command == "s4_source_add":
		Source.add(tele.bot.getChat(text).id)
	elif command == "s4_source_delete":
		Source.remove(tele.bot.getChat(text).id)
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