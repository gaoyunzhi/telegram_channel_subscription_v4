import traceback as tb
import yaml
import time
import export_to_telegraph
from common import telegraph_token
import re

class _Source(object):
    def __init__(self):
        self.db = "db/source.yaml"
        try:
            with open(self.db) as f:
                self.source = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            tb.print_exc()
            self.source = {}

    def add(self, chat_id):
        if chat_id not in self.source:
            self.source[chat_id] = 0
            self.save()
            return 'success'
        return 'source already added'

    def remove(self, chat_id):
        if chat_id in self.source:
            self.source.pop(chat_id, None)
            return 'success'
        return 'no such source'

    def iterate(self, chat_id, max):
        return [167] # testing
        # while self.source[chat_id] < max:
        #     self.source[chat_id] += 1
        #     save()
        #     yield self.source[chat_id]

    def save(self):
        with open(self.db, 'w') as f:
            f.write(yaml.dump(self.source, sort_keys=True, indent=2))

class _Subscription(object):
    def __init__(self):
        self.db = "db/subscription.yaml"
        try:
            with open(self.db) as f:
                self.subscription = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            tb.print_exc()
            self.subscription = {}

    def add(self, x, mode):
        if x not in self.subscription or self.subscription[x]['mode'] != mode:
            self.subscription[x] = mode
        self.save()

    def remove(self, x):
        self.subscription.pop(x, None)

    def save(self):
        with open(self.db, 'w') as f:
            f.write(yaml.dump(self.subscription, sort_keys=True, indent=2))

def getLan(title):
    if re.search(u'[\u4e00-\u9fff]', title):
        return 'zh'
    return 'en'

class _Pool(object):
    def __init__(self):
        self.db = "db/pool.yaml"
        try:
            with open(self.db) as f:
                self.pool = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            tb.print_exc()
            self.pool = {}

    def add(self, x):
        export_to_telegraph.token = telegraph_token
        self.pool[x] = {
            "view": export_to_telegraph.get(x['view']),
            "language": getLan(x['title']),
        }    
        self.save()

    def save(self):
        with open(self.db, 'w') as f:
            f.write(yaml.dump(self.pool, sort_keys=True, indent=2))

class _Sent(object):
    def __init__(self):
        self.db = "db/sent.yaml"
        try:
            with open(self.db) as f:
                self.sent = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            tb.print_exc()
            self.sent = {}

    def forget(self, x):
        self.sent.pop(x, None)
        self.save()

    def add(self, gid, url):
        if not gid in self.sent:
            self.sent[gid] = set()
        self.save()

    def save(self):
        with open(self.db, 'w') as f:
            f.write(yaml.dump(self.sent, sort_keys=True, indent=2))

Subscription = _Subscription()
Sent = _Sent()
Pool = _Pool()
Source = _Source()