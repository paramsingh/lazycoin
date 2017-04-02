from redis import Redis
from chain import Transaction
from user import LazyUser
from config import *
import json

if __name__ == '__main__':
    r = Redis()
    hero = LazyUser()
    receiver = LazyUser()

    t = Transaction(
        prev_hash=r.get(PREV_HASH_KEY),
        transaction_type='SEND',
        sender=hero.pub,
        receiver=receiver.pub,
    )

    message, signature = hero.sign(t)
    t.add_signature(signature)

    print(json.dumps(t.to_redis(), indent=4))
    t.write_to_redis(r)
    print(r.llen(SEND_TRANSACTION_QUEUE_KEY))



