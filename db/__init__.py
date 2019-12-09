import traceback as tb
import yaml
import time

class Subscription(object):
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
            f.write(yaml.dump(self.pool, sort_keys=True, indent=2))

class Pool(object):
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

class Sent(object):
    def __init__(self):
        self.db = "db/sent.yaml"
        try:
            with open(self.db) as f:
                self.sent = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            tb.print_exc()
            self.sent = set()

    def forget(self, gid):
        self.sent = set([(x, url) for x, url in self.sent if x != gid])
        self.save()

    def add(self, gid, url):
        self.sent.add((gid, url))
        self.save()

    def save(self):
        with open(self.db, 'w') as f:
            f.write(yaml.dump(self.sent, sort_keys=True, indent=2))