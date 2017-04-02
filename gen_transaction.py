from redis import Redis
from chain import Transaction
from user import LazyUser
from config import *
import json

if __name__ == '__main__':
    hero = LazyUser()

    t = Transaction(
        prev_hash='No hash fuck you',
        transaction_type='CREATE',
        sender=hero.pub,
        receiver=hero.pub,
    )

    message, signature = hero.sign(t)
    t.add_signature(signature)

    r = Redis()
    print(json.dumps(t.to_redis(), indent=4))
    key = "{}{}".format(TRANSACTIONS_SIGNATURE, t.hash)
    print(key)
    r.set(key, t.signature)
    r.lpush(TRANSACTION_QUEUE_KEY, json.dumps(t.to_redis()))
    print(r.get(key))
    print(r.llen(TRANSACTION_QUEUE_KEY))



