import random
import redis
from 模拟登陆.accountpool.settings import *

class RedisClient(object):

    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        return f'{self.type}:{self.website}'

    def set(self, username, value):
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        return self.db.hget(self.name(), username)

    def delete(self, username):
        return self.db.hdel(self.name(), username)

    def count(self):
        return self.db.hlen(self.name())

    def random(self):
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        return self.db.hkeys(self.name())

    def all(self):
        return self.db.hgetall(self.name())