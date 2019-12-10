from db import Sent, Pool, Subscription
import random

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
	_, url = potential_urls.sort(reverse=True)[0]
	Sent.add(chat_id, url)
	return url


