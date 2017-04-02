from redis import Redis
import rsa
from hashlib import sha256
import json
from config import *


class Transaction(object):

    def __init__(self, prev_hash, transaction_type, sender, receiver):
        """ Constructor for creating new transaction
        """
        self.prev_hash = prev_hash
        self.transaction_type = transaction_type
        self.sender = sender
        self.receiver = receiver


    def add_signature(self, signature):
        """ Add signature to the transaction """
        self.signature = signature

    @property
    def hash(self):
        return sha256(json.dumps(self.to_dict()).encode('utf-8')).hexdigest()

    def to_dict(self):
        """
        Converts the transaction data into a serializable json format.
        """
        return {
            'prev_hash': self.prev_hash,
            'transaction_type': self.transaction_type,
            'sender': {
                'n': self.sender.n,
                'e': self.sender.e,
            },
            'receiver': {
                'n': self.receiver.n,
                'e': self.receiver.e,
            },
        }


    def to_redis(self):
        """
        Converts the entire transaction into a json format that can be put into redis
        """

        return {
            'data': self.to_dict(),
        }

    def write_to_redis(self, r):
        r.rpush(TRANSACTION_QUEUE_KEY, json.dumps(self.to_redis()))
        sig_key = "{}{}".format(TRANSACTIONS_SIGNATURE, self.hash)
        print("signature key for transaction = " + sig_key)
        r.set(sig_key, signature)


    def verify(self):
        """ Verifies the signature of transaction
        """
        try:
            rsa.verify(self.message, self.signature, self.sender)
        except VerificationError:
            print("Verification failed", file=sys.stderr)
            return False

        return True


    @classmethod
    def from_redis(cls, redis, payload):
        """ Factory to create a Transaction object from redis
        """
        print("in from redis")
        obj = cls(
            prev_hash=payload['data']['prev_hash'],
            transaction_type=payload['data']['transaction_type'],
            sender=rsa.key.PublicKey(payload['data']['sender']['n'], payload['data']['sender']['e']),
            receiver=rsa.key.PublicKey(payload['data']['receiver']['n'], payload['data']['receiver']['e']),
        )
        key = '{}{}'.format(TRANSACTIONS_SIGNATURE, obj.hash)
        print(key)
        obj.add_signature(redis.get(key))
        print("Hello")
        return obj


class Block(object):

    def __init__(self, prev_hash):
        self.prev_hash = prev_hash
        self.transactions = []
        self.signatures = []


    def full(self):
        return len(self.transactions) >= TRANSACTIONS_IN_BLOCK


    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.signatures.append(transaction.signature)

    def to_json(self):
        payload = {
            'nonce': self.nonce,
            'prev_hash': self.prev_hash,
            'transactions': [],
        }
        for t in self.transactions:
            payload['transactions'].append(t.to_redis())
        return payload


    def add_nonce(self, nonce):
        self.nonce = nonce


    @property
    def hash(self):
        return sha256(json.dumps(self.to_json()).encode('utf-8')).hexdigest()


    @classmethod
    def from_json(cls, payload):
        obj = cls(payload['prev_hash'])
        for transaction in payload['transactions']:
            obj.transactions.append(Transaction.from_json(transaction))
        obj.add_nonce(payload['nonce'])
        return obj

    def verify(self):
        acc = ''
        for t in self.transactions:
            acc += str(t.hash)

        return int(sha256((str(self.nonce)+acc).encode('utf-8')).hexdigest()[0:4],16) < GAMER_BAWA


if __name__ == '__main__':
    pass
