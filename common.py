import yaml
from telegram.ext import Updater

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)

telegraph_token = CREDENTIALS['telegraph_token']

debug_group = tele.bot.get_chat(-1001198682178)