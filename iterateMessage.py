from db import Sent, Pool, Subscription
import random
import export_to_telegraph
from common import telegraph_token

def iterateMessage(chat_id):
	mode = Subscription.db.get(chat_id)
	sent = Sent.db.get(chat_id, set())
	potential_urls = [url for url in Pool.db \
		if url not in sent and Pool.db[url]['language'] == mode]
	if len(potential_urls) == 0:
		Sent.forget(chat_id)
		potential_urls = [url for url in Pool.db \
			if url not in sent and Pool.db[url]['language'] == mode]
	for url in random.sample(potential_urls, min(len(potential_urls), 2)):
		Pool.add(url) # update url info
	potential_urls = [(Pool.db[url]['view'], url) for url in potential_urls]
	potential_urls.sort(reverse=True)
	_, url = potential_urls[0]
	Sent.add(chat_id, url)
	export_to_telegraph.token = telegraph_token
	r = export_to_telegraph.export(url)
	return r or url


