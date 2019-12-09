from .common import tele, debug_group
from telegram_util import log_on_fail

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

