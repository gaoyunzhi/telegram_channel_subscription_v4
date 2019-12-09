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

    def add(self, x):
        if x not in self.subscription:
            self.subscription[x] = 0 # start item 
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

class SUBSCRIPTION(object):
    def __init__(self):
        try:
            with open('subscription.yaml') as f:
                self.SUBSCRIPTION = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            tb.print_exc()
            self.SUBSCRIPTION = {}

    def getList(self, chat_id):
        return self.SUBSCRIPTION.get(chat_id, [])

    def deleteIndex(self, chat_id, index):
        try:
            del self.SUBSCRIPTION[chat_id][index]
            self.save()
            return 'success'
        except Exception as e:
            return str(e)

    def getSubsribers(self, chat_id):
        result = []
        for subscriber, items in self.SUBSCRIPTION.items():
            for item in items:
                if item['id'] == chat_id:
                    result.append(subscriber)
                    break
        return result

    def add(self, chat_id, chat):
        self.SUBSCRIPTION[chat_id] = self.SUBSCRIPTION.get(chat_id, [])
        if chat['id'] in [x['id'] for x in self.SUBSCRIPTION[chat_id]]:
            return 'FAIL: subscripion already exist.'
        self.SUBSCRIPTION[chat_id].append(chat)
        self.save()
        return 'success'

    def save(self):
        with open('subscription.yaml', 'w') as f:
            f.write(yaml.dump(self.SUBSCRIPTION, sort_keys=True, indent=2))