import traceback as tb
import yaml
import time

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

    def add(self, chat):
        self.source.add(chat.id);
        self.save()

    def remove(self, chat):
        self.source.pop(chat.id, None)

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
            self.subscription[x] = {
                "start": 0,
                "mode": mode,
            }
        self.save()

    def remove(self, x):
        self.subscription.pop(x, None)

    def save(self):
        with open(self.db, 'w') as f:
            f.write(yaml.dump(self.subscription, sort_keys=True, indent=2))

class _Pool(object):
    def __init__(self):
        self.db = "db/pool.yaml"
        try:
            with open(self.db) as f:
                self.pool = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            tb.print_exc()
            self.pool = set()

    def add(self, x):
        self.pool.add()
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
            self.sent = set()

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