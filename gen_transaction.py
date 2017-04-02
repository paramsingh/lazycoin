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
    t.write_to_redis(r)
    print(r.llen(TRANSACTION_QUEUE_KEY))



