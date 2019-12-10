#!/usr/bin/env python3
# -*- coding: utf-8 -*-

INTERVAL = 60 * 24 * 60	

from telegram.ext import Updater, MessageHandler, Filters

from telegram_util import splitCommand, log_on_fail, autoDestroy, formatChat, matchKey
from db import Source, Subscription
import loop
from common import tele, debug_group
from iterateMessage import iterateMessage
import traceback as tb

def commandImp(msg):
	autoDestroy(msg)
	command, text = splitCommand(msg.text)
	print(command, text)
	if "s4_g" in command:
		return msg.reply_text(iterateMessage(msg.chat.id), quote=False)
	elif matchKey(command, ["s4_source_add", "s4_sa", "s4_a"]):
		autoDestroy(msg.reply_text(Source.add(tele.bot.getChat(text).id)))
	elif matchKey(command, ["s4_source_delete", "s4_sd", "s4_d"]):
		autoDestroy(msg.reply_text(Source.remove(tele.bot.getChat(text).id)))
	elif matchKey(command, ["s4_source_list", "s4_sl", "s4_l"]):
		pass # intentional
	elif matchKey(command, ["s4_sub", "s4_s"]):
		Subscription.add(msg.chat.id, text)
	else:
		return
	print('here1.2')
	if matchKey(command, ["s4_source", "s4_sl", "s4_l", "s4_sa", "s4_a", "s4_sd", "s3_d"]):
		print('here2')
		sources = [str(index) + ': ' + formatChat(tele.bot, chat_id) for \
            index, chat_id in enumerate(subscriptions)]
		autoDestroy(msg.reply_text('Source list: \n\n' + '\n'.join(sources), 
            parse_mode='Markdown', 
            disable_web_page_preview=True))
	else:
		autoDestroy(msg.reply_text("success"))

def command(update, context):
	print('here')
	msg = update.effective_message
	try:
		commandImp(msg)
	except Exception as e:
		print('here3')
		autoDestroy(msg.reply_text(str(e)))
		tb.print_exc()
		raise e
	print('here4')

tele.dispatcher.add_handler(MessageHandler(Filters.command, command))

tele.start_polling()
tele.idle()