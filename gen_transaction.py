from redis import Redis
from chain import Transaction
from user import LazyUser

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


