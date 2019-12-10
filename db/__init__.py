#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback as tb
import yaml
import time
import export_to_telegraph
from common import telegraph_token
import re

class DBClass(object):
    def __init__(self, name, default = {}):
        self.name = "db/%s.yaml" % name
        try:
            with open(self.name) as f:
                self.db = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            tb.print_exc()
            self.db = default

    def save(self):
        with open(self.name, 'w') as f:
            f.write(yaml.dump(self.db, sort_keys=True, indent=2, allow_unicode=True))


class _Source(DBClass):
    def __init__(self):
        super().__init__("source")

    def add(self, chat_id):
        if chat_id not in self.db:
            self.db[chat_id] = 0
            self.save()
            return 'success'
        return 'source already added'

    def remove(self, chat_id):
        if chat_id in self.db:
            self.db.pop(chat_id, None)
            return 'success'
        return 'no such source'

    def iterate(self, chat_id, max):
        while self.db[chat_id] < max:
            self.db[chat_id] += 1
            self.save()
            yield self.db[chat_id]

class _Subscription(DBClass):
    def __init__(self):
        super().__init__("subscription")

    def add(self, x, mode):
        if x not in self.db or self.db[x]['mode'] != mode:
            self.db[x] = mode
        self.save()

    def remove(self, x):
        self.db.pop(x, None)

def getLan(title):
    if re.search(u'[\u4e00-\u9fff]', title):
        return 'zh'
    return 'en'

class _Pool(DBClass):
    def __init__(self):
        super().__init__("pool")

    def add(self, x):
        export_to_telegraph.token = telegraph_token
        r = export_to_telegraph.get(x)
        self.db[x] = {
            "view": r['views'],
            "language": getLan(r['title']),
        }    
        self.save()

class _Sent(DBClass):
    def __init__(self):
        super().__init__("sent")

    def forget(self, x):
        self.db.pop(x, None)
        self.save()

    def add(self, gid, url):
        if not gid in self.db:
            self.db[gid] = set()
        self.save()

Subscription = _Subscription()
Sent = _Sent()
Pool = _Pool()
Source = _Source()